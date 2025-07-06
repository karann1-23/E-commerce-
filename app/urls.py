from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("add-to-wishlist/<int:product_id>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/", views.view_wishlist, name="view_wishlist"),
    path("remove-from-wishlist/<int:item_id>/", views.remove_from_wishlist, name="remove_from_wishlist"),
    path("cart/", views.view_cart, name="view_cart"),
    path("remove-from-cart/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("stripe-checkout/", views.stripe_checkout, name="stripe_checkout"),
    path("checkout/success/", views.payment_success, name="payment_success"),
    path("profile/", views.profile, name="profile"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
]