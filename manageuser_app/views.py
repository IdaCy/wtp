from django.contrib import messages
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.shortcuts import render, redirect


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Additional fields from custom User model
            user.salutation = request.POST.get('salutation')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.jobtitle = request.POST.get('jobtitle')
            user.company = request.POST.get('organisation')
            user.admin_priv = request.POST.get('admin_priv')

            user.save()

            messages.success(request, f'Account created for {user.first_name} {user.last_name}!')
            return redirect('login')
        else:
            for error in form.errors:
                messages.error(request, form.errors[error])
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                print("Successful login for user:", user.email)
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                return redirect('dashboard')
            else:
                print("Invalid email or password")
                messages.error(request, 'Invalid email or password.')
        else:
            print("Form is not valid:", form.errors)
            for error in form.errors:
                messages.error(request, form.errors[error])
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')
