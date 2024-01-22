from django import forms
from .models import DataCR, PubType, PubTitle, Language, Reference, Habitat, SpeciesName
from .models import RAP, Lifestage, StudyType, Radionuclide, WildlifeGroup, Tissue

class DataCRForm(forms.ModelForm):
    # for reference
    reference_id = forms.IntegerField()
    author = forms.CharField(max_length=500)
    ref_article_title = forms.CharField(max_length=500)
    year = forms.CharField(max_length=30)
    volume = forms.CharField(max_length=50)
    part = forms.CharField(max_length=50)
    page_numbers = forms.CharField(max_length=50)
    translation_available = forms.BooleanField(required=False)
    notes = forms.CharField(max_length=500, required=False)

    # for datacr
    cr_id = forms.DecimalField(max_digits=25, decimal_places=10)
    measurement_date = forms.DateField()
    n_of_cr = forms.IntegerField()
    concentration_ratio = forms.IntegerField()
    sd_of_cr = forms.DecimalField(max_digits=25, decimal_places=10)
    biota_conc = forms.CharField(max_length=30)
    biota_conc_units = forms.CharField(max_length=20)
    biota_n = forms.IntegerField()
    biota_sd = forms.CharField(max_length=30)
    biota_wet_dry = forms.CharField(max_length=20)
    media_type = forms.CharField(max_length=50)
    media_conc = forms.CharField(max_length=30)
    media_n = forms.CharField(max_length=30)
    media_conc_units = forms.CharField(max_length=20)
    media_sd = forms.CharField(max_length=30)
    media_wet_dry = forms.CharField(max_length=5)


    class Meta:
        model = DataCR
        fields = '__all__'

    publication_type = forms.ModelChoiceField(queryset=PubType.objects.all(), to_field_name='pub_type_name')
    publication_title = forms.ModelChoiceField(queryset=PubTitle.objects.all(), to_field_name='pub_title_name')
    reference_language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name='language')
    ref_article_title = forms.ModelChoiceField(queryset=Reference.objects.all(), to_field_name='article_title')
    habitat_specific_type = forms.ModelChoiceField(queryset=Habitat.objects.all(), to_field_name='habitat_specific_type')
    #icrp_rap = forms.ModelChoiceField(queryset=RAP.objects.all(), to_field_name='rap_name')
    #lifestage_name = forms.ModelChoiceField(queryset=Lifestage.objects.all(), to_field_name='lifestage_name')
    study_type_name = forms.ModelChoiceField(queryset=StudyType.objects.all(), to_field_name='study_type_name')
    radionuclide_name = forms.ModelChoiceField(queryset=Radionuclide.objects.all(), to_field_name='radionuclide_name')
    #wildlife_group_name = forms.ModelChoiceField(queryset=WildlifeGroup.objects.all(), to_field_name='wildlife_group_name')
    tissue_name = forms.ModelChoiceField(queryset=Tissue.objects.all(), to_field_name='tissue_name')
    name_common = forms.CharField(widget=forms.Select(attrs={'class': 'limited'}))
    name_latin = forms.CharField(widget=forms.Select(attrs={'class': 'limited'}))

    icrp_rap = forms.ModelChoiceField(
        queryset=RAP.objects.order_by('rap_name').distinct('rap_name'),
        to_field_name='rap_name'
    )
    lifestage_name = forms.ModelChoiceField(
        queryset=Lifestage.objects.order_by('lifestage_name').distinct('lifestage_name'),
        to_field_name='lifestage_name'
    )
    wildlife_group_name = forms.ModelChoiceField(
        queryset=WildlifeGroup.objects.order_by('wildlife_group_name').distinct('wildlife_group_name'),
        to_field_name='wildlife_group_name'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Separate querysets for common names and Latin names
        common_names = SpeciesName.objects.values_list('name_common', flat=True).distinct()
        latin_names = SpeciesName.objects.values_list('name_latin', flat=True).distinct()

        # Update the choices for each dropdown
        self.fields['name_common'].widget.choices = [(name, name) for name in common_names]
        self.fields['name_latin'].widget.choices = [(name, name) for name in latin_names]
