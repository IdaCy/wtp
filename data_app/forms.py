from django import forms
from .models import DataCR, Reference, PubType, PubTitle, Language, Habitat, SpeciesName
from .models import RAP, Lifestage, StudyType, Radionuclide, WildlifeGroup, Tissue, Media
from .attribute_choices import units, wet_dry_choices


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

    class Meta:
        model = Reference
        fields = ['ref_id', 'author', 'article_title', 'pub_title', 'year', 'volume', 'part', 'pages', 'language',
                  'pub_type', 'translation', 'notes']

        distinct_article_title = Reference.objects.order_by('article_title').values_list('article_title',
                                                                                         flat=True).distinct()

    def __init__(self, *args, **kwargs):
        super(ReferenceForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name not in ['ref_id']:
                field.required = False


class DataCRForm(forms.ModelForm):
    stand_media_conc = forms.FloatField(
        required=False, widget=forms.HiddenInput()
    )
    stand_biota_conc = forms.FloatField(
        required=False, widget=forms.HiddenInput()
    )

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
    media_wet_dry = forms.ChoiceField(
        choices=wet_dry_choices,
        required=False,
        label='Media Wet/Dry'
    )
    biota_wet_dry = forms.ChoiceField(
        choices=wet_dry_choices,
        required=False,
        label='Biota Wet/Dry',
    )
    biota_conc_units = forms.ChoiceField(
        choices=units,
        label='Units'
    )

    class Meta:
        model = DataCR
        fields = '__all__'
        exclude = ['reference']  # Exclude reference as it will be handled separately

    def clean(self):
        cleaned_data = super().clean()
        stand_media_conc = cleaned_data.get('stand_media_conc')
        stand_biota_conc = cleaned_data.get('stand_biota_conc')

        try:
            if stand_media_conc is not None:
                cleaned_data['stand_media_conc'] = float(stand_media_conc)
            if stand_biota_conc is not None:
                cleaned_data['stand_biota_conc'] = float(stand_biota_conc)
        except (ValueError, TypeError):
            cleaned_data['stand_media_conc'] = None
            cleaned_data['stand_biota_conc'] = None

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['habitat'].required = True
        self.fields['cr_n'].required = True
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
            if name not in ['cr', 'cr_n', 'habitat']:
                field.required = False
