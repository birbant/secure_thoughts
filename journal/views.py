from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, ThoughtForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import Thought


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
        form = LoginForm(request, data=request.POST)
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


@login_required(login_url='my-login')
def create_thought(request):
    form = ThoughtForm(request)
    if request.method == 'POST':
        form = ThoughtForm(request.POST)
        if form.is_valid():
            thought = form.save(commit=False)
            thought.user = request.user
            thought.save()
            return redirect('my-thoughts')
    else:
        form = ThoughtForm()
    context = {'CreateThoughtForm': form}
    return render(request, 'create-thought.html', context)


@login_required(login_url='my-login')
def my_thoughts(request):

    current_user = request.user.id
    thought = Thought.objects.all().filter(user=current_user)
    context = {'Allthoughts': thought}

    return render(request, 'my-thoughts.html', context)


@login_required(login_url='my-login')
def update_thought(request, pk):
    try:
        thought = Thought.objects.get(id=pk, user=request.user)
    except:
        return redirect('my-thoughts')

    form = ThoughtForm(instance=thought)
    if request.method == 'POST':
        form = ThoughtForm(request.POST, instance=thought)
        if form.is_valid():
            form.save()
            return redirect('my-thoughts')
    context = {'UpdateThought': form}

    return render(request, 'update-thought.html', context)


@login_required(login_url='my-login')
def delete_thought(request, pk):
    try:
        thought = Thought.objects.get(id=pk, user=request.user)
    except:
        return redirect('my-thoughts')

    if request.method == 'POST':
        thought.delete()
        return redirect('my-thoughts')

    return render(request, 'delete-thought.html')


@login_required(login_url='my-login')
def profile_management(request):
    pass