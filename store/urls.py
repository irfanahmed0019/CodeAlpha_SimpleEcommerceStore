from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [

    # -------------------------
    # Store
    # -------------------------
    path("", views.home, name="home"),
    path("product/<int:id>/", views.product, name="product"),

    # -------------------------
    # Cart & Checkout
    # -------------------------
    path("cart/", views.cart, name="cart"),
    path("review/", views.review, name="review"),
    path("shipping/", views.shipping, name="shipping"),
    path("payment/", views.payment, name="payment"),
    path("orders/", views.orders, name="orders"),
    path("confirmed/<int:id>/", views.confirmed, name="confirmed"),
    path("addresses/", views.addresses, name="addresses"),

    path("add-to-cart/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/increase/<int:id>/", views.increase_quantity, name="increase_quantity"),
    path("cart/decrease/<int:id>/", views.decrease_quantity, name="decrease_quantity"),
    path("cart/delete/<int:id>/", views.delete_cart_item, name="delete_cart_item"),
    path("account/payments/",views.payment_account,name="payment_account",),
    path("login-security/",views.login_security,name="login_security",),
    # -------------------------
    # Authentication
    # -------------------------
    path("auth/", views.login, name="login"),
    path("auth/login/", views.continue_login, name="continue_login"),
    path("auth/new-user/", views.new_user, name="new_user"),
    path("auth/signup/", views.signup, name="signup"),
    path("auth/reset-password/", views.reset_password, name="reset_password"),
    path("auth/forgot-password/", views.forgot_password, name="forgot_password"),
    path("auth/logout/", views.logout_user, name="logout"),

    # -------------------------
    # User Account
    # -------------------------
    path("account/", views.user_dashboard, name="user_dashboard"),
    path(
    "category/<slug:slug>/",
    views.category_products,
    name="category_products",),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)