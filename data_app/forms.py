from django import forms
from django.forms import ModelChoiceField
from .models import DataCR, Reference, PubType, PubTitle, Language, Habitat, SpeciesName
from .models import RAP, Lifestage, StudyType, Radionuclide, WildlifeGroup, Tissue, Media


class ReferenceForm(forms.ModelForm):
    ref_id = forms.IntegerField(required=True)
    article_title = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'article-title-search', 'autocomplete': 'off'})
    )
    pub_title = forms.ModelChoiceField(
        queryset=PubTitle.objects.all().order_by('pub_title_name'),
        required=False,
        label='Publication Title',
        empty_label="Select Title"
    )
    pub_type = forms.ModelChoiceField(
        queryset=PubType.objects.all().order_by('pub_type_name'),
        required=False,
        label='Publication Type',
        empty_label="Select"
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all().order_by('language'),
        required=False,
        label='Language',
        empty_label="Select"
    )

    translation = forms.BooleanField(
        required=False,
        label='English Translation Available'
    )

    """article_title = forms.ModelChoiceField(
        queryset=Reference.objects.all().order_by('article_title'),
        required=False,
        label='Article Title',
        empty_label="Select Article Title"
    )"""
    #translation = forms.BooleanField(required=False)

    class Meta:
        model = Reference
        fields = ['ref_id', 'author', 'article_title', 'pub_title', 'year', 'volume', 'part', 'pages', 'language',
                  'pub_type', 'translation', 'notes']

        # Set distinct article title
        distinct_article_title = Reference.objects.order_by('article_title').values_list('article_title',
                                                                                         flat=True).distinct()

    def __init__(self, *args, **kwargs):
        super(ReferenceForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name not in ['ref_id']:
                field.required = False


class DataCRForm(forms.ModelForm):
    species_name = forms.ModelChoiceField(
        queryset=SpeciesName.objects.all(),
        label='Species',
        empty_label="Please Select",
        required=False
    )

    lifestage = forms.ModelChoiceField(
        queryset=Lifestage.objects.all().order_by('lifestage_name').distinct('lifestage_name'),
        required=False,
        label='Lifestage',
        empty_label="Select Lifestage"
    )
    wildlife_group = forms.ModelChoiceField(
        queryset=WildlifeGroup.objects.all(),
        required=False,
        label='Wildlife Group',
        empty_label="Select Wildlife Group"
    )
    icrp_rap = forms.ModelChoiceField(
        queryset=RAP.objects.all(),
        required=False,
        label='ICRP RAP',
        empty_label="Select ICRP RAP"
    )
    media = forms.ModelChoiceField(
        queryset=Media.objects.all(),
        required=False,
        label='Media',
        empty_label="Select Media"
    )
    tissue = forms.ModelChoiceField(
        queryset=Tissue.objects.all(),
        required=False,
        label='Tissue',
        empty_label="Select"
    )
    study_type = forms.ModelChoiceField(
        queryset=StudyType.objects.all(),
        required=False,
        label='Studytype',
        empty_label="Select"
    )
    radionuclide = forms.ModelChoiceField(
        queryset=Radionuclide.objects.all(),
        required=False,
        label='Radionuclide',
        empty_label=""
    )
    measurement_date = forms.DateField(
        required=False,
        label='Measured',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Notes...'}),
        label='Notes'
    )
    media_wet_dry_choices = [
        ('Wet', 'Wet'),
        ('Dry', 'Dry')
    ]
    media_wet_dry = forms.ChoiceField(
        choices=media_wet_dry_choices,
        required=False,
        label='Media Wet/Dry'
    )
    biota_wet_dry_choices = [
        ('Wet', 'Wet'),
        ('Dry', 'Dry'),
        ('Ash', 'Ash')
    ]
    biota_wet_dry = forms.ChoiceField(
        choices=biota_wet_dry_choices,
        required=False,
        label='Biota Wet/Dry',
    )
    biota_conc_units_choices = [
        ('µCi/kg', 'µCi/kg'),
        ('Bq/l', 'Bq/l'),
        ('Bq/g', 'Bq/g'),
        ('Bq/kg', 'Bq/kg'),
        ('Bq/m2', 'Bq/m2'),
        ('mBq/g', 'mBq/g'),
        ('mBq/kg', 'mBq/kg'),
        ('mg/g', 'mg/g'),
        ('mg/kg', 'mg/kg'),
        ('pCi/g', 'pCi/g'),
        ('pCi/kg', 'pCi/kg'),
        ('ppb', 'ppb'),
        ('ppm', 'ppm'),
        ('ug/g', 'ug/g'),
        ('ug/kg', 'ug/kg')
    ]
    biota_conc_units = forms.ChoiceField(
        choices=biota_conc_units_choices,
        label='Units'
    )

    class Meta:
        model = DataCR
        exclude = ['reference']  # Exclude reference as it will be handled separately

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['habitat'].required = True
        self.fields['crn'].required = True
        # self.fields['species_name'].required = False
        self.fields['habitat'].queryset = Habitat.objects.all()
        self.fields['study_type'].queryset = StudyType.objects.all()
        self.fields['radionuclide'].queryset = Radionuclide.objects.all()
        self.fields['tissue'].queryset = Tissue.objects.all()
        self.fields['media'].queryset = Media.objects.all()

        if not self.initial.get('habitat'):
            default_habitat = Habitat.objects.first()
            if default_habitat:
                self.fields['habitat'].initial = default_habitat.pk

        # Modify the choices for wildlife_group, icrp_rap, and lifestage
        self.fields['wildlife_group'].choices = [(wg.wildlife_group_id, wg.wildlife_group_name) for wg in
                                                 WildlifeGroup.objects.all().order_by('wildlife_group_name').distinct(
                                                     'wildlife_group_name')]
        self.fields['icrp_rap'].choices = [(rap.rap_id, rap.rap_name) for rap in
                                           RAP.objects.all().order_by('rap_name').distinct('rap_name')]
        self.fields['lifestage'].choices = [(ls.lifestage_id, ls.lifestage_name) for ls in
                                            Lifestage.objects.all().order_by('lifestage_name').distinct(
                                                'lifestage_name')]

        for name, field in self.fields.items():
            if name not in ['cr', 'crn', 'habitat']:
                field.required = False

    """def clean_species_name(self):
        data = self.cleaned_data['species_name']
        # Explicitly allow None or empty string as valid values
        if data == "" or str(data).lower() == "none":
            return None
        return data"""
