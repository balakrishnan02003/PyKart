from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Cart, CartItem
from store.models import Product


def get_or_create_cart(request):
    """Get or create cart for user (authenticated or anonymous)"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key, user=None)
    return cart


def view_cart(request):
    """Display shopping cart"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart.get_total(),
        'item_count': cart.get_item_count(),
    }
    return render(request, 'cart/cart.html', context)


@require_POST
def add_to_cart(request, product_id):
    """Add product to cart"""
    try:
        product = get_object_or_404(Product, id=product_id, is_active=True)
        quantity = int(request.POST.get('quantity', 1))
        
        # Validate quantity
        if quantity < 1:
            messages.error(request, 'Quantity must be at least 1.')
            return redirect('store:product_detail', slug=product.slug)
        
        if quantity > product.stock:
            messages.error(request, f'Only {product.stock} items available in stock.')
            return redirect('store:product_detail', slug=product.slug)
        
        cart = get_or_create_cart(request)
        
        # Get or create cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Update quantity if item already exists
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock:
                messages.error(request, f'Cannot add more. Only {product.stock} items available in stock.')
                return redirect('store:product_detail', slug=product.slug)
            cart_item.quantity = new_quantity
            cart_item.save()
        
        messages.success(request, f'{product.name} added to cart!')
        
        # Return JSON for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'{product.name} added to cart!',
                'cart_count': cart.get_item_count(),
            })
        
        return redirect('cart:view_cart')
    
    except ValueError:
        messages.error(request, 'Invalid quantity.')
        return redirect('store:home')
    except Exception as e:
        messages.error(request, 'An error occurred. Please try again.')
        return redirect('store:home')


@require_POST
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()
    
    messages.success(request, f'{product_name} removed from cart.')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = get_or_create_cart(request)
        return JsonResponse({
            'success': True,
            'message': f'{product_name} removed from cart.',
            'cart_count': cart.get_item_count(),
            'cart_total': float(cart.get_total()),
        })
    
    return redirect('cart:view_cart')


@require_POST
def update_quantity(request, item_id):
    """Update quantity of cart item"""
    try:
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        quantity = int(request.POST.get('quantity', 1))
        
        # Validate quantity
        if quantity < 1:
            messages.error(request, 'Quantity must be at least 1.')
            return redirect('cart:view_cart')
        
        if quantity > cart_item.product.stock:
            messages.error(request, f'Only {cart_item.product.stock} items available in stock.')
            return redirect('cart:view_cart')
        
        cart_item.quantity = quantity
        cart_item.save()
        
        messages.success(request, 'Cart updated.')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            cart = get_or_create_cart(request)
            return JsonResponse({
                'success': True,
                'message': 'Cart updated.',
                'cart_count': cart.get_item_count(),
                'cart_total': float(cart.get_total()),
                'item_subtotal': float(cart_item.get_subtotal()),
            })
        
        return redirect('cart:view_cart')
    
    except ValueError:
        messages.error(request, 'Invalid quantity.')
        return redirect('cart:view_cart')
    except Exception as e:
        messages.error(request, 'An error occurred. Please try again.')
        return redirect('cart:view_cart')


def get_cart_count(request):
    """Get cart item count for AJAX requests"""
    cart = get_or_create_cart(request)
    return JsonResponse({'count': cart.get_item_count()})

