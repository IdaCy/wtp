from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from data_app.models import User

from data_app.models import User


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # Use password1 to get the password
            # Create a new User instance
            user = User.objects.create(username=username, password=password)

            # Additional fields from your custom User model
            user.salutation = request.POST.get('salutation')
            user.firstname = request.POST.get('firstname')
            user.lastname = request.POST.get('lastname')
            user.email = request.POST.get('email')
            user.jobtitle = request.POST.get('jobtitle')
            user.company = request.POST.get('company')
            user.admin_priv = request.POST.get('admin_priv')

            user.save()

            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        else:
            for error in form.errors:
                messages.error(request, form.errors[error])
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print("Successful login for user:", username)  # for debugging
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
            else:
                print("Invalid username or password")  # for debugging
                messages.error(request, 'Invalid username or password.')
        else:
            print("Form is not valid:", form.errors)  # for debugging
            for error in form.errors:
                messages.error(request, form.errors[error])
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


def privacy_view(request):
    return render(request, 'privacy.html')


def legal_view(request):
    return render(request, 'legal.html')
