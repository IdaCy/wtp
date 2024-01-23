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
            reference = form.save(commit=False)
            reference.user = request.user
            reference.approval_status = 'PENDING'
            reference.save()

            # Create and save the DataCR object with the reference foreign key
            datacr = DataCR.form.save(commit=False)
            # Assigning fields from the form to the DataCR instance
            datacr.reference = reference
            datacr.habitat = get_habitat_id(form.cleaned_data['habitat_specific_type'])
            datacr.wildlife_group = get_wildlife_group_id(form.cleaned_data['wildlife_group_name'])
            datacr.icrp_rap = get_rap_id(form.cleaned_data['icrp_rap'], datacr.habitat.habitat_id if datacr.habitat else None)
            datacr.lifestage = get_lifestage_id(form.cleaned_data['lifestage_name'])
            datacr.species_name = get_name_common_id(form.cleaned_data['name_common'])
            datacr.study_type = get_studytype_id(form.cleaned_data['study_type_name'])
            datacr.measurement_date = form.cleaned_data['measurement_date']
            datacr.tissue = get_tissue_id(form.cleaned_data['tissue_name'])
            datacr.media = get_media_id(form.cleaned_data['media_type'])
            datacr.crn = form.cleaned_data['n_of_cr']
            datacr.cr = form.cleaned_data['concentration_ratio']
            datacr.cr_sd = form.cleaned_data['sd_of_cr']
            datacr.radionuclide = get_radionuclide_id(form.cleaned_data['radionuclide_name'])
            datacr.biota_conc = form.cleaned_data['biota_conc']
            datacr.biota_conc_units = form.cleaned_data['biota_conc_units']
            datacr.biota_n = form.cleaned_data['biota_n']
            datacr.biota_sd = form.cleaned_data['biota_sd']
            datacr.biota_wet_dry = form.cleaned_data['biota_wet_dry']
            datacr.media_conc = form.cleaned_data['media_conc']
            datacr.media_n = form.cleaned_data['media_n']
            datacr.media_conc_units = form.cleaned_data['media_conc_units']
            datacr.media_sd = form.cleaned_data['media_sd']
            datacr.media_wet_dry = form.cleaned_data['media_wet_dry']
            datacr.approval_data_status = 'PENDING'

            # Fields not covered by the form
            datacr.notes = "Default notes"
            datacr.from_erica = False
            datacr.accepted = False
            datacr.biohalflife = "Default biota half life"
            datacr.data_extract = 0
            datacr.other_tissue = "Default other tissue"
            datacr.qc = False
            datacr.rep_organ_units = "Default rep organ units"
            datacr.reproductive_organ = "Default reproductive organ"
            datacr.rep_wet_dry = "W"
            datacr.stand_biota_conc = 1.0
            datacr.stand_biota_sd = "Default stand biota sd"
            datacr.stand_media_conc = 1.0
            datacr.stand_media_sd = "Default stand media sd"
            datacr.summary_approve = False
            datacr.approval_data_status = 'PENDING'

            datacr.save()

            return redirect('success_page')
        else:
            # Handling form errors
            print(form.errors)
            return render(request, 'add_datacr.html', {'form': form})
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
