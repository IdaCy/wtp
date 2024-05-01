from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from django import forms
from django.contrib.auth.forms import UserChangeForm
from data_app.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "salutation", "first_name", "last_name", "job_title", "organisation")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]  # Set username to email
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(required=True, label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise ValidationError("Invalid email or password.")
            self.cleaned_data['user'] = user
        return self.cleaned_data

    def get_user(self):
        return self.cleaned_data.get('user')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'salutation', 'job_title', 'organisation', 'admin_priv', 'is_active', 'is_staff')
