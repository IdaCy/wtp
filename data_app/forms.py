from django import forms
from .models import DataCR, PubType, PubTitle, Language

class DataCRForm(forms.ModelForm):
    class Meta:
        model = DataCR
        fields = '__all__'

    publication_type = forms.ModelChoiceField(queryset=PubType.objects.all(), to_field_name='pub_type_name')
    publication_title = forms.ModelChoiceField(queryset=PubTitle.objects.all(), to_field_name='pub_title_name')
    reference_language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name='language')
