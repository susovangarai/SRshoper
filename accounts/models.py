from django.db import models
from django.contrib.auth.models import User

from products.models import Product


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    transaction_id = models.CharField(max_length=255, null=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, blank=True)
    created = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([items.get_total for items in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([items.quantity for items in order_items])
        return total

    @property
    def shipping(self):
        shipping = False
        for i in self.orderitem_set.all():
            if not i.product.digital:
                return True
        return shipping


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.title

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=255, null=False)
    state = models.CharField(max_length=255, null=False)
    zipcode = models.CharField(max_length=255, null=False)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str("{} {} {} {}".format(self.address, self.city, self.state, self.zipcode))
