from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.home, name='home'),
    path('update/', views.update, name='update'),
]
