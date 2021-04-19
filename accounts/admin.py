from django.contrib import admin

# Register your models here.
from accounts.models import *

admin.site.register(Customer)
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
