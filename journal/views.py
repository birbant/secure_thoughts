from django.shortcuts import render


def homepage(request):
    return render(request, 'homepage.html')


def register(request):
    return render(request, 'register.html')


def my_login(request):
    return render(request, 'my-login.html')


def dashboard(request):
    return render(request, 'dashboard.html')