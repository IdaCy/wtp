from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import DataCR, PubType, PubTitle, Language, Reference, Habitat, SpeciesName
from .models import RAP, Lifestage, StudyType, ActivityConcUnit, Media, WildlifeGroup, Element, Radionuclide, Tissue
from .forms import DataCRForm, ReferenceForm

from django.http import JsonResponse
from django.db.models import Sum, F

from django.http import JsonResponse
from django.views import View

from django.db.models import Avg, F
from django.db.models.functions import StringAgg
from django.db.models import Avg, F
from django.db.models.functions import Concat
#from django.db.models import Avg, StringAgg
#from django.db.models.functions import Str
#from django.db.models.functions import StringAgg
#from django.db.models.aggregates import StringAgg

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages


@login_required
def data_view(request):
    dataobj = ActivityConcUnit.objects.all()
    return render(request, 'data.html', {'data': dataobj})

@login_required
def download_summaries(request):
    return render(request, 'download_summaries.html')


@login_required
def view_summary_results(request):
    habitat_query = request.GET.get('habitat')  # This will capture the selected habitat from the request

    # Initialize the context with an empty list; it will hold our filtered data
    context = {'datacr_list': []}

    # Check if there's a habitat query
    if habitat_query in ['Freshwater', 'Marine', 'Terrestrial']:
        datacr_list = DataCR.objects.filter(
            habitat__habitat_specific_type=habitat_query
        ).select_related('habitat').values(
            'radionuclide__element__element_symbol', 'cr', 'reference'
        )
        context['datacr_list'] = datacr_list

    return render(request, 'view_summary_results.html', context)


@login_required
def view_xxx(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Extract query parameters from AJAX request
        habitat = request.GET.get('habitat')
        choice = request.GET.get('choice')
        additional_choice = request.GET.get('additionalChoice')
        media_type = request.GET.get('mediaType')

        # Perform database query and aggregation
        query_result = DataCR.objects.filter(
            habitat__habitat_specific_type=habitat,
            # ...
            media__media_type=media_type
        ).values(
            'element__element_symbol'
        ).annotate(
            arithmetic_mean=Sum('cr'),
            arithmetic_std_dev=Sum('cr'),
            geometric_std_dev=Sum('cr'),
            n=Sum('crn'),
            ref_id=Sum(F('reference__ref_id'))
        )

        # Convert to list of dicts
        data_list = list(query_result)

        # Return as JSON
        return JsonResponse(data_list, safe=False)

    # For non-AJAX requests, just render the template with no data
    return render(request, 'view_summary_results.html', {'data': []})


@login_required
def ref_view(request):
    refobj = Reference.objects.all()
    return render(request, 'reference.html', {'reference': refobj})


@login_required
def add_datacr(request):
    if request.method == 'POST':
        print("POST Data:", request.POST)
        reference_form = ReferenceForm(request.POST)
        datacr_form = DataCRForm(request.POST)

        if reference_form.is_valid() and datacr_form.is_valid():
            ref_id = reference_form.cleaned_data['ref_id']

            # Check if a Reference with this ref_id already exists
            reference, created = Reference.objects.get_or_create(
                ref_id=ref_id,
                defaults={**reference_form.cleaned_data, 'user': request.user}
            )

            messages.success(request, "Successfully saved. Thank you for your submission!")

            # If the reference was not created (already exists), update its fields
            if not created:
                for field, value in reference_form.cleaned_data.items():
                    setattr(reference, field, value)
                reference.save()

            # Save DataCR instance
            datacr = datacr_form.save(commit=False)
            datacr.reference = reference

            # Fetching the actual model instances
            wildlife_group_id = datacr_form.cleaned_data.get('wildlife_group').wildlife_group_id if datacr_form.cleaned_data.get(
                'wildlife_group') else None
            icrp_rap_id = datacr_form.cleaned_data.get('icrp_rap').rap_id if datacr_form.cleaned_data.get(
                'icrp_rap') else None
            lifestage_id = datacr_form.cleaned_data.get('lifestage').lifestage_id if datacr_form.cleaned_data.get(
                'lifestage') else None
            media_id = datacr_form.cleaned_data.get('media').media_id if datacr_form.cleaned_data.get(
                'media') else None

            if wildlife_group_id:
                datacr.wildlife_group = WildlifeGroup.objects.get(pk=wildlife_group_id)

            if icrp_rap_id:
                datacr.icrp_rap = RAP.objects.get(pk=icrp_rap_id)

            if lifestage_id:
                datacr.lifestage = Lifestage.objects.get(pk=lifestage_id)

            if media_id:
                datacr.media = Media.objects.get(pk=media_id)

            #media_id = request.POST.get('media')
            #if media_id:
            #    datacr.media = Media.objects.get(pk=media_id)

            # from invisible in-between calculation field
            #datacr.biota_n = request.POST.get('biota_n', 0)

            datacr.media_wet_dry = datacr_form.cleaned_data['media_wet_dry']

            datacr.save()

            #return redirect('dashboard')
        else:
            # Handling form errors
            print(reference_form.errors, datacr_form.errors)
            messages.error(request, "There was a problem with your submission. Please try again or contact us.")
            return render(request, 'add_datacr.html', {'reference_form': reference_form, 'datacr_form': datacr_form})
    else:
        reference_form = ReferenceForm()
        datacr_form = DataCRForm()

    return render(request, 'add_datacr.html', {'reference_form': reference_form, 'datacr_form': datacr_form})


@login_required
def get_media_for_habitat(request):
    habitat_id = request.GET.get('habitat_id')
    media_options = Media.objects.filter(habitat_id=habitat_id).values('media_type', 'media_id')

    # Convert QuerySet to list of dicts
    media_options_list = list(media_options)

    return JsonResponse(media_options_list, safe=False)


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


def view_all_data(request, ref_id=None):
    if ref_id is None:
        # If ref_id is not provided - redirecting to a default reference?
        # trying to redirect to the first reference if available
        first_reference = Reference.objects.order_by('ref_id').first()
        if first_reference:
            return redirect('view_all_data', ref_id=first_reference.ref_id)
        else:
            return render(request, 'view_all_data.html', {'error_message': 'No references available.'})

    try:
        # Get the reference with the specified ref_id
        reference = Reference.objects.get(ref_id=ref_id)
    except Reference.DoesNotExist:
        # Handle the case where the reference does not exist
        reference = None

    return render(request, 'view_all_data.html', {'reference': reference})


def next_ref_record(request, ref_id):
    try:
        # Get the next reference with a ref_id greater than the current one
        next_reference = Reference.objects.filter(ref_id__gt=ref_id).order_by('ref_id').first()

        if next_reference:
            # Redirect to the view_all_data page for the next reference
            return redirect('view_all_data', ref_id=next_reference.ref_id)
        else:
            # If no next reference, redirect to the view_all_data page for the current reference
            return redirect('view_all_data', ref_id=ref_id)
    except Reference.DoesNotExist:
        # Handle the case where the reference does not exist
        return redirect('view_all_data', ref_id=ref_id)


def prev_ref_record(request, ref_id):
    try:
        # Get the previous reference with a ref_id less than the current one
        prev_reference = Reference.objects.filter(ref_id__lt=ref_id).order_by('-ref_id').first()

        if prev_reference:
            # Redirect to the view_all_data page for the previous reference
            return redirect('view_all_data', ref_id=prev_reference.ref_id)
        else:
            # If no previous reference, redirect to the view_all_data page for the current reference
            return redirect('view_all_data', ref_id=ref_id)
    except Reference.DoesNotExist:
        # Handle the case where the reference does not exist
        return redirect('view_all_data', ref_id=ref_id)


def next_datacr_record(request, ref_id, cr_id):
    try:
        # Get the next DataCR with a cr_id greater than the current one
        next_datacr = DataCR.objects.filter(cr_id__gt=cr_id, reference__ref_id=ref_id).order_by('cr_id').first()

        if next_datacr:
            # Redirect to the view_all_data page for the next DataCR
            return redirect('view_all_data', ref_id=ref_id, cr_id=next_datacr.cr_id)
        else:
            # If no next DataCR, redirect to the view_all_data page for the current reference and DataCR
            return redirect('view_all_data', ref_id=ref_id, cr_id=cr_id)
    except DataCR.DoesNotExist:
        # Handle the case where the DataCR does not exist
        return redirect('view_all_data', ref_id=ref_id, cr_id=cr_id)


def prev_datacr_record(request, ref_id, cr_id):
    try:
        # Get the previous DataCR with a cr_id less than the current one
        prev_datacr = DataCR.objects.filter(cr_id__lt=cr_id, reference__ref_id=ref_id).order_by('-cr_id').first()

        if prev_datacr:
            # Redirect to the view_all_data page for the previous DataCR
            return redirect('view_all_data', ref_id=ref_id, cr_id=prev_datacr.cr_id)
        else:
            # If no previous DataCR, redirect to the view_all_data page for the current reference and DataCR
            return redirect('view_all_data', ref_id=ref_id, cr_id=cr_id)
    except DataCR.DoesNotExist:
        # Handle the case where the DataCR does not exist
        return redirect('view_all_data', ref_id=ref_id, cr_id=cr_id)


############## HELPERS ###############

def get_habitat_id(habitat_name):
    habitats = Habitat.objects.filter(habitat_specific_type=habitat_name)

    if habitats.exists():
        # Return the ID of the first with the given name
        return habitats.first().habitat_id
    else:
        # Handle the case where none with the given name exists
        return None


def get_wildlife_group_id(wildlife_group_n):
    wildlife_group = WildlifeGroup.objects.filter(wildlife_group_name=wildlife_group_n)

    if wildlife_group.exists():
        # Return the ID of the first with the given name
        return wildlife_group.first().wildlife_group_id
    else:
        # Handle the case where none with the given name exists
        return None


def get_rap_id(rap_n, habitat_id):
    rap = RAP.objects.filter(rap_name=rap_n, habitat=habitat_id).first()

    return rap.rap_id if rap else None


def get_lifestage_id(lifestage_n):
    lifestage = Lifestage.objects.filter(lifestage_name=lifestage_n)

    if lifestage.exists():
        # Return the ID of the first with the given name
        return lifestage.first().lifestage_id
    else:
        # Handle the case where none with the given name exists
        return None


def get_name_common_id(name_c):
    speciesname = SpeciesName.objects.filter(name_common=name_c)

    if speciesname.exists():
        # Return the ID of the first with the given name
        return speciesname.first().species_id
    else:
        # Handle the case where none with the given name exists
        return None


def get_name_latin_id(name_l):
    speciesname = SpeciesName.objects.filter(name=name_l)

    if speciesname.exists():
        # Return the ID of the first with the given name
        return speciesname.first().species_id
    else:
        # Handle the case where none with the given name exists
        return None


def get_studytype_id(studytype_name):
    studytype = StudyType.objects.filter(study_type_name=studytype_name)

    if studytype.exists():
        # Return the ID of the first with the given name
        return studytype.first().study_type_id
    else:
        # Handle the case where none with the given name exists
        return None


def get_tissue_id(tissue_n):
    tissue = Tissue.objects.filter(tissue_name=tissue_n)

    if tissue.exists():
        # Return the ID of the first with the given name
        return tissue.first().tissue_id
    else:
        # Handle the case where none with the given name exists
        return None


def get_media_id(media_name):
    media = Media.objects.filter(media_type=media_name)

    if media.exists():
        # Return the ID of the first with the given name
        return media.first().media_id
    else:
        # Handle the case where none with the given name exists
        return None


def get_radionuclide_id(radionuclide_n):
    radionuclide = Radionuclide.objects.filter(radionuclide_name=radionuclide_n)

    if radionuclide.exists():
        # Return the ID of the first with the given name
        return radionuclide.first().radionuclide_id
    else:
        # Handle the case where none with the given name exists
        return None
