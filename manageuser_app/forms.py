from django import forms
from django.contrib.auth.forms import UserCreationForm
from data_app.models import User  # Assuming your User model is in the same app

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            'salutation',
            'firstname',
            'lastname',
            'email',
            'jobtitle',
            'company',
        )
