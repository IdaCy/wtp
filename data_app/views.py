from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import DataCR, PubType, PubTitle, Language, Reference, Habitat, SpeciesName
from .models import RAP, Lifestage, StudyType, ActivityConcUnit, Media
from .forms import DataCRForm

from django.http import JsonResponse
from django.views import View

from django.shortcuts import render, redirect
from django.urls import reverse


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
    if request.method == 'POST':
        form = DataCRForm(request.POST)

        if form.is_valid():
            # Save the Reference object
            reference = Reference(
                author=form.cleaned_data['author'],
                article_title=form.cleaned_data['ref_article_title'],
                # Add other fields as needed
            )
            reference.save()

            # Save the DataCR object with the reference foreign key
            datacr = DataCRForm(
                reference=reference,
                habitat=form.cleaned_data['habitat_specific_type'],
                wildlife_group=form.cleaned_data['wildlife_group_name'],
                # Add other fields as needed
            )
            datacr.save()

            return redirect('success_page')  # Redirect to a success page or any other desired URL
    else:
        form = DataCRForm()

    return render(request, 'add_datacr.html', {'form': form})



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
        # If ref_id is not provided, you can redirect to a default reference or handle it as you prefer
        # For example, redirect to the first reference if available
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
