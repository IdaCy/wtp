from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import DataCR, PubType, PubTitle, Language, Reference, Habitat, SpeciesName, ReferenceRejectionReason
from .models import RAP, Lifestage, StudyType, ActivityConcUnit, Media, WildlifeGroup, Element, Radionuclide, Tissue
from .forms import DataCRForm, ReferenceForm

from django.http import JsonResponse
from math import exp, log

from django.http import JsonResponse
from django.views import View

from django.db.models.functions import Concat
from django.contrib.postgres.aggregates import StringAgg
from django.db.models.functions import Cast
from django.db.models.fields import TextField

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from django.http import JsonResponse

from django.db.models import Avg, Sum, Min, Max, Count, Window, F
import statistics
import math
from django.db.models.functions import RowNumber


def reject_reference(reference_id, reason):
    try:
        reference = Reference.objects.get(pk=reference_id)
        if reference.approval_status == 'REJECTED':
            ReferenceRejectionReason.objects.create(reference=reference, reason=reason)
        else:
            # possibly: raising an exception or handle the logic for when a non-rejected reference is attempted to be associated with a rejection reason
            print("Reference is not marked as rejected.")
    except Reference.DoesNotExist:
        # !!Handling the case where the reference does not exist
        print("Reference does not exist.")


def get_rejection_reason(reference_id):
    try:
        reference = Reference.objects.get(pk=reference_id)
        if reference.approval_status == 'REJECTED' and hasattr(reference, 'rejection_reason'):
            return reference.rejection_reason.reason
        else:
            return "This reference is not rejected or does not have a rejection reason."
    except Reference.DoesNotExist:
        return "Reference does not exist."


def article_title_search(request):
    if 'term' in request.GET:
        qs = Reference.objects.filter(article_title__icontains=request.GET.get('term'))
        titles = list(qs.values_list('article_title', flat=True))
        return JsonResponse(titles, safe=False)
    return JsonResponse([], safe=False)


@login_required
def data_view(request):
    dataobj = ActivityConcUnit.objects.all()
    return render(request, 'data.html', {'data': dataobj})


@login_required
def download_summaries(request):
    return render(request, 'download_summaries.html')


@login_required
def view_summary_results(request):
    habitat_query = request.GET.get('habitat', '')
    selection_type = request.GET.get('selection_type', '')
    selection_id = request.GET.get('selection_id', '')

    # Using distinct and order_by to ensure unique and sorted values
    habitats = Habitat.objects.order_by('habitat_specific_type').values_list('habitat_specific_type', flat=True).distinct()
    wildlife_groups = WildlifeGroup.objects.order_by('wildlife_group_name').distinct('wildlife_group_name')
    raps = RAP.objects.order_by('rap_name').distinct('rap_name')

    # Query for unique habitat names
    #habitats = Habitat.objects.order_by('habitat_specific_type').values_list('habitat_specific_type', flat=True).distinct()

    context = {
        'datacr_list': [],
        'wildlife_groups': wildlife_groups,
        'raps': raps,
        'habitat_query': habitat_query,
        'selection_type': selection_type,
        'selection_id': selection_id,
        'habitats': habitats,
    }

    # Construct filters for the query based on user selection
    filters = {'habitat__habitat_specific_type': habitat_query} if habitat_query else {}
    if selection_type and selection_id.isdigit():
        selection_id = int(selection_id)
        if selection_type == 'wildlife':
            filters['wildlife_group__wildlife_group_id'] = selection_id
        elif selection_type == 'rap':
            filters['icrp_rap__rap_id'] = selection_id

    # Fetch all elements irrespective of whether other data exists for them
    elements = DataCR.objects.values('radionuclide__element__element_symbol').distinct().order_by('radionuclide__element__element_symbol')

    datacr_list = []
    for element in elements:
        element_symbol = element['radionuclide__element__element_symbol']
        aggregated_data = DataCR.objects.filter(
            radionuclide__element__element_symbol=element_symbol, **filters
        ).aggregate(
            arith_mean_cr=Avg('cr'),
            sum_crn=Sum('crn'),
            min_cr=Min('cr'),
            max_cr=Max('cr'),
            reference_ids=StringAgg(Cast('reference__ref_id', output_field=TextField()), delimiter=', ', distinct=True)
        )

        # Making sure the element symbol is included in the aggregated data for display
        aggregated_data['element_symbol'] = element_symbol

        # Ensuring even if no data is found, the element still gets displayed
        datacr_list.append(aggregated_data)




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


def handle_reference_datacr(reference_form, datacr_form, user):
    if reference_form.is_valid() and datacr_form.is_valid():
        print("CR Value from Form:", datacr_form.cleaned_data.get('cr'))
        print("CRN Value from Form:", datacr_form.cleaned_data.get('crn'))
        reference = reference_form.save(commit=False)
        reference.user = user
        reference.save()

        datacr = datacr_form.save(commit=False)
        datacr.reference = reference
        datacr.save()
        return True, reference_form, datacr_form
    else:
        print("Reference form errors:", reference_form.errors)
        print("DataCR form errors:", datacr_form.errors)
        return False, reference_form, datacr_form


@login_required
def add_datacr(request):
    # Defining 'species_list' here so it's available regardless of if...else outcome
    species_list = SpeciesName.objects.all()

    if request.method == 'POST':
        print("POST Data:", request.POST)

        reference_form = ReferenceForm(request.POST)
        datacr_form = DataCRForm(request.POST)

        success, reference_form, datacr_form = handle_reference_datacr(
            reference_form=reference_form,
            datacr_form=datacr_form,
            user=request.user
        )

        if success:
            messages.success(request, "Successfully saved. Thank you for your submission!")
            return redirect('add_datacr')
        else:
            messages.error(request, "There was a problem with your submission. Please try again or contact us.")
    else:
        reference_form = ReferenceForm()
        datacr_form = DataCRForm()

    # needing 'species_list' in the context
    context = {
        'reference_form': reference_form,
        'datacr_form': datacr_form,
        'species_list': species_list,
    }
    return render(request, 'add_datacr.html', context)


@login_required
def get_media_for_habitat(request):
    habitat_id = request.GET.get('habitat_id')
    media_options = Media.objects.filter(habitat_id=habitat_id).values('media_type', 'media_id')

    # Convert QuerySet to list of dicts
    media_options_list = list(media_options)

    return JsonResponse(media_options_list, safe=False)


# def get_correction_factor(request, unit_symbol, media_type):
# unit_symbol = unit_symbol
# media_type_string = media_type

@login_required
def get_correction_factor(request):
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


@login_required
def view_editable_data_records(request):
    # Fetch records with 'PENDING' status and belong to the logged-in user
    records = Reference.objects.filter(approval_status='PENDING', user=request.user)
    return render(request, 'view_editable_data_records.html', {'records': records})


@login_required
def edit_data_record(request, ref_id):
    species_list = SpeciesName.objects.all()
    print("Edit data record POST data:", request.POST)
    reference = get_object_or_404(Reference, pk=ref_id)
    print(reference.ref_id)
    try:
        datacr = DataCR.objects.filter(reference=reference).first()
        if not datacr:
            messages.error(request, 'No associated DataCR record found.')
            return redirect('some_error_handling_view')
    except DataCR.DoesNotExist:
        messages.error(request, 'No associated DataCR record found.')
        return redirect('some_error_handling_view')

    print("next comes 'POST'")
    if request.method == 'POST':
        reference_form = ReferenceForm(request.POST, instance=reference)
        datacr_form = DataCRForm(request.POST, instance=datacr)

        print("next comes 'success' and entering my method")
        success, _, _ = handle_reference_datacr(reference_form, datacr_form, request.user)
        print("my method is through")
        if success:
            print("was successful actually - so should print message in cmd !")
            messages.success(request, 'Record updated successfully!')
            print("printed it in cmd???")
        else:
            print("aha! that's why... error after all")
            messages.error(request, "There was a problem with your submission. Please review the form and try again.")
    else:
        reference_form = ReferenceForm(instance=reference)
        datacr_form = DataCRForm(instance=datacr)

    return render(request, 'edit_data_record.html', {
        'species_list': species_list,
        'reference_form': reference_form,
        'datacr_form': datacr_form,
        'ref_id': ref_id,
        'reference': reference,
        'form_action': reverse('edit_data_record', kwargs={'ref_id': ref_id})
    })


@login_required
def view_all_data(request, ref_id=None, cr_id=None):
    # Redirect to a URL with the first Reference's ID if ref_id is not provided
    if ref_id is None:
       #first_reference = Reference.objects.order_by('ref_id').first()
        first_reference = Reference.objects.filter(approval_status='APPROVED').order_by('ref_id').first()
        if first_reference:
           #first_datacr = first_reference.datacr_set.order_by('cr_id').first()
            first_datacr = first_reference.datacr_set.filter(approval_status='APPROVED').order_by('cr_id').first()
            if first_datacr:
                # Redirect to a URL with both ref_id and cr_id for the first Reference and its first DataCR
                return redirect('view_all_data', ref_id=first_reference.ref_id, cr_id=first_datacr.cr_id)
            else:
                # Redirect to a URL with only ref_id if there are no DataCR objects
                return redirect('view_all_data', ref_id=first_reference.ref_id)
        else:
            # Render a page with an error message if there are no Reference objects
            return render(request, 'view_all_data.html', {'error_message': 'No references available.'})

    # Get the current reference
    reference = get_object_or_404(Reference, pk=ref_id)

    # Determine the first DataCR for the current Reference if cr_id is not provided
    if not cr_id:
       #first_datacr = reference.datacr_set.first()
        first_datacr = reference.datacr_set.filter(approval_status='APPROVED').order_by('cr_id').first()
        if first_datacr:
            cr_id = first_datacr.id
        else:
            cr_id = None

    # Get the current DataCR based on cr_id
    if cr_id:
        datacr = get_object_or_404(DataCR, pk=cr_id, reference_id=ref_id)
    else:
        datacr = None

    # Calculate next and previous Reference IDs
   #next_ref = Reference.objects.filter(ref_id__gt=ref_id).order_by('ref_id').first()
    next_ref = Reference.objects.filter(ref_id__gt=ref_id, approval_status='APPROVED').order_by('ref_id').first()
    #first_datacr = first_reference.datacr_set.filter(approval_status='APPROVED').order_by('cr_id').first()
    prev_ref = Reference.objects.filter(ref_id__lt=ref_id, approval_status='APPROVED').order_by('-ref_id').first()

    # Calculate the first DataCR ID for next and previous References
    if next_ref:
        next_ref_first_datacr = next_ref.datacr_set.first()
       #next_ref_first_datacr = next_ref.datacr_set.filter(approval_status='APPROVED').order_by('cr_id').first()
       #TAKEN FROM: first_datacr = reference.datacr_set.filter(approval_status='APPROVED').order_by('cr_id').first()
    else:
        next_ref_first_datacr = None

    if prev_ref:
        prev_ref_first_datacr = prev_ref.datacr_set.first()
       #prev_ref_first_datacr = prev_ref.datacr_set.filter(approval_status='APPROVED').order_by('cr_id').first()
    else:
        prev_ref_first_datacr = None

    # Calculate next and previous DataCR IDs within the current Reference
    next_datacr = reference.datacr_set.filter(cr_id__gt=cr_id, approval_status='APPROVED').order_by('cr_id').first()
    prev_datacr = reference.datacr_set.filter(cr_id__lt=cr_id, approval_status='APPROVED').order_by('-cr_id').first()

    context = {
        'reference': reference,
        'datacr': datacr,
        'ref_id': ref_id,
        'next_ref_id': next_ref.ref_id if next_ref else None,
        'prev_ref_id': prev_ref.ref_id if prev_ref else None,
        'next_datacr_id': next_datacr.cr_id if next_datacr else None,
        'prev_datacr_id': prev_datacr.cr_id if prev_datacr else None,
        'first_cr_of_next_ref': next_ref_first_datacr.cr_id if next_ref_first_datacr else None,
        'first_cr_of_prev_ref': prev_ref_first_datacr.cr_id if prev_ref_first_datacr else None,
    }

    # Get all references ordered by ref_id
    references_with_row_number = Reference.objects.annotate(
        row_number=Window(
            expression=RowNumber(),
            order_by=F('ref_id').asc()
        )
    )

    # Find the current reference's row number and total count
    current_reference_row_number = None
    total_references = references_with_row_number.count()
    if reference:
        current_reference_info = references_with_row_number.filter(ref_id=reference.ref_id).first()
        if current_reference_info:
            current_reference_row_number = current_reference_info.row_number

    # Update context with pagination info
    context.update({
        'total_references': total_references,
        'current_reference_position': current_reference_row_number,
    })

    return render(request, 'view_all_data.html', context)


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
