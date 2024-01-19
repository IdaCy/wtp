from django import forms
from .models import DataCR

class DataCRForm(forms.ModelForm):
    class Meta:
        model = DataCR
        fields = '__all__'

