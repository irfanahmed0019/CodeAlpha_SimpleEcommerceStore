"""
seed_products.py

Idempotent seed script that creates 30 realistic e-commerce products.

Usage (Django shell script):
    python manage.py shell < seed_products.py

Or as a management command, copy this into:
    yourapp/management/commands/seed_products.py
and wrap the body in a Command.handle() method.
"""

import django
import os
import sys
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")
django.setup()

from store.models import Product, Category  # noqa: E402


def get_category(name):
    try:
        return Category.objects.get(name=name)
    except Category.DoesNotExist:
        raise SystemExit(
            f'Category "{name}" does not exist. Please create the categories '
            f"Electronics, Home Office, and Accessories before running this script."
        )


def seed():
    electronics = get_category("Electronics")
    home_office = get_category("Home Office")
    accessories = get_category("Accessories")

    products = [
        # ---------------- Electronics (12) ----------------
        dict(
            name="Sony WH-1000XM5 Wireless Headphones",
            original_price=Decimal("34990.00"),
            discounted_price=Decimal("27627.00"),
            description="Industry-leading noise cancellation with crystal-clear hands-free calling and up to 30 hours of battery life.",
            category=electronics,
            featured=True,
            brand="Sony",
            stock=45,
            rating=4.8,
        ),
        dict(
            name="Apple MacBook Air 13-inch (M3)",
            original_price=Decimal("84990.00"),
            discounted_price=Decimal("62990.00"),
            description="Strikingly thin laptop powered by the M3 chip, delivering blazing performance and all-day battery life.",
            category=electronics,
            featured=True,
            brand="Apple",
            stock=25,
            rating=4.9,
        ),
        dict(
            name="Samsung 55-inch QLED 4K Smart TV",
            original_price=Decimal("74699.00"),
            discounted_price=Decimal("62199.00"),
            description="Vivid Quantum Dot color and AI-powered upscaling bring every scene to life on a sleek, bezel-less display.",
            category=electronics,
            featured=False,
            brand="Samsung",
            stock=18,
            rating=4.6,
        ),
        dict(
            name="Dell XPS 15 Laptop",
            original_price=Decimal("157599.00"),
            discounted_price=Decimal("140999.00"),
            description="Premium 15-inch laptop with InfinityEdge display, powerful Intel Core processor, and stunning build quality.",
            category=electronics,
            featured=False,
            brand="Dell",
            stock=15,
            rating=4.7,
        ),
        dict(
            name="iPad Pro 11-inch (M4)",
            original_price=Decimal("82899.00"),
            discounted_price=Decimal("74599.00"),
            description="Ultra-thin tablet with the powerful M4 chip and a stunning Ultra Retina XDR display for creative professionals.",
            category=electronics,
            featured=True,
            brand="Apple",
            stock=30,
            rating=4.8,
        ),
        dict(
            name="Bose SoundLink Revolve+ Bluetooth Speaker",
            original_price=Decimal("24799.00"),
            discounted_price=Decimal("20699.00"),
            description="360-degree immersive sound in a durable, water-resistant design built for all-day adventures.",
            category=electronics,
            featured=False,
            brand="Bose",
            stock=50,
            rating=4.5,
        ),
        dict(
            name="Canon EOS R50 Mirrorless Camera",
            original_price=Decimal("66399.00"),
            discounted_price=Decimal("56399.00"),
            description="Compact mirrorless camera with 24.2MP sensor, ideal for creators stepping up their photo and video game.",
            category=electronics,
            featured=False,
            brand="Canon",
            stock=12,
            rating=4.6,
        ),
        dict(
            name="Logitech MX Master 3S Wireless Mouse",
            original_price=Decimal("8299.00"),
            discounted_price=Decimal("6599.00"),
            description="Ultra-precise 8K DPI sensor with quiet clicks, designed for all-day productivity across multiple devices.",
            category=electronics,
            featured=False,
            brand="Logitech",
            stock=80,
            rating=4.7,
        ),
        dict(
            name="Samsung Galaxy Tab S9",
            original_price=Decimal("66399.00"),
            discounted_price=Decimal("58099.00"),
            description="Sleek, durable tablet with a vivid AMOLED display and included S Pen for note-taking and creativity.",
            category=electronics,
            featured=False,
            brand="Samsung",
            stock=22,
            rating=4.5,
        ),
        dict(
            name="JBL Flip 6 Portable Speaker",
            original_price=Decimal("10799.00"),
            discounted_price=Decimal("8299.00"),
            description="Bold JBL Original Pro Sound in a rugged, waterproof speaker built for adventures anywhere.",
            category=electronics,
            featured=False,
            brand="JBL",
            stock=60,
            rating=4.4,
        ),
        dict(
            name="ASUS ROG Strix Gaming Monitor 27-inch",
            original_price=Decimal("37299.00"),
            discounted_price=Decimal("31499.00"),
            description="Fast 165Hz refresh rate and crisp QHD resolution deliver a smooth, immersive gaming experience.",
            category=electronics,
            featured=False,
            brand="ASUS",
            stock=20,
            rating=4.6,
        ),
        dict(
            name="Amazon Echo Dot (5th Gen)",
            original_price=Decimal("4099.00"),
            discounted_price=Decimal("2899.00"),
            description="Compact smart speaker with Alexa, delivering crisp vocals and balanced bass for any room.",
            category=electronics,
            featured=False,
            brand="Amazon",
            stock=100,
            rating=4.3,
        ),

        # ---------------- Home Office (8) ----------------
        dict(
            name="Herman Miller Aeron Office Chair",
            original_price=Decimal("124099.00"),
            discounted_price=Decimal("107499.00"),
            description="Ergonomic icon engineered with PostureFit support, breathable mesh, and a fully adjustable frame.",
            category=home_office,
            featured=True,
            brand="Herman Miller",
            stock=10,
            rating=4.9,
        ),
        dict(
            name="Uplift V2 Standing Desk",
            original_price=Decimal("66299.00"),
            discounted_price=Decimal("57999.00"),
            description="Whisper-quiet dual motor sit-stand desk with memory presets and a sturdy steel frame.",
            category=home_office,
            featured=True,
            brand="Uplift Desk",
            stock=14,
            rating=4.8,
        ),
        dict(
            name="BenQ ScreenBar Desk Lamp",
            original_price=Decimal("8999.00"),
            discounted_price=Decimal("7399.00"),
            description="Auto-dimming monitor light bar that eliminates screen glare without taking up desk space.",
            category=home_office,
            featured=False,
            brand="BenQ",
            stock=40,
            rating=4.6,
        ),
        dict(
            name="HP OfficeJet Pro Wireless Printer",
            original_price=Decimal("20699.00"),
            discounted_price=Decimal("16599.00"),
            description="All-in-one wireless printer with fast print speeds and rich, professional-quality color output.",
            category=home_office,
            featured=False,
            brand="HP",
            stock=18,
            rating=4.3,
        ),
        dict(
            name="Steelcase Series 2 Office Chair",
            original_price=Decimal("41399.00"),
            discounted_price=Decimal("35599.00"),
            description="Adaptive back support and a sleek, modern silhouette make long workdays effortlessly comfortable.",
            category=home_office,
            featured=False,
            brand="Steelcase",
            stock=16,
            rating=4.7,
        ),
        dict(
            name="Fellowes Bamboo Monitor Stand",
            original_price=Decimal("4999.00"),
            discounted_price=Decimal("3699.00"),
            description="Sustainable bamboo riser that elevates your monitor while organizing desk space underneath.",
            category=home_office,
            featured=False,
            brand="Fellowes",
            stock=55,
            rating=4.4,
        ),
        dict(
            name="Shark Cordless Stick Vacuum",
            original_price=Decimal("27399.00"),
            discounted_price=Decimal("23199.00"),
            description="Lightweight, powerful cordless vacuum with versatile attachments for a spotless home office.",
            category=home_office,
            featured=False,
            brand="Shark",
            stock=24,
            rating=4.5,
        ),
        dict(
            name="Anker PowerExtend Mini Power Strip",
            original_price=Decimal("3299.00"),
            discounted_price=Decimal("2499.00"),
            description="Compact surge-protected power strip with USB-C charging, perfect for organized desk setups.",
            category=home_office,
            featured=False,
            brand="Anker",
            stock=70,
            rating=4.2,
        ),

        # ---------------- Accessories (10) ----------------
        dict(
            name="Apple Watch Series 10",
            original_price=Decimal("49900.00"),
            discounted_price=Decimal("37999.00"),
            description="Advanced health tracking and a brighter, larger display in Apple's most refined watch yet.",
            category=accessories,
            featured=True,
            brand="Apple",
            stock=35,
            rating=4.8,
        ),
        dict(
            name="Ray-Ban Aviator Classic Sunglasses",
            original_price=Decimal("15199.00"),
            discounted_price=Decimal("12399.00"),
            description="Timeless aviator silhouette with crystal lenses and a lightweight, durable metal frame.",
            category=accessories,
            featured=True,
            brand="Ray-Ban",
            stock=42,
            rating=4.6,
        ),
        dict(
            name="Fossil Gen 6 Smartwatch",
            original_price=Decimal("24799.00"),
            discounted_price=Decimal("18999.00"),
            description="Stylish hybrid smartwatch with fitness tracking, heart rate monitoring, and customizable watch faces.",
            category=accessories,
            featured=False,
            brand="Fossil",
            stock=28,
            rating=4.2,
        ),
        dict(
            name="Herschel Supply Co. Little America Backpack",
            original_price=Decimal("12399.00"),
            discounted_price=Decimal("9999.00"),
            description="Classic silhouette backpack with a padded laptop sleeve, perfect for commuting or travel.",
            category=accessories,
            featured=False,
            brand="Herschel",
            stock=38,
            rating=4.5,
        ),
        dict(
            name="Anker 737 Power Bank",
            original_price=Decimal("12399.00"),
            discounted_price=Decimal("9999.00"),
            description="High-capacity 24,000mAh portable charger with fast charging for phones, tablets, and laptops.",
            category=accessories,
            featured=False,
            brand="Anker",
            stock=65,
            rating=4.7,
        ),
        dict(
            name="Pelican Protector Phone Case",
            original_price=Decimal("4099.00"),
            discounted_price=Decimal("3299.00"),
            description="Military-grade drop protection wrapped in a slim, lightweight design that won't bulk up your phone.",
            category=accessories,
            featured=False,
            brand="Pelican",
            stock=90,
            rating=4.3,
        ),
        dict(
            name="Tumi Alpha Leather Wallet",
            original_price=Decimal("16199.00"),
            discounted_price=Decimal("13199.00"),
            description="Sleek full-grain leather wallet with RFID-blocking technology and a slim, minimalist profile.",
            category=accessories,
            featured=False,
            brand="Tumi",
            stock=33,
            rating=4.6,
        ),
        dict(
            name="Garmin Forerunner 265 Sports Watch",
            original_price=Decimal("37299.00"),
            discounted_price=Decimal("33199.00"),
            description="Advanced GPS running watch with a vivid AMOLED display and in-depth training metrics.",
            category=accessories,
            featured=True,
            brand="Garmin",
            stock=20,
            rating=4.8,
        ),
        dict(
            name="Coach Signature Leather Belt",
            original_price=Decimal("10599.00"),
            discounted_price=Decimal("8199.00"),
            description="Classic reversible leather belt featuring iconic signature canvas and a polished buckle.",
            category=accessories,
            featured=False,
            brand="Coach",
            stock=48,
            rating=4.4,
        ),
        dict(
            name="Peak Design Everyday Sling Bag",
            original_price=Decimal("13299.00"),
            discounted_price=Decimal("10799.00"),
            description="Weatherproof, thoughtfully organized sling bag designed for photographers and everyday carry.",
            category=accessories,
            featured=False,
            brand="Peak Design",
            stock=27,
            rating=4.7,
        ),
    ]

    featured_count = sum(1 for p in products if p["featured"])
    assert featured_count == 8, f"Expected 8 featured products, got {featured_count}"
    assert len(products) == 30, f"Expected 30 products, got {len(products)}"

    created_count = 0
    updated_count = 0

    for data in products:
        defaults = {k: v for k, v in data.items() if k != "name"}
        obj, created = Product.objects.get_or_create(
            name=data["name"],
            defaults=defaults,
        )
        if created:
            created_count += 1
            print(f"Created: {obj.name}")
        else:
            updated_count += 1
            print(f"Already exists, skipped: {obj.name}")

    print(f"\nDone. {created_count} created, {updated_count} already existed.")


if __name__ == "__main__":
    seed()
else:
    # Allows running via `python manage.py shell < seed_products.py`
    seed()