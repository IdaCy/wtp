from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        else:
            for error in form.errors:
                messages.error(request, form.errors[error])
    else:
        form = UserCreationForm()
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
                print("Successful login for user:", username)  # Add this line for debugging
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
            else:
                print("Invalid username or password")  # Add this line for debugging
                messages.error(request, 'Invalid username or password.')
        else:
            print("Form is not valid:", form.errors)  # Add this line for debugging
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
