from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from .forms import SignUpForm, LoginForm

# Create your views here.
def signup(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def log_in(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:  # If the returned object is not None
                login(request, user)  #connect the user
                return redirect('core:home')
            else:  # otherwise an error will be displayed
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect(reverse('users:login'))
