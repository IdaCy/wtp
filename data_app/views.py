from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import DataCR, PubType, PubTitle, Language, Reference, Habitat, SpeciesName
from .models import RAP, Lifestage, StudyType, ActivityConcUnit, Media
from .forms import DataCRForm


from django.http import JsonResponse
from django.views import View


@login_required
def data_view(request):
    dataobj = ActivityConcUnit.objects.all()
    return render(request, 'data.html', {'data': dataobj})


@login_required
def ref_view(request):
    refobj = Reference.objects.all()
    return render(request, 'reference.html', {'reference': refobj})


@login_required
def add_datacr(request):
    # Handle form submission
    if request.method == 'POST':
        form = DataCRForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Redirect to the data view or any other desired page
            return redirect('data_view')
    else:
        # Render the form for GET requests
        form = DataCRForm()

    return render(request, 'add_datacr.html', {
        'form': form,
        'pub_types': PubType.objects.all(),
        'pub_titles': PubTitle.objects.all(),
        'languages': Language.objects.all(),
        'article_title': Reference.objects.all(),
        'habitat_specific_type': Habitat.objects.all(),
        'rap_name': RAP.objects.all(),
        'lifestage_name': Habitat.objects.all(),
        'study_type_name': Habitat.objects.all(),
        'name_common': SpeciesName.objects.all(),
        #'name_latin': SpeciesName.objects.all(),
        #'radionuclide_name': SpeciesName.objects.all(),
        #'wildlife_group_name': SpeciesName.objects.all(),
    })


class GetCorrectionFactorView(View):
    def get(self, request, *args, **kwargs):
        unit_symbol = request.GET.get('unit_symbol', '')
        media_type_string = request.GET.get('media_type', '')

        print("Unit Symbol:", unit_symbol)
        print("Media Type:", media_type_string)

        try:
            # Get the first Media object based on the selected media type name
            media_obj = Media.objects.filter(media_type=media_type_string).first()

            if media_obj:
                # Get the correction factor based on both unit symbol and media type
                correction_factor_entry = ActivityConcUnit.objects.filter(
                    act_conc_unit_symbol=unit_symbol,
                    media=media_obj
                ).first()

                if correction_factor_entry:
                    correction_factor = correction_factor_entry.correction_factor_act_conc
                    return JsonResponse({'correction_factor': correction_factor})
                else:
                    return JsonResponse({'error': 'Unit not found for the given media type'}, status=404)
            else:
                return JsonResponse({'error': 'Media not found'}, status=404)

        except Media.DoesNotExist:
            return JsonResponse({'error': 'Media not found'}, status=404)

