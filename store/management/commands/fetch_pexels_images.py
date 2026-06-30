"""
Django management command: fetch_pexels_images

Finds every Product without an image, searches the Pexels API using a
multi-tier query strategy (brand+category > full name > brand > category),
scores candidate photos against the product's brand/category/name keywords
using Pexels' alt-text, and picks the BEST match instead of the first
landscape result. Falls back through queries until something usable is found.

WHY THIS MATTERS:
Pexels has no concept of "Sony WH-1000XM5" — it's keyword matching against
photographer-submitted alt text. Searching the exact model number usually
returns nothing or junk. Searching "Sony headphones" returns relevant stock
photos far more often. This version queries smarter AND scores results
instead of blindly taking photo #1.

LIMITATION THAT WON'T GO AWAY:
This will never return the EXACT product photo (the actual MacBook Air, the
actual WH-1000XM5 box shot). Stock photography fundamentally can't do that.
If you need exact-SKU images for a real production catalog, you need a
product image API (Google Shopping Content API, Amazon PA-API, a manufacturer
press kit, or manual sourcing) — not Pexels/Unsplash. Use this script for
demo/seed data and portfolio projects, not for products real customers buy.

Setup:
    1. Place this file at: <yourapp>/management/commands/fetch_pexels_images.py
       (create management/ and management/commands/ folders with empty
       __init__.py files if they don't already exist)
    2. Get a free API key from https://www.pexels.com/api/
    3. Set it as an environment variable:
           export PEXELS_API_KEY="your-key-here"

Usage:
    python manage.py fetch_pexels_images
    python manage.py fetch_pexels_images --dry-run
    python manage.py fetch_pexels_images --limit 10
    python manage.py fetch_pexels_images --delay 1.5
    python manage.py fetch_pexels_images --min-score 1   (looser matching)
    python manage.py fetch_pexels_images --force          (re-fetch even if image exists)
"""

import logging
import os
import re
import time

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger("fetch_pexels_images")

PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"
DEFAULT_DELAY_SECONDS = 1.0  # be polite to the free-tier rate limit (200 req/hr)
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 2.0
REQUEST_TIMEOUT = 15
PER_PAGE = 8  # pull more candidates so scoring has something to work with

# Generic filler words stripped out of product names before building queries.
# These add noise to the search ("Wireless", "Pro", "5th Gen") without
# helping Pexels find a relevant photo, and they hurt alt-text scoring.
NOISE_WORDS = {
    "wireless", "pro", "max", "plus", "ultra", "gen", "edition", "series",
    "inch", "in", "the", "with", "for", "and", "smart", "portable",
    "rechargeable", "official", "genuine", "new", "v2", "2nd", "3rd", "4th",
    "5th", "6th", "1st",
}

# Model-number-looking tokens (e.g. "WH-1000XM5", "M3", "RTX4060") are
# stripped for SEARCH queries (Pexels can't match them) but kept for
# SCORING so a photo whose alt text happens to mention them still gets
# bonus relevance.
MODEL_TOKEN_RE = re.compile(r"^[A-Za-z]*\d[A-Za-z0-9\-]*$")


def configure_logging(verbosity):
    level = logging.DEBUG if verbosity >= 2 else logging.INFO
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%H:%M:%S")
    )
    logger.handlers = [handler]
    logger.setLevel(level)
    logger.propagate = False


def print_progress(current, total, label=""):
    width = 30
    filled = int(width * current / total) if total else width
    bar = "#" * filled + "-" * (width - filled)
    print(f"\r[{bar}] {current}/{total} {label}", end="", flush=True)
    if current >= total:
        print()


def tokenize(text):
    return [t for t in re.findall(r"[a-z0-9]+", (text or "").lower()) if len(t) > 1]


# Maps product-type keywords (as they'd appear in a product name) to a
# canonical, Pexels-searchable noun. Order doesn't matter for lookup, but
# longer/more-specific keys are checked first so "gaming monitor" beats
# a bare "monitor" match, etc. Extend this as your catalog grows.
PRODUCT_TYPE_MAP = {
    # Electronics
    "headphone": "headphones", "headphones": "headphones",
    "earbud": "earbuds", "earbuds": "earbuds",
    "laptop": "laptop", "notebook": "laptop", "macbook": "laptop",
    "desktop": "desktop computer",
    "monitor": "monitor", "display": "monitor",
    "tv": "television", "television": "television",
    "mouse": "computer mouse",
    "keyboard": "keyboard",
    "speaker": "speaker", "soundbar": "soundbar",
    "camera": "camera",
    "tablet": "tablet", "ipad": "tablet",
    "smartwatch": "smartwatch", "watch": "watch",
    "printer": "printer",
    "router": "router",
    "webcam": "webcam",
    "charger": "charger", "power bank": "power bank", "powerbank": "power bank",
    "drone": "drone",
    "projector": "projector",
    "phone": "smartphone", "smartphone": "smartphone",
    "vacuum": "vacuum cleaner",
    # Home / office furniture
    "chair": "office chair",
    "desk": "desk",
    "lamp": "desk lamp",
    "stand": "monitor stand",
    "shelf": "shelf", "shelving": "shelving",
    # Accessories / fashion
    "backpack": "backpack",
    "bag": "bag", "sling": "sling bag",
    "wallet": "wallet",
    "belt": "leather belt",
    "sunglasses": "sunglasses",
    "case": "phone case",
    "strip": "power strip",
}

# Descriptive modifiers worth keeping in the query (unlike NOISE_WORDS)
# because they meaningfully narrow the stock photo result, e.g.
# "gaming monitor" / "wireless mouse" / "office chair" / "standing desk".
TYPE_MODIFIERS = {
    "gaming", "wireless", "mechanical", "standing", "noise", "cancelling",
    "cancellation", "portable", "bluetooth", "ergonomic", "cordless",
    "leather", "running", "sports",
}


def extract_product_type(name_tokens):
    """
    Scan tokenized product name for a known product-type keyword and
    return (canonical_type, modifier_or_None). Checks two-word phrases
    first (e.g. "power bank") then single tokens.
    """
    joined = " ".join(name_tokens)
    # two-word product types first
    for key, canonical in PRODUCT_TYPE_MAP.items():
        if " " in key and key in joined:
            return canonical, _find_modifier(name_tokens, key)
    # single-word product types, longest key first to prefer specificity
    for key in sorted((k for k in PRODUCT_TYPE_MAP if " " not in k), key=len, reverse=True):
        if key in name_tokens:
            return PRODUCT_TYPE_MAP[key], _find_modifier(name_tokens, key)
    return None, None


def _find_modifier(name_tokens, type_key):
    """Find a useful descriptive modifier token (e.g. 'gaming', 'wireless')
    that appears in the name alongside the product type, to build queries
    like 'gaming laptop' or 'wireless mouse'."""
    for t in name_tokens:
        if t in TYPE_MODIFIERS:
            return t
    return None


def build_query_chain(product):
    """
    Returns an ordered list of query strings to try, most specific first.
    Priority:
        1. brand + product type            -> "Sony headphones"
        2. modifier + product type          -> "gaming laptop", "office chair"
        3. product type alone                -> "headphones"
        4. cleaned full product name         -> fallback for unmapped types
        5. brand alone
        6. category (last resort only)
    """
    name = product.name or ""
    brand = getattr(product, "brand", "") or ""
    category = getattr(product.category, "name", "") if getattr(product, "category", None) else ""

    name_tokens = [
        t for t in tokenize(name)
        if t not in NOISE_WORDS and not MODEL_TOKEN_RE.match(t)
    ]
    clean_name = " ".join(name_tokens)

    product_type, modifier = extract_product_type(tokenize(name))

    chain = []
    if brand and product_type:
        chain.append(f"{brand} {product_type}")
    if modifier and product_type:
        chain.append(f"{modifier} {product_type}")
    if product_type:
        chain.append(product_type)
    if clean_name:
        chain.append(clean_name)
    if brand:
        chain.append(brand)
    if category:
        # last resort only -- this is what was returning "Sony cameras"
        # for headphones before, so it now sits at the bottom of the chain.
        chain.append(category)

    # de-dupe, preserve order
    seen = set()
    deduped = []
    for q in chain:
        q = q.strip()
        if q and q.lower() not in seen:
            seen.add(q.lower())
            deduped.append(q)
    return deduped


def score_photo(photo, product):
    """
    Score a Pexels photo's relevance to the product using alt text overlap
    with brand, category, and product-name keywords (including model
    numbers, which we don't search on but DO reward if they show up).
    Higher is better. Also requires landscape/square orientation to be
    eligible at all (returns -1 if portrait).
    """
    width = photo.get("width") or 0
    height = photo.get("height") or 0
    if not height or width < height:
        return -1

    alt = (photo.get("alt") or "").lower()
    if not alt:
        # No alt text to score against — treat as weak/neutral match
        return 0

    alt_tokens = set(tokenize(alt))

    name_tokens = set(tokenize(product.name))
    brand_tokens = set(tokenize(getattr(product, "brand", "") or ""))
    category_tokens = set(
        tokenize(getattr(product.category, "name", "") if getattr(product, "category", None) else "")
    )
    product_type, _modifier = extract_product_type(tokenize(product.name))
    type_tokens = set(tokenize(product_type)) if product_type else set()

    score = 0
    # Product-type match matters MOST: a "headphones" photo for a
    # headphones product beats a "Sony"-tagged photo of a camera.
    score += 4 * len(type_tokens & alt_tokens)
    score += 3 * len(brand_tokens & alt_tokens)
    score += 1 * len(category_tokens & alt_tokens)
    score += 1 * len(name_tokens & alt_tokens)
    return score


def pick_best_photo(photos, product, min_score=1):
    """
    Score all candidate photos and return the highest scorer that meets
    min_score. Returns None if nothing qualifies.
    """
    scored = [(score_photo(p, product), p) for p in photos]
    scored = [(s, p) for s, p in scored if s >= 0]  # drop portrait/invalid
    if not scored:
        return None
    scored.sort(key=lambda pair: pair[0], reverse=True)
    best_score, best_photo = scored[0]
    if best_score < min_score:
        return None
    return best_photo


class PexelsClient:
    def __init__(self, api_key, delay=DEFAULT_DELAY_SECONDS):
        self.api_key = api_key
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({"Authorization": api_key})
        self._last_request_time = 0.0

    def _throttle(self):
        elapsed = time.monotonic() - self._last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)

    def search(self, query, per_page=PER_PAGE):
        params = {"query": query, "per_page": per_page}

        for attempt in range(1, MAX_RETRIES + 1):
            self._throttle()
            try:
                self._last_request_time = time.monotonic()
                response = self.session.get(
                    PEXELS_SEARCH_URL, params=params, timeout=REQUEST_TIMEOUT
                )
            except requests.RequestException as exc:
                logger.warning(
                    "Network error searching Pexels for %r (attempt %d/%d): %s",
                    query, attempt, MAX_RETRIES, exc,
                )
                time.sleep(RETRY_BACKOFF_SECONDS * attempt)
                continue

            if response.status_code == 429:
                wait = RETRY_BACKOFF_SECONDS * attempt * 3
                logger.warning(
                    "Rate limited by Pexels (attempt %d/%d). Waiting %.1fs.",
                    attempt, MAX_RETRIES, wait,
                )
                time.sleep(wait)
                continue

            if response.status_code >= 500:
                logger.warning(
                    "Pexels server error %s for %r (attempt %d/%d).",
                    response.status_code, query, attempt, MAX_RETRIES,
                )
                time.sleep(RETRY_BACKOFF_SECONDS * attempt)
                continue

            if response.status_code != 200:
                logger.error(
                    "Pexels search failed for %r: HTTP %s - %s",
                    query, response.status_code, response.text[:200],
                )
                return []

            try:
                data = response.json()
            except ValueError:
                logger.error("Invalid JSON from Pexels for query %r", query)
                return []

            return data.get("photos", [])

        logger.error("Exhausted retries searching Pexels for %r", query)
        return []

    def download_image(self, url):
        for attempt in range(1, MAX_RETRIES + 1):
            self._throttle()
            try:
                self._last_request_time = time.monotonic()
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            except requests.RequestException as exc:
                logger.warning(
                    "Network error downloading image (attempt %d/%d): %s",
                    attempt, MAX_RETRIES, exc,
                )
                time.sleep(RETRY_BACKOFF_SECONDS * attempt)
                continue

            if response.status_code == 200:
                return response.content

            if response.status_code >= 500 or response.status_code == 429:
                logger.warning(
                    "Transient error %s downloading image (attempt %d/%d).",
                    response.status_code, attempt, MAX_RETRIES,
                )
                time.sleep(RETRY_BACKOFF_SECONDS * attempt)
                continue

            logger.error("Image download failed: HTTP %s for %s", response.status_code, url)
            return None

        logger.error("Exhausted retries downloading image from %s", url)
        return None


def build_filename(product, photo):
    slug_source = product.name.lower()
    slug = "".join(c if c.isalnum() else "-" for c in slug_source).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    photo_id = photo.get("id", "0")
    return f"{slug}-{photo_id}.jpg"


class Command(BaseCommand):
    help = "Fetch and attach Pexels images for products, using smarter query + relevance scoring."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true",
                             help="Search and log what would happen, but don't save anything.")
        parser.add_argument("--limit", type=int, default=None,
                             help="Only process the first N products missing images.")
        parser.add_argument("--delay", type=float, default=DEFAULT_DELAY_SECONDS,
                             help=f"Seconds to wait between Pexels API calls (default: {DEFAULT_DELAY_SECONDS}).")
        parser.add_argument("--min-score", type=int, default=1,
                             help="Minimum alt-text relevance score required to accept a photo (default: 1). "
                                  "Set to 0 to accept any landscape/square photo even with no keyword overlap.")
        parser.add_argument("--force", action="store_true",
                             help="Re-fetch and overwrite images even for products that already have one.")

    def handle(self, *args, **options):
        configure_logging(options.get("verbosity", 1))

        api_key = os.environ.get("PEXELS_API_KEY")
        if not api_key:
            raise CommandError(
                "PEXELS_API_KEY environment variable is not set. "
                "Get a free key at https://www.pexels.com/api/ and export it."
            )

        from store.models import Product  # noqa: E402 -- adjust "store" if needed

        dry_run = options["dry_run"]
        limit = options["limit"]
        delay = options["delay"]
        min_score = options["min_score"]
        force = options["force"]

        if force:
            queryset = Product.objects.all().order_by("id")
        else:
            queryset = (
                Product.objects.filter(image="") | Product.objects.filter(image__isnull=True)
            ).distinct().order_by("id")

        if limit:
            queryset = queryset[:limit]

        products = list(queryset)
        total = len(products)

        if total == 0:
            self.stdout.write(self.style.SUCCESS("No products need images. Nothing to do."))
            return

        logger.info("Found %d product(s) to process.", total)
        if dry_run:
            logger.info("Running in --dry-run mode: no files or DB rows will change.")

        client = PexelsClient(api_key=api_key, delay=delay)

        succeeded = 0
        skipped = 0
        failed = 0

        for index, product in enumerate(products, start=1):
            print_progress(index - 1, total, label=product.name[:40])

            if product.image and not force:
                logger.debug("Skipping %r: already has an image.", product.name)
                skipped += 1
                continue

            queries = build_query_chain(product)
            photo = None
            winning_query = None

            for query in queries:
                logger.info("Searching Pexels for %r ...", query)
                photos = client.search(query)
                photo = pick_best_photo(photos, product, min_score=min_score)
                if photo:
                    winning_query = query
                    logger.info(
                        "Matched %r using query %r (photo id %s, alt=%r).",
                        product.name, query, photo.get("id"), photo.get("alt"),
                    )
                    break
                logger.info("No sufficiently relevant match for query %r.", query)

            if not photo:
                logger.warning(
                    "No suitable image found for %r (tried: %s). Skipping.",
                    product.name, ", ".join(queries) or "none",
                )
                failed += 1
                continue

            image_url = (
                photo.get("src", {}).get("large2x")
                or photo.get("src", {}).get("large")
                or photo.get("src", {}).get("original")
            )
            if not image_url:
                logger.error("Photo result for %r had no usable src URL. Skipping.", product.name)
                failed += 1
                continue

            image_bytes = client.download_image(image_url)
            if not image_bytes:
                logger.error("Failed to download image for %r. Skipping.", product.name)
                failed += 1
                continue

            filename = build_filename(product, photo)

            if dry_run:
                logger.info(
                    "[dry-run] Would save %s (%d bytes) to %r.image (matched via %r)",
                    filename, len(image_bytes), product.name, winning_query,
                )
                succeeded += 1
                continue

            try:
                product.image.save(filename, ContentFile(image_bytes), save=True)
            except Exception as exc:  # noqa: BLE001
                logger.error("Failed to save image for %r: %s", product.name, exc)
                failed += 1
                continue

            logger.info("Saved image for %r -> media/products/%s", product.name, filename)
            succeeded += 1

        print_progress(total, total, label="done")

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Succeeded: {succeeded}"))
        self.stdout.write(self.style.WARNING(f"Skipped (already had image): {skipped}"))
        self.stdout.write(
            self.style.ERROR(f"Failed/no match: {failed}") if failed else "Failed/no match: 0"
        )