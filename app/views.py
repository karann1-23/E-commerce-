from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem, Profile, Category, WishlistItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as auth_logout
from django.db.models import Q

SHIPPING_COST = 50

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    cart_count = CartItem.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    wishlist_count = WishlistItem.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Category filtering
    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)
    
    return render(request, "app/index.html", {
        "products": products, 
        "categories": categories,
        "cart_count": cart_count,
        "wishlist_count": wishlist_count,
        "search_query": search_query,
        "selected_category": category_id
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('home')

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        wishlist_item.delete()  # Remove if already in wishlist
    return redirect('home')

@login_required
def view_wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    cart_count = CartItem.objects.filter(user=request.user).count()
    wishlist_count = wishlist_items.count()
    return render(request, "app/wishlist.html", {
        "wishlist_items": wishlist_items,
        "cart_count": cart_count,
        "wishlist_count": wishlist_count
    })

@login_required
def remove_from_wishlist(request, item_id):
    item = WishlistItem.objects.filter(id=item_id, user=request.user).first()
    if item:
        item.delete()
    return redirect('view_wishlist')

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    shipping = SHIPPING_COST if cart_items else 0
    total = subtotal + shipping
    cart_count = cart_items.count()
    wishlist_count = WishlistItem.objects.filter(user=request.user).count()
    return render(request, "app/cart.html", {
        "cart_items": cart_items, 
        "subtotal": subtotal, 
        "shipping": shipping, 
        "total": total, 
        "cart_count": cart_count,
        "wishlist_count": wishlist_count
    })

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    shipping = SHIPPING_COST if cart_items else 0
    total = subtotal + shipping
    cart_count = cart_items.count()
    wishlist_count = WishlistItem.objects.filter(user=request.user).count()
    payment_success = False
    if request.GET.get('success') == '1':
        payment_success = True
    if request.method == 'POST':
        return HttpResponseRedirect('/stripe-checkout/')
    return render(request, 'app/checkout.html', {
        'cart_items': cart_items, 
        'subtotal': subtotal, 
        'shipping': shipping, 
        'total': total, 
        'payment_success': payment_success, 
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })

@login_required
def stripe_checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    line_items = []
    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.product.name,
                },
                'unit_amount': int(item.product.price * 100),
            },
            'quantity': item.quantity,
        })
    # Add shipping as a separate line item if there are products
    if cart_items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Shipping',
                },
                'unit_amount': SHIPPING_COST * 100,
            },
            'quantity': 1,
        })
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/checkout/success/'),
        cancel_url=request.build_absolute_uri('/checkout/'),
    )
    return HttpResponseRedirect(session.url)

@login_required
def payment_success(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_items.delete()  # Clear the cart after payment
    cart_count = 0
    wishlist_count = WishlistItem.objects.filter(user=request.user).count()
    return render(request, 'app/payment_success.html', {
        'cart_count': cart_count,
        'wishlist_count': wishlist_count
    })

@login_required
def remove_from_cart(request, item_id):
    item = CartItem.objects.filter(id=item_id, user=request.user).first()
    if item:
        item.delete()
    return HttpResponseRedirect(reverse('view_cart'))

# Profile form for user details
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ExtraProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'phone']

@login_required
def profile(request):
    user = request.user
    profile = user.profile
    cart_count = CartItem.objects.filter(user=request.user).count()
    wishlist_count = WishlistItem.objects.filter(user=request.user).count()
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        extra_form = ExtraProfileForm(request.POST, instance=profile)
        if form.is_valid() and extra_form.is_valid():
            form.save()
            extra_form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)
        extra_form = ExtraProfileForm(instance=profile)
    return render(request, 'app/profile.html', {
        'form': form, 
        'extra_form': extra_form,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count
    })

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'app/user_login.html', {'form': form})

def user_logout(request):
    auth_logout(request)
    return redirect('user_login')