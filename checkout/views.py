import datetime
import json
from decimal import Decimal

from django.http import JsonResponse
from django.shortcuts import render, redirect

from accounts.models import Order, ShippingAddress


def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items': 0,
                 'get_cart_total': 0,
                 'shipping': False}
    context = {'items': items, 'order': order, }
    if order.get_cart_items:
        return render(request, 'checkout/summary.html', context)
    return redirect('cart:home')


def payment_process(request):
    print('Data: ', request.body)
    data = json.loads(request.body)
    transaction_id = "TXN" + "".join(datetime.datetime.now().strftime("%w%d%m%Y%H%M%S%f"))
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # form_total = data['form']['total']
        total = Decimal(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zip'],
            )

    return JsonResponse("Payment initiated and order is under process", safe=False)
