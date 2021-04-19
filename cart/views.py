import json
from django.http import JsonResponse
from django.shortcuts import render
from products.models import Product
from accounts.models import Order, OrderItem


def home(request):
    items = Order.objects.none()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        order = {'get_cart_items': 0,
                 'get_cart_total': 0,
                 'shipping': False}
    context = {'items': items,
               'order': order, }
    return render(request, 'cart/cart.html', context)


def update(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1
    order_item.save()

    if order_item.quantity <= 0 or action == 'delete':
        order_item.delete()
    return JsonResponse('Item was added', safe=False)
