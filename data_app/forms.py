from django import forms
from .models import DataCR, PubType, PubTitle, Language, Reference, Habitat, SpeciesName
from .models import RAP, Lifestage, StudyType, Radionuclide, WildlifeGroup, Tissue

class DataCRForm(forms.ModelForm):
    class Meta:
        model = DataCR
        fields = '__all__'

    publication_type = forms.ModelChoiceField(queryset=PubType.objects.all(), to_field_name='pub_type_name')
    publication_title = forms.ModelChoiceField(queryset=PubTitle.objects.all(), to_field_name='pub_title_name')
    reference_language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name='language')
    ref_article_title = forms.ModelChoiceField(queryset=Reference.objects.all(), to_field_name='article_title')
    habitat_specific_type = forms.ModelChoiceField(queryset=Habitat.objects.all(), to_field_name='habitat_specific_type')
    rap_name = forms.ModelChoiceField(queryset=RAP.objects.all(), to_field_name='rap_name')
    lifestage_name = forms.ModelChoiceField(queryset=Lifestage.objects.all(), to_field_name='lifestage_name')
    study_type_name = forms.ModelChoiceField(queryset=StudyType.objects.all(), to_field_name='study_type_name')
    radionuclide_name = forms.ModelChoiceField(queryset=Radionuclide.objects.all(), to_field_name='radionuclide_name')
    wildlife_group_name = forms.ModelChoiceField(queryset=WildlifeGroup.objects.all(), to_field_name='wildlife_group_name')
    tissue_name = forms.ModelChoiceField(queryset=Tissue.objects.all(), to_field_name='tissue_name')
    name_common = forms.CharField(widget=forms.Select(attrs={'class': 'limited'}))
    name_latin = forms.CharField(widget=forms.Select(attrs={'class': 'limited'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Separate querysets for common names and Latin names
        common_names = SpeciesName.objects.values_list('name_common', flat=True).distinct()
        latin_names = SpeciesName.objects.values_list('name_latin', flat=True).distinct()

        # Update the choices for each dropdown
        self.fields['name_common'].widget.choices = [(name, name) for name in common_names]
        self.fields['name_latin'].widget.choices = [(name, name) for name in latin_names]
