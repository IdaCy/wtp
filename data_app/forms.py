from django import forms
from django.forms import ModelChoiceField
from .models import DataCR, Reference, PubType, PubTitle, Language, Habitat, SpeciesName
from .models import RAP, Lifestage, StudyType, Radionuclide, WildlifeGroup, Tissue, Media

class ReferenceForm(forms.ModelForm):
    ref_id = forms.IntegerField(required=True)

    article_title = forms.ModelChoiceField(
        queryset=Reference.objects.all().order_by('article_title'),
        required=False,
        label='Article Title'
    )

    class Meta:
        model = Reference
        fields = ['ref_id', 'author', 'article_title', 'pub_title', 'year', 'volume', 'part', 'pages', 'language', 'pub_type', 'translation', 'notes']

        # Set distinct article title
        distinct_article_title = Reference.objects.order_by('article_title').values_list('article_title', flat=True).distinct()


class DataCRForm(forms.ModelForm):
    species_name = forms.ModelChoiceField(
        queryset=SpeciesName.objects.all(),
        label='Species',
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

    class Meta:
        model = DataCR
        exclude = ['reference']  # Exclude reference as it will be handled separately

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['habitat'].queryset = Habitat.objects.all()
        #self.fields['icrp_rap'].queryset = RAP.objects.all()
        self.fields['study_type'].queryset = StudyType.objects.all()
        self.fields['radionuclide'].queryset = Radionuclide.objects.all()
        self.fields['tissue'].queryset = Tissue.objects.all()
        self.fields['media'].queryset = Media.objects.all()

        # Modify the choices for wildlife_group, icrp_rap, and lifestage
        self.fields['wildlife_group'].choices = [(wg.wildlife_group_id, wg.wildlife_group_name) for wg in WildlifeGroup.objects.all().order_by('wildlife_group_name').distinct('wildlife_group_name')]
        self.fields['icrp_rap'].choices = [(rap.rap_id, rap.rap_name) for rap in RAP.objects.all().order_by('rap_name').distinct('rap_name')]
        self.fields['lifestage'].choices = [(ls.lifestage_id, ls.lifestage_name) for ls in Lifestage.objects.all().order_by('lifestage_name').distinct('lifestage_name')]
        #self.fields['media'].choices = [(md.media_id, md.media_type) for md in Media.objects.all().order_by('media_id').distinct('media_id')]

        # Set distinct lifestages
        #distinct_lifestages = Lifestage.objects.order_by('lifestage_name').values_list('lifestage_name', flat=True).distinct()
        #self.fields['lifestage'].choices = [(name, name) for name in distinct_lifestages]

        # Set distinct wildlife group
        #distinct_wildlife_group = WildlifeGroup.objects.order_by('wildlife_group_name').values_list('wildlife_group_name', flat=True).distinct()
        #self.fields['wildlife_group'].choices = [(name, name) for name in distinct_wildlife_group]

        # Set distinct rap
        #distinct_rap = RAP.objects.order_by('rap_name').values_list('rap_name', flat=True).distinct()
        #self.fields['icrp_rap'].choices = [(name, name) for name in distinct_rap]
