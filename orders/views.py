from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
import random
import string
from cart.models import Cart, CartItem
from accounts.models import Address
from .models import Order, OrderItem


def generate_order_number():
    """Generate unique order number"""
    timestamp = timezone.now().strftime('%Y%m%d')
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f'ORD-{timestamp}-{random_str}'


@login_required
def checkout(request):
    """Checkout page - review cart and place order"""
    # Get user's cart
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart:view_cart')
    
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart:view_cart')
    
    # Get user's addresses
    addresses = Address.objects.filter(user=request.user)
    
    # Calculate totals
    subtotal = cart.get_total()
    tax = subtotal * Decimal('0.10')  # 10% tax (mock)
    shipping_cost = Decimal('10.00') if subtotal < Decimal('100') else Decimal('0.00')  # Free shipping over ₹100
    total = subtotal + tax + shipping_cost
    
    if request.method == 'POST':
        # Get selected address
        address_id = request.POST.get('address_id')
        if not address_id:
            messages.error(request, 'Please select a shipping address.')
            return render(request, 'orders/checkout.html', {
                'cart': cart,
                'cart_items': cart_items,
                'addresses': addresses,
                'subtotal': subtotal,
                'tax': tax,
                'shipping_cost': shipping_cost,
                'total': total,
            })
        
        try:
            address = Address.objects.get(id=address_id, user=request.user)
        except Address.DoesNotExist:
            messages.error(request, 'Invalid address selected.')
            return render(request, 'orders/checkout.html', {
                'cart': cart,
                'cart_items': cart_items,
                'addresses': addresses,
                'subtotal': subtotal,
                'tax': tax,
                'shipping_cost': shipping_cost,
                'total': total,
            })
        
        # Create order
        order_number = generate_order_number()
        order = Order.objects.create(
            order_number=order_number,
            user=request.user,
            shipping_name=address.full_name,
            shipping_phone=address.phone_number,
            shipping_address_line1=address.address_line1,
            shipping_address_line2=address.address_line2,
            shipping_city=address.city,
            shipping_state=address.state,
            shipping_postal_code=address.postal_code,
            shipping_country=address.country,
            subtotal=subtotal,
            tax=tax,
            shipping_cost=shipping_cost,
            total=total,
            payment_status='paid',  # Mock payment - always succeeds
            status='processing',
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                product_price=cart_item.product.price,
                quantity=cart_item.quantity,
                subtotal=cart_item.get_subtotal(),
            )
            
            # Update product stock
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()
        
        # Clear cart
        cart_items.delete()
        
        messages.success(request, f'Order placed successfully! Order number: {order_number}')
        return redirect('orders:order_confirmation', order_number=order_number)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'addresses': addresses,
        'subtotal': subtotal,
        'tax': tax,
        'shipping_cost': shipping_cost,
        'total': total,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_confirmation(request, order_number):
    """Order confirmation page after successful checkout"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_confirmation.html', {'order': order})


@login_required
def order_history(request):
    """List all orders for the current user"""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_number):
    """Order detail page with invoice"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def invoice(request, order_number):
    """Invoice view for printing/downloading"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/invoice.html', {'order': order})

