from django.urls import path
from checkout import views

app_name = 'checkout'

urlpatterns = [
    path('', views.home, name='summary'),
    path('payment/', views.payment_process, name='payment')
]
