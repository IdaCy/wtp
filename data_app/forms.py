from django import forms
from django.forms import ModelChoiceField
from .models import DataCR, Reference, PubType, PubTitle, Language, Habitat, SpeciesName
from .models import RAP, Lifestage, StudyType, Radionuclide, WildlifeGroup, Tissue, Media


class ReferenceForm(forms.ModelForm):
    ref_id = forms.IntegerField(required=True)
    article_title = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'article-title-search', 'autocomplete': 'off'}))

    """article_title = forms.ModelChoiceField(
        queryset=Reference.objects.all().order_by('article_title'),
        required=False,
        label='Article Title',
        empty_label="Select Article Title"
    )"""
    translation = forms.BooleanField(required=False)

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
    species_list = forms.ModelChoiceField(
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
    media_wet_dry = forms.ChoiceField(
        choices=DataCR.media_wet_dry_choices,
        required=False,
        label='Media Wet/Dry'
    )

    class Meta:
        model = DataCR
        exclude = ['reference']  # Exclude reference as it will be handled separately

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['habitat'].required = True
        self.fields['crn'].required = True
        self.fields['habitat'].queryset = Habitat.objects.all()
        self.fields['study_type'].queryset = StudyType.objects.all()
        self.fields['radionuclide'].queryset = Radionuclide.objects.all()
        self.fields['tissue'].queryset = Tissue.objects.all()
        self.fields['media'].queryset = Media.objects.all()

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
