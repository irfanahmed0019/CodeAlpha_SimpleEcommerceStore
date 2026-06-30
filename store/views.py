from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import (
    Product,
    CartItem,
    ShippingAddress,
    Payment,
    Order,
    OrderItem,
)
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.db.models import Q
# -------------------------
# Store Pages
# -------------------------

def home(request):
    products = Product.objects.filter(featured=True)
    query=request.GET.get("q")
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query)
        )
    else:
        products = Product.objects.filter(featured=True)

    return render(request, "home.html", {"products": products,"query":query,},)


def product(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "product.html", {"product": product})

# -------------------------
# Cart Actions
# -------------------------

def get_cart_context(user):
    cart_items=CartItem.objects.filter(user=user)
    total=sum(item.total_price for item in cart_items)
    tax = Decimal("40.00")
    ship=Decimal("150.00")
    grand_total = total + tax
    ship_total=total + tax + ship
    return{
        "cart_items":cart_items,
        "total":total,
        "tax":tax,
        "grand_total":grand_total,
        "ship_total":ship_total,
    }

@login_required(login_url="login")
def cart(request):
    return render(request, "cart.html",get_cart_context(request.user)
                  )

@login_required(login_url="login")
def review(request):
    return render(request, "review.html",get_cart_context(request.user))


from .models import ShippingAddress

@login_required(login_url="login")
def shipping(request):

    if request.method == "POST":

        address, created = ShippingAddress.objects.get_or_create(
            user=request.user,
            defaults={
                "full_name": request.POST.get("full_name"),
                "email": request.POST.get("email"),
                "street": request.POST.get("street"),
                "city": request.POST.get("city"),
                "state": request.POST.get("state"),
                "pincode": request.POST.get("postal_code"),
            }
        )

        if not created:
            address.full_name = request.POST.get("full_name")
            address.email = request.POST.get("email")
            address.street = request.POST.get("street")
            address.city = request.POST.get("city")
            address.state = request.POST.get("state")
            address.pincode = request.POST.get("postal_code")
            address.save()

        return redirect("payment")
    addresses = ShippingAddress.objects.filter(
    user=request.user
)

    return render(request, "shipping.html", {
        "addresses":addresses,
        **get_cart_context(request.user)
    })


def order(request):
    return render(request, "order.html",get_cart_context(request.user))

@login_required(login_url="login")
def payment(request):

    if request.method == "POST":

        # Save payment
        payment = Payment.objects.create(
            user=request.user,
            payment_method=request.POST.get("payment_method"),
            paid=request.POST.get("payment_method") == "card"
        )

        # Get latest shipping address
        shipping = ShippingAddress.objects.filter(
            user=request.user
        ).last()

        # Get cart items
        cart_items = CartItem.objects.filter(
            user=request.user
        )

        # Create order
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping,
            payment=payment,
            total=get_cart_context(request.user)["ship_total"]
        )

        # Copy cart items into order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.discounted_price
            )

        # Empty cart
        cart_items.delete()

        # Go to confirmation page
        return redirect("confirmed", id=order.id)

    return render(
        request,
        "payment.html",
        get_cart_context(request.user)
    )


@login_required(login_url="login")
def confirmed(request, id):

    order = get_object_or_404(
        Order,
        id=id,
        user=request.user
    )

    context = {
        "order": order,
        "items": order.items.all(),
    }

    return render(
        request,
        "confirmed.html",
        context
    )


@login_required(login_url="login")
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect(request.GET.get("next","cart"))



@login_required(login_url="login")
def increase_quantity(request,id):
    cart_item=get_object_or_404(CartItem,id=id,user=request.user)

    cart_item.quantity+=1
    cart_item.save()
    return redirect(request.GET.get("next","cart"))

@login_required(login_url="login")
def decrease_quantity(request,id):
    cart_item=get_object_or_404(CartItem,id=id,user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity-=1
        cart_item.save()
    
    else:
        cart_item.delete()
    return redirect(request.GET.get("next","cart"))

@login_required(login_url="login")
def delete_cart_item(request,id):
    cart_item=get_object_or_404(CartItem,id=id,user=request.user)
    cart_item.delete()
    return redirect(request.GET.get("next","cart"))

# -------------------------
# Authentication
# -------------------------

def continue_login(request):
    email = request.session.get("email")

    context = {
        "email": email,
    }

    if request.method == "POST":
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            context["error"] = "Incorrect password."

    return render(request, "continue_login.html", context)

def login(request):
    if request.method == "POST":
        email=request.POST.get("email")
        if User.objects.filter(email=email).exists():
            request.session["email"]=email
            return redirect("continue_login")
        else:
            request.session["email"]=email
            return redirect("new_user")
    return render(request,"login.html")

def signup(request):
    email=request.session.get("email")
    context={
        "email":email,
    }
    if request.method=="POST":
        name=request.POST.get("name")
        password=request.POST.get("password")
        password_check=request.POST.get("password_check")
        if password==password_check:
            User.objects.create_user(
                username=email,
                first_name=name,
                email=email,
                password=password
            )
            user= authenticate(
                request,
                username=email,
                password=password
            )
            auth_login(request,user)
            return redirect("home")
        else:
            context["error"]="Password do not match"
    return render(request,"signup.html",context)

def reset_password(request):
    email=request.session.get("email")
    context={"email":email,}
    return render(request,"reset_password.html",context)

def forgot_password(request):
    return render(request,"forgot_password.html")

def new_user(request):
    email=request.session.get("email")
    context={"email":email}
    return render(request,"new_user.html",context)

@login_required(login_url="/auth/")
def user_dashboard(request):
    context={
        "user":request.user
    }
    return render(request,"user_dashboard.html",context)

def logout_user(request):
    logout(request)
    return redirect("home")

@login_required(login_url="login")
def orders(request):

    orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related("items__product")
        .order_by("-created_at")
    )

    return render(
        request,
        "orders.html",
        {
            "orders": orders
        }
    )
@login_required(login_url="login")
def addresses(request):

    addresses = ShippingAddress.objects.filter(
        user=request.user
    )

    context = {
        "addresses": addresses,
    }

    return render(
        request,
        "addresses.html",
        context
    )

@login_required(login_url="login")
def payment_account(request):

    payments = (
        Payment.objects
        .filter(user=request.user)
        .order_by("-created_at")
    )

    context = {
        "payments": payments,
    }

    return render(
        request,
        "payment_account.html",
        context
    )

@login_required(login_url="login")
def login_security(request):
    context={
        "user": request.user,
    }
    return render(request,"login_security.html",context)

def category_products(request, slug):
    category = get_object_or_404(
        Category,
        name__iexact=slug.replace("-", " ")
    )

    products = Product.objects.filter(category=category)

    categories = Category.objects.all()

    return render(
        request,
        "category.html",
        {
            "category": category,
            "products": products,
            "categories": categories,
        },
    )