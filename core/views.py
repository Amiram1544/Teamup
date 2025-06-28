from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import UserForm
from core.models import Topics

# Create your views here.


def home(request):
    
    topics = Topics.objects.all()
    
    context = {
        'topics' : topics,
    }
    return render(request, 'core/index.html', context)

def loginpage(request):
    
    if request.user.is_authenticated:
        return redirect('home')
    
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
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
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.set_password(form.cleaned_data['password1'])
            user.save()
            
            authenticated_user = authenticate(request, username= user.username, password= form.cleaned_data['password1'])
            
            if authenticated_user is not None:        
                login(request, authenticated_user)
                return redirect('home')
        else:
            messages.error(request, 'Error during registration, please try again')
    
    context = {
        'page': page,
        'form': form,
    }
    
    return render(request, 'core/login_register.html', context)    

def logoutpage(request):
    logout(request)
    return redirect('home')

def profile(request):
    
    if request.user.is_authenticated:
        context = {
            'user': request.user
        }
    else:
        messages.warning(request, "Please Login to view your profile first.")
        return redirect('login')
    
    return render(request, 'core/profile.html', context)     

@login_required(login_url='login')
def edit_profile(request):

    user = request.user
    form = UserCreationForm(request.POST)
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated succesfully')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating your profile, please try again')
    
    if not request.user.is_authenticated:
        messages.warning(request, 'Please Login first to edit your profile')
        return redirect('login')
    
    context = {
        'form': form,
    }
    
    return render(request, 'core/edit_profile.html', context)
    
    