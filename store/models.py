from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User


# -------------------------
# Category
# -------------------------

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    banner = models.ImageField(upload_to="categories/", blank=True)

    def __str__(self):
        return self.name

# -------------------------
# Product
# -------------------------

class Product(models.Model):
    name = models.CharField(max_length=200)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )
    featured = models.BooleanField(default=False)
    brand = models.CharField(max_length=100, blank=True, null=True)
    stock = models.PositiveBigIntegerField(default=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)

    @property
    def savings(self):
        return self.original_price - self.discounted_price

    @property
    def discount_percentage(self):
        if self.original_price > 0:
            return round(
                (self.savings / self.original_price) * Decimal("100")
            )
        return 0

    def __str__(self):
        return self.name


# -------------------------
# Product Specification
# -------------------------

class Specification(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="specifications"
    )

    specification = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.product.name} - {self.specification}"


@property
def savings(self):
    return self.original_price - self.discounted_price

@property
def discount_percentage(self):
    if self.original_price > 0:
        return round(
            (self.savings / self.original_price) * Decimal("100")
        )
    return 0

# -------------------------
# Product Images
# -------------------------

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="products/gallery/")

    def __str__(self):
        return self.product.name


# -------------------------
# Cart
# -------------------------

class CartItem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.discounted_price * self.quantity

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"


# -------------------------
# Shipping Address
# -------------------------

class ShippingAddress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shipping_addresses"
    )

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    street = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.full_name} - {self.city}"


# -------------------------
# Payment
# -------------------------

class Payment(models.Model):
    PAYMENT_CHOICES = [
        ("card", "Card"),
        ("cod", "Cash on Delivery"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES
    )

    paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.user.username} - {self.payment_method}"


# -------------------------
# Order
# -------------------------

class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    shipping_address = models.ForeignKey(
        ShippingAddress,
        on_delete=models.SET_NULL,
        null=True
    )

    payment = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        null=True
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


# -------------------------
# Order Items
# -------------------------

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"
    
