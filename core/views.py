from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.


def home(request):
    return render(request, 'core/index.html')

def loginpage(request):
    
    if request.user.is_authenticated:
        return redirect('home')
    
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, usename=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            
    context = {
        'page': page,
    }        
    return render(request, 'core/login_register.html', context)

def registerpage(request):
    
    if request.user.is_authenticated:
        return redirect('home')
    
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error during registration, please try again')
    
    context = {
        'page': page,
        'form': form,
    }
    
    return render(request, 'core/login_register.html', context)         