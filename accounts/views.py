from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from .forms import LoginForm


def login_page(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if login_form.is_valid():
            if user is not None:
                login(request, user)
            return redirect('products:all_products')
    else:
        login_form = LoginForm()
    return render(request, 'accounts/auth/login.html', {"form": login_form})


def logout_view(request):
    logout(request)
    return redirect('products:all_products')
