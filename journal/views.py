from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def homepage(request):
    return render(request, 'homepage.html')


def register(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your secure account has been created!')
            return redirect('my-login')

    context = {'form': form}
    return render(request, 'register.html', context=context)


def my_login(request):

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
    context = {'form': form}

    return render(request, 'my-login.html', context)


@login_required(login_url='my-login')
def dashboard(request):
    return render(request, 'dashboard.html')


def user_logout(request):
    auth.logout(request)
    return redirect('homepage')
