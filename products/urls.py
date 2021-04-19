from django.urls import path, include
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='all_products'),
    path('add/', views.product_data, name='add_product'),
    path('details/<slug>', views.ProductDetailView.as_view(), name='detail'),
    path('update/<int:item_id>/', views.product_data, name='update'),
    path('delete/<int:item_id>/', views.product_delete, name='delete'),
]
