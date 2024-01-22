from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import DataCR, PubType, PubTitle, Language, Reference, Habitat, SpeciesName
from .models import RAP, Lifestage, StudyType, ActivityConcUnit, Media, WildlifeGroup
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
                ref_id=form.cleaned_data['reference_id'],
                author=form.cleaned_data['author'],
                article_title=form.cleaned_data['ref_article_title'],
                pub_title=form.cleaned_data['publication_title'],
                year=form.cleaned_data['year'],
                volume=form.cleaned_data['volume'],
                part=form.cleaned_data['part'],
                pages=form.cleaned_data['page_numbers'],
                language=form.cleaned_data['reference_language'],
                pub_type=form.cleaned_data['publication_title'],
                translation=form.cleaned_data['translation_available'],
                notes=form.cleaned_data['notes'],
                user=request.user,
                dc_id=form.cleaned_data['reference_id'],
                approval_status='PENDING',
            )
            reference.save()

            # Save the DataCR object with the reference foreign key
            datacr = DataCR(
                reference=reference,
                habitat_id=get_habitat_id(form.cleaned_data['habitat_specific_type']),
                wildlife_group_id=get_wildlife_group_id(form.cleaned_data['wildlife_group_name']),
                icrp_rap=get_rap_id(form.cleaned_data['icrp_rap'], habitat_id),
                lifestage=get_lifestage_id(form.cleaned_data['lifestage_name']),
                species_name=get_name_common_id(form.cleaned_data['common_names']),
                study_type=get_study_type_id(form.cleaned_data['study_type_name']),
                measurement_date=form.cleaned_data['measurement_date'],
                tissue=get_study_tissue_id(form.cleaned_data['tissue_name']),
                media=get_study_media_id(form.cleaned_data['media_type']),
                crn=form.cleaned_data['n_of_cr'],
                cr=form.cleaned_data['concentration_ratio'],
                cr_sd=form.cleaned_data['sd_of_cr'],
                radionuclide=get_radionuclide_id(form.cleaned_data['radionuclide_name']),
                biota_conc=form.cleaned_data['biota_conc'],
                biota_conc_units=form.cleaned_data['biota_conc_units'],
                biota_n=form.cleaned_data['biota_n'],
                biota_sd=form.cleaned_data['biota_sd'],
                biota_wet_dry=form.cleaned_data['biota_wet_dry'],
                media_conc=form.cleaned_data['media_conc'],
                media_n=form.cleaned_data['media_n'],
                media_conc_units=form.cleaned_data['media_conc_units'],
                media_sd=form.cleaned_data['media_sd'],
                media_wet_dry=form.cleaned_data['media_wet_dry'],
                approval_data_status='PENDING',
            )
            datacr.save()

            return redirect('success_page')  # Redirect to a success page or any other desired URL

        else:
            print(form.errors)
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
