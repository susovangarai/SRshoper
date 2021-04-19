from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from .forms import ProductForm
from .models import Product


def index(request):
    return render(request, 'products/index.html')


class ProductListView(ListView):
    model = Product
    template_name = 'products/products/all_products.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/products/detail.html'


def product_data(request, item_id=0):
    if request.user.has_perm('products.add_product') or request.user.has_perm('products.change_product'):
        if request.method == 'GET':
            if item_id == 0:
                product_form = ProductForm()
            else:
                item = get_object_or_404(Product, pk=item_id)
                product_form = ProductForm(instance=item)
            return render(request, 'products/products/add_product.html', {'form': product_form})
        else:
            if item_id == 0:
                product_form = ProductForm(request.POST, request.FILES)
            else:
                item = Product.objects.get(pk=item_id)
                product_form = ProductForm(request.POST or None, request.FILES or None, instance=item)
            if product_form.is_valid():
                product_form.save()
    return redirect('products:all_products')


def product_delete(request, item_id):
    if request.user.has_perm('products.delete_product'):
        item = get_object_or_404(Product, pk=item_id)
        item.delete()
    return redirect('products:all_products')
