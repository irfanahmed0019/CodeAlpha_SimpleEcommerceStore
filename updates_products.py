from store.models import Product, Category

electronics = Category.objects.get(name="Electronics")
home = Category.objects.get(name="Home Office")
accessories = Category.objects.get(name="Accessories")

electronics_products = [
    "Sony WH-1000XM5 Wireless Headphones",
    "Apple MacBook Air 13-inch (M3)",
    "Samsung 55-inch QLED 4K Smart TV",
    "Dell XPS 15 Laptop",
    "iPad Pro 11-inch (M4)",
    "Bose SoundLink Revolve+ Bluetooth Speaker",
    "Canon EOS R50 Mirrorless Camera",
    "Logitech MX Master 3S Wireless Mouse",
    "Samsung Galaxy Tab S9",
    "JBL Flip 6 Portable Speaker",
    "ASUS ROG Strix Gaming Monitor 27-inch",
    "Amazon Echo Dot (5th Gen)",
]

home_products = [
    "Herman Miller Aeron Office Chair",
    "Uplift V2 Standing Desk",
    "BenQ ScreenBar Desk Lamp",
    "HP OfficeJet Pro Wireless Printer",
    "Steelcase Series 2 Office Chair",
    "Fellowes Bamboo Monitor Stand",
    "Shark Cordless Stick Vacuum",
    "Anker PowerExtend Mini Power Strip",
]

accessories_products = [
    "Apple Watch Series 10",
    "Ray-Ban Aviator Classic Sunglasses",
    "Fossil Gen 6 Smartwatch",
    "Herschel Supply Co. Little America Backpack",
    "Anker 737 Power Bank",
    "Pelican Protector Phone Case",
    "Tumi Alpha Leather Wallet",
    "Garmin Forerunner 265 Sports Watch",
    "Coach Signature Leather Belt",
    "Peak Design Everyday Sling Bag",
]

for name in electronics_products:
    Product.objects.filter(name=name).update(category=electronics)

for name in home_products:
    Product.objects.filter(name=name).update(category=home)

for name in accessories_products:
    Product.objects.filter(name=name).update(category=accessories)

print("✅ Categories updated successfully.")