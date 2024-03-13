from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import DataCR, PubType, PubTitle, Language, Reference, Habitat, SpeciesName, ReferenceRejectionReason
from .models import RAP, Lifestage, StudyType, ActivityConcUnit, Media, WildlifeGroup, Element, Radionuclide, Tissue
from .models import MaterialStatus, ParCRCalc, MaterialCRCalc
from .forms import DataCRForm, ReferenceForm

from django import template

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

from django.db.models import Avg, Sum, Min, Max, Count, Window, F, StdDev
import statistics
import math
from django.db.models.functions import RowNumber


@login_required
def tables_panel(request):
    term = request.GET.get('term', '')
    context = {
        'selected_term': term,
    }

    # Depending on the term, fetch the appropriate data from the database
    if term == 'Elements':
        context['data'] = Element.objects.all()
    elif term == 'Habitats':
        context['data'] = Habitat.objects.all()
    elif term == 'WildlifeGroups':
        context['data'] = WildlifeGroup.objects.all()
    elif term == 'RAPs':
        context['data'] = RAP.objects.all()
    elif term == 'Lifestages':
        context['data'] = Lifestage.objects.all()
    elif term == 'Media':
        context['data'] = Media.objects.all()
    elif term == 'PublicationTypes':
        context['data'] = PubType.objects.all()
    elif term == 'PublicationTitles':
        context['data'] = PubTitle.objects.all()
    elif term == 'SpeciesNames':
        context['data'] = SpeciesName.objects.all()
    elif term == 'StudyTypes':
        context['data'] = StudyType.objects.all()
    elif term == 'Tissues':
        context['data'] = Tissue.objects.all()
    elif term == 'MaterialStatus':
        context['data'] = MaterialStatus.objects.all()
    elif term == 'ActivityConcentrationUnits':
        context['data'] = ActivityConcUnit.objects.all()
    elif term == 'ParameterCRCalculations':
        context['data'] = ParCRCalc.objects.all()
    elif term == 'MaterialCRCalculations':
        context['data'] = MaterialCRCalc.objects.all()
    elif term == 'Radionuclide':
        context['data'] = Radionuclide.objects.all()
    elif term == 'Languages':
        context['data'] = Language.objects.all()

    return render(request, 'tables_panel.html', context)


@login_required
def get_table_data(request):
    term = request.GET.get('term')
    data = {'headers': [], 'rows': []}

    # Implement logic to set headers and rows based on the term
    if term == 'Elements':
        data['headers'] = ['Element ID', 'Element Symbol']
        elements = Element.objects.filter(approved=True).values_list('element_id', 'element_symbol')
        data['rows'] = list(elements)
    elif term == 'Habitats':
        data['headers'] = ['Habitat ID', 'Habitat Specific Type', 'Habitat Main Type', 'User ID']
        habitats = Habitat.objects.filter(approved=True).values_list('habitat_id', 'habitat_specific_type',
                                                                     'habitat_main_type_id', 'user')
        data['rows'] = list(habitats)
    elif term == 'WildlifeGroups':
        data['headers'] = ['Wildlife Group ID', 'Wildlife Group Name', 'Habitat', 'Data Extract', 'User ID',
                           'de_tophab_topwild', 'de_tophab_indwild', 'de_indhab_topwild', 'de_indhab_indwild']
        wildlife_groups = WildlifeGroup.objects.filter(approved=True).values_list('wildlife_group_id',
                                                                                  'wildlife_group_name', 'habitat',
                                                                                  'data_extract', 'user',
                                                                                  'de_tophab_topwild',
                                                                                  'de_tophab_indwild',
                                                                                  'de_indhab_topwild',
                                                                                  'de_indhab_indwild')
        data['rows'] = list(wildlife_groups)
    elif term == 'RAPs':
        data['headers'] = ['RAP ID', 'RAP Name', 'Habitat', 'Wildlife Group', 'Summary']
        raps = RAP.objects.filter(approved=True).values_list('rap_id', 'rap_name', 'habitat', 'wildlife_group',
                                                             'summary')
        data['rows'] = list(raps)
    elif term == 'Lifestages':
        data['headers'] = ['Lifestage ID', 'Lifestage Name']
        lifestages = Lifestage.objects.filter(approved=True).values_list('lifestage_id', 'lifestage_name')
        data['rows'] = list(lifestages)
    elif term == 'Media':
        data['headers'] = ['Media ID', 'Media Type', 'User', 'Habitat']
        media = Media.objects.filter(approved=True).values_list('media_id', 'media_type', 'user', 'habitat')
        data['rows'] = list(media)
    elif term == 'PublicationTypes':
        data['headers'] = ['Publication Type ID', 'Publication Type Name', 'User ID']
        pub_types = PubType.objects.filter(approved=True).values_list('pub_type_id', 'pub_type_name', 'user')
        data['rows'] = list(pub_types)
    elif term == 'PublicationTitles':
        data['headers'] = ['Publication Title ID', 'Publication Title Name', 'Publication Type', 'User ID']
        pub_titles = PubTitle.objects.filter(approved=True).values_list('pub_title_id', 'pub_title_name', 'pub_type',
                                                                        'user')
        data['rows'] = list(pub_titles)
    elif term == 'SpeciesNames':
        data['headers'] = ['Species ID', 'Latin Name', 'Common Name', 'User ID']
        species_names = SpeciesName.objects.filter(approved=True).values_list('species_id', 'name_latin', 'name_common',
                                                                              'user')
        data['rows'] = list(species_names)
    elif term == 'StudyTypes':
        data['headers'] = ['Study Type ID', 'Study Type Name']
        study_types = StudyType.objects.all().values_list('study_type_id', 'study_type_name')
        data['rows'] = list(study_types)
    elif term == 'Tissues':
        data['headers'] = ['Tissue ID', 'Tissue Name', 'Correction Factor Tissue', 'User ID']
        tissues = Tissue.objects.filter(approved=True).values_list('tissue_id', 'tissue_name',
                                                                   'correction_factor_tissue', 'user')
        data['rows'] = list(tissues)
    elif term == 'MaterialStatus':
        data['headers'] = ['Material Status ID', 'Material Status Name', 'Correction Ratio', 'Media']
        material_status = MaterialStatus.objects.all().values_list('material_status_id', 'material_status_name',
                                                                   'correction_ratio', 'media')
        data['rows'] = list(material_status)
    elif term == 'ActivityConcentrationUnits':
        data['headers'] = ['Activity Conc. Unit ID', 'Symbol', 'Correction Factor', 'Media']
        activity_units = ActivityConcUnit.objects.filter(approved=True).values_list('act_conc_unit_id',
                                                                                    'act_conc_unit_symbol',
                                                                                    'correction_factor_act_conc',
                                                                                    'media')
        data['rows'] = list(activity_units)
    elif term == 'ParameterCRCalculations':
        data['headers'] = ['CR ID', 'Wildlife Group', 'Tissue', 'Dry to Wet Ratio', 'Ash to Wet Ratio',
                           'Is Fresh/Marine/Terrestrial']
        par_calcs = ParCRCalc.objects.all().values_list('cr_id', 'wildlife_group_id', 'tissue_id', 'dry_to_wet_ratio',
                                                        'ash_to_wet_ratio', 'is_fre_mar_ter')
        data['rows'] = list(par_calcs)
    elif term == 'MaterialCRCalculations':
        data['headers'] = ['CR ID', 'Element', 'Organism', 'Liver to Body Ratio', 'Bone to Body Ratio',
                           'Muscle to Body Ratio', 'Is Fresh/Marine/Terrestrial']
        material_calcs = MaterialCRCalc.objects.all().values_list('cr_id', 'element_id', 'organism',
                                                                  'liver_to_body_ratio', 'bone_to_body_ratio',
                                                                  'muscle_to_body_ratio', 'is_fre_mar_ter')
        data['rows'] = list(material_calcs)
    elif term == 'Radionuclides':
        data['headers'] = ['Radionuclide ID', 'Radionuclide Name', 'Element', 'User ID']
        radionuclides = Radionuclide.objects.filter(approved=True).values_list('radionuclide_id', 'radionuclide_name',
                                                                               'element_id', 'user')
        data['rows'] = list(radionuclides)
    elif term == 'Languages':
        data['headers'] = ['Language ID', 'Language', 'User ID']
        languages = Language.objects.filter(approved=True).values_list('language_id', 'language', 'user')
        data['rows'] = list(languages)

    return JsonResponse(data)


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
        titles = list(qs.values_list('article_title', flat=True).distinct())
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

    # Check if the "Show All" checkbox is checked
    show_all = request.GET.get('table23_show', '') == 'table23'

    # Using distinct and order_by to ensure unique and sorted values
    habitats = Habitat.objects.order_by('habitat_specific_type').values_list('habitat_specific_type',
                                                                             flat=True).distinct()
    wildlife_groups = WildlifeGroup.objects.order_by('wildlife_group_name').distinct('wildlife_group_name')
    raps = RAP.objects.order_by('rap_name').distinct('rap_name')

    context = {
        'datacr_list': [],
        'wildlife_groups': wildlife_groups,
        'raps': raps,
        'habitat_query': habitat_query,
        'selection_type': selection_type,
        'selection_id': selection_id,
        'habitats': habitats,
        'show_all': show_all,
    }

    # Construct filters for the query based on user selection
    filters = {'habitat__habitat_specific_type': habitat_query} if habitat_query else {}
    if selection_type and selection_id.isdigit():
        filter_key = 'wildlife_group__wildlife_group_id' if selection_type == 'wildlife' else 'icrp_rap__rap_id'
        filters[filter_key] = int(selection_id)

    if habitat_query:
        datacr_list = DataCR.objects.filter(**filters).values(
            'radionuclide__element__element_symbol'
        ).values(
            'radionuclide__element__element_symbol'
        ).annotate(
            arith_mean_cr=Avg('cr'),
            sum_crn=Sum('crn'),
            min_cr=Min('cr'),
            max_cr=Max('cr'),
            geo_mean_cr=Sum('crn'),
            arith_std_dev=Sum('crn'),
            geo_std_dev=Sum('crn'),
            reference_ids=StringAgg(Cast('reference__ref_id', output_field=TextField()), delimiter=', ', distinct=True)
            # needing to cast reference__ref_id to a text field before aggregation
        ).order_by('radionuclide__element__element_symbol')

        # Calculate standard deviation etc for each element symbol
        for item in datacr_list:
            item['arith_mean_cr'] = "{:.2e}".format(item['arith_mean_cr']) if item['arith_mean_cr'] else None
            item['min_cr'] = "{:.2e}".format(item['min_cr']) if item['min_cr'] else None
            item['max_cr'] = "{:.2e}".format(item['max_cr']) if item['max_cr'] else None

            cr_values = list(DataCR.objects.filter(
                radionuclide__element__element_symbol=item['radionuclide__element__element_symbol'],
                habitat__habitat_specific_type=habitat_query
            ).values_list('cr', flat=True))

            # Filter out None and non-positive values for geometric mean
            cr_values = [value for value in cr_values if value and value > 0]

            if cr_values:
                # Calculate geometric mean
                log_sum = sum(math.log(value) for value in cr_values)
                geo_mean = math.exp(log_sum / len(cr_values))

                # Calculate arithmetic standard deviation - if needed
                try:
                    arith_std_dev = statistics.stdev(cr_values)
                except statistics.StatisticsError:
                    arith_std_dev = None

                # Geometric Standard Deviation
                log_deviation_sum = sum((math.log(value) - math.log(geo_mean)) ** 2 for value in cr_values)
                geo_std_dev = math.exp(math.sqrt(log_deviation_sum / len(cr_values)))

                item['geo_mean_cr'] = "{:.2e}".format(geo_mean) if geo_mean is not None else None
                item['arith_std_dev'] = "{:.2e}".format(arith_std_dev) if arith_std_dev is not None else None
                item['geo_std_dev'] = "{:.2e}".format(geo_std_dev) if geo_std_dev is not None else None
            else:
                item['geo_mean_cr'] = None
                item['arith_std_dev'] = None
                item['geo_std_dev'] = None

        # Only prepare datacr_list2 and datacr_list3 if show_all is True
        if show_all:
            datacr_list2 = DataCR.objects.filter(**filters).values(
                'radionuclide__element__element_symbol'
            ).values(
                'radionuclide__element__element_symbol'
            ).annotate(
                CR=Sum('cr'),
                CRN=Sum('crn'),
                CRSD=Avg('cr_sd'),
                D=Sum('cr'),
                E=Sum('cr'),
            ).order_by('radionuclide__element__element_symbol')

            datacr_list3 = DataCR.objects.filter(**filters).values(
                'radionuclide__element__element_symbol'
            ).values(
                'radionuclide__element__element_symbol'
            ).annotate(
                M=Sum('cr'),
                S=Sum('cr'),
                V=Sum('cr'),
                K=Sum('cr')
            ).order_by('radionuclide__element__element_symbol')

            for item in datacr_list2:
                # Assuming D = CRN * CR
                # Assuming: need to calculate D for each record - iterating over individual records with CR & CRN values
                # Testing: using aggregate functions as placeholders
                crn_cr_product = DataCR.objects.filter(
                    radionuclide__element__element_symbol=item['radionuclide__element__element_symbol'],
                    habitat__habitat_specific_type=habitat_query
                ).annotate(
                    dose=F('crn') * F('cr')
                ).aggregate(total_dose=Sum('dose'))['total_dose']

                # item['D'] = "{:.2e}".format(crn_cr_product) if crn_cr_product is not None else None

                # Assuming: for E, it's an error calculation based on variance or standard deviation
                # Testing: placeholder calculation
                # Assuming: E could be a sum of (CRN * CR^2) - this is an assumption tho!!
                crn_cr_square_sum = DataCR.objects.filter(
                    radionuclide__element__element_symbol=item['radionuclide__element__element_symbol'],
                    habitat__habitat_specific_type=habitat_query
                ).annotate(
                    crn_cr_square=F('crn') * F('cr') * F('cr')
                ).aggregate(total_crn_cr_square=Sum('crn_cr_square'))['total_crn_cr_square']

                # Assign the calculated values directly without formatting
                item['D'] = crn_cr_product
                item['E'] = crn_cr_square_sum
                # item['E'] = "{:.2e}".format(crn_cr_square_sum) if crn_cr_square_sum is not None else None

            # cr_values = DataCR.objects.filter(**filters).values_list('cr', flat=True)
            # cr_values = [value for value in cr_values if value is not None]

            datacr_list3 = []
            elements = DataCR.objects.filter(**filters).values_list('radionuclide__element__element_symbol',
                                                                    flat=True).distinct()
            for element in elements:
                element_cr_values = DataCR.objects.filter(
                    radionuclide__element__element_symbol=element,
                    **filters
                ).values_list('cr', flat=True)

                # Filter out None and non-positive values for geometric mean
                element_cr_values = [value for value in element_cr_values if value and value > 0]

                # Initialize the dictionary to store calculations for the element
                element_data = {
                    'radionuclide__element__element_symbol': element,
                    'M': None,
                    'S': None,
                    'V': None,
                    'K': None
                }

                if element_cr_values:
                    # Calculate mean, sum, variance, and count for the element
                    element_data['M'] = statistics.mean(element_cr_values) if element_cr_values else None
                    element_data['S'] = sum(element_cr_values) if element_cr_values else None
                    element_data['V'] = statistics.variance(element_cr_values) if len(element_cr_values) > 1 else None
                    element_data['K'] = len(element_cr_values)

                    # Formatting for display
                    element_data['M'] = "{:.8f}".format(element_data['M']) if element_data['M'] is not None else None
                    element_data['S'] = "{:.8f}".format(element_data['S']) if element_data['S'] is not None else None
                    element_data['V'] = "{:.8f}".format(element_data['V']) if element_data['V'] is not None else None
                    ###element_data['K'] = "{:.2e}".format(element_data['K']) if element_data['V'] is not None else None

                # Append the element data to the list
                datacr_list3.append(element_data)

            context['datacr_list2'] = datacr_list2
            context['datacr_list3'] = datacr_list3

        context['datacr_list'] = datacr_list
        # context['datacr_list2'] = datacr_list2
        # context['datacr_list3'] = datacr_list3
        context['show_all'] = show_all

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


def handle_reference_datacr(reference_form, datacr_form, user, submit_ref=True, existing_reference=None):
    if submit_ref:
        # For "Add All" action
        if reference_form.is_valid() and datacr_form.is_valid():
            #reference_form.instance.translation = False
            print(datacr_form.errors)
            reference = reference_form.save(commit=False)
            reference.user = user
            reference.save()

            datacr = datacr_form.save(commit=False)
            """print("species name selected?")
            print(datacr_form.cleaned_data.get('species_name'))

            if 'species_name' in datacr_form.cleaned_data and datacr_form.cleaned_data['species_name'] is not None:
                species_id = datacr_form.cleaned_data['species_name'].species_id
                if species_id == 24:
                    datacr.species_name = None"""

            """species_name = datacr_form.cleaned_data.get('species_name')
            if species_name == "" or species_name == "None" or species_name is None:
                datacr.species_name = None"""

            datacr.reference = reference
            datacr.save()
            return True, reference_form, datacr_form
        else:
            return False, reference_form, datacr_form
    else:
        if datacr_form.is_valid():
            datacr = datacr_form.save(commit=False)
            """species_name = datacr_form.cleaned_data.get('species_name')
            if species_name == "" or species_name == "None" or species_name is None:
                datacr.species_name = None"""
            datacr.reference = existing_reference
            datacr.save()
            return True, None, datacr_form  # No need to return a reference form here
        else:
            return False, None, datacr_form


@login_required
def add_datacr(request):
    # Defining 'species_list' here so it's available regardless of if...else outcome
    species_list = SpeciesName.objects.filter(approved=True).order_by('name_latin')

    if request.method == 'POST':
        print("POST Data:", request.POST)
        action = request.POST.get('action')
        success = False

        reference_form = ReferenceForm(request.POST)
        datacr_form = DataCRForm(request.POST)
        print(datacr_form.errors)
        """print("request.POST.get('species_name', ''): ")
        print(request.POST.get('species_name', ''))
        species_name = request.POST.get('species_name', '')
        if species_name == "None":
            datacr_form.species_name = None"""

        #if 'translation' not in request.POST:
         #   reference_form.instance.translation = False

        # Capture reference form values to re-populate after submission
        ref_id = request.POST.get('ref_id', '')
        volume = request.POST.get('volume', '')
        article_title = request.POST.get('article_title', '')


        context = {
            'reference_form': reference_form,
            'datacr_form': datacr_form,
            'species_list': species_list,
        }

        if action == 'add_all':
            success, reference_form, datacr_form = handle_reference_datacr(
                reference_form=reference_form,
                datacr_form=datacr_form,
                user=request.user
            )
            if success:
                # Reset the reference form to clear fields after successful "Add All"
                # reference_form = ReferenceForm()
                context.update({
                    'reference_form': ReferenceForm(),
                    'datacr_form': DataCRForm
                })
        elif action == 'add_mid':
            print('attempting elif add_mid')
            ref_id = request.POST.get('ref_id')
            existing_reference = Reference.objects.filter(ref_id=ref_id).first()
            print(existing_reference)
            if existing_reference:
                print("Attempting Add Mid WITHOUT ref")
                success, _, datacr_form = handle_reference_datacr(
                    reference_form=None,  # Not used in this case
                    datacr_form=datacr_form,
                    user=request.user,
                    submit_ref=False,
                    existing_reference=existing_reference
                )
                print(success)
            else:
                print("Attempting Add Mid WITH ref")
                success, reference_form, datacr_form = handle_reference_datacr(
                    reference_form=reference_form,
                    datacr_form=datacr_form,
                    user=request.user
                )
                print(success)

            """if success:
                initial_data = {'ref_id': ref_id, 'volume': volume, 'article_title': article_title}
                print("Initial Data for Reference Form:", initial_data)
                reference_form = ReferenceForm(initial=initial_data)
                context.update({
                    'reference_form': reference_form,
                    'datacr_form': datacr_form
                })

                return render(request, 'add_datacr.html', context)"""

            # initial_data = {'ref_id': ref_id, 'volume': volume, 'article_title': article_title, }

            # Re-instantiate the reference form with initial data to keep fields filled in all cases
            # reference_form_fields = set(ReferenceForm().fields.keys())
            # initial_data = {key: value for key, value in request.POST.items() if key in reference_form_fields}
            # reference_form = ReferenceForm(initial=initial_data)

        if success:
            messages.success(request, "Successfully saved. Thank you for your submission!")
            return render(request, 'add_datacr.html', context)
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


"""@login_required
def view_editable_data_records(request):
    # Fetch records with 'PENDING' status and belong to the logged-in user
    records = Reference.objects.filter(approval_status='PENDING', user=request.user)
    return render(request, 'view_editable_data_records.html', {'records': records})
"""


@login_required
def view_editable_data_records(request):
    # Fetch records with 'PENDING' status and belong to the logged-in user
    references = Reference.objects.filter(approval_status='PENDING', user=request.user)

    # Create a list to hold data that includes details from both Reference and related DataCR objects
    records_with_details = []
    for ref in references:
        # For each reference, fetch related DataCR objects
        datacr_objects = DataCR.objects.filter(reference=ref)

        # Append a dictionary for each DataCR object related to the reference
        for datacr in datacr_objects:
            records_with_details.append({
                'ref_id': ref.ref_id,
                'article_title': ref.article_title,
                'cr': datacr.cr
            })

        # If there are no related DataCR objects, still add the reference info
        if not datacr_objects:
            records_with_details.append({
                'ref_id': ref.ref_id,
                'article_title': ref.article_title,
                'cr': None
            })

    return render(request, 'view_editable_data_records.html', {'records': records_with_details})


@login_required
def edit_data_record(request, ref_id):
    species_list = SpeciesName.objects.all()
    print("Edit data record POST data:", request.POST)
    reference = get_object_or_404(Reference, pk=ref_id)
    print(reference.ref_id)
    datacr = DataCR.objects.filter(reference=reference).first()
    """try:
        datacr = DataCR.objects.filter(reference=reference).first()
        if not datacr:
            messages.error(request, 'No associated DataCR record found.')
            return redirect('some_error_handling_view')
    except DataCR.DoesNotExist:
        messages.error(request, 'No associated DataCR record found.')
        return redirect('some_error_handling_view')"""

    print("next comes 'POST'")
    if request.method == 'POST':
        reference_form = ReferenceForm(request.POST, instance=reference)
        #datacr_form = DataCRForm(request.POST, instance=datacr)
        datacr_form = DataCRForm(request.POST, instance=datacr if datacr else None)

        if 'translation' not in request.POST:
            reference_form.instance.translation = False
        else:
            reference_form.instance.translation = True

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
        'datacr': datacr,
        #'cr_id': cr_id,
        'form_action': reverse('edit_data_record', kwargs={'ref_id': ref_id})
    })


register = template.Library()


@login_required
def delete_entire_record_confirm(request, ref_id):
    reference = get_object_or_404(Reference, pk=ref_id)
    if request.method == 'POST':
        reference.delete()
        messages.success(request, "Entire record deleted successfully.")
        return redirect('view_editable_data_records')
    else:
        return render(request, 'confirm_delete_entire_record.html', {'ref_id': ref_id})


@login_required
def delete_datacr_record_confirm(request, cr_id):
    # This view can be used to confirm the deletion of a single DataCR record
    datacr = get_object_or_404(DataCR, pk=cr_id)
    if request.method == 'POST':
        # Assuming deletion is confirmed
        datacr.delete()
        messages.success(request, "DataCR record deleted successfully.")
        return redirect('view_editable_data_records')  # Redirect to your listing view
    return render(request, 'confirm_delete_datacr_record.html', {'datacr': datacr})


@login_required
def view_all_data(request, ref_id=None, cr_id=None):
    # Redirect to a URL with the first Reference's ID if ref_id is not provided
    if ref_id is None:
        # first_reference = Reference.objects.order_by('ref_id').first()
        first_reference = Reference.objects.filter(approval_status='APPROVED').order_by('ref_id').first()
        if first_reference:
            # first_datacr = first_reference.datacr_set.order_by('cr_id').first()
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

    # `reference_list` contains all the references to include
    reference_list = Reference.objects.filter(approval_status='APPROVED').order_by('ref_id')
    paginator = Paginator(reference_list, 1)  # Show 1 reference per page for navigation

    # Find out the current page number
    current_page_number = paginator.page_range[ref_id - 1]  # Assuming ref_id corresponds directly to page numbers

    # Decide how many page numbers to show on each side of the current page
    num_pages_to_show = 2
    start_index = max(1, current_page_number - num_pages_to_show)
    end_index = min(paginator.num_pages, current_page_number + num_pages_to_show)

    # Generate the range of page numbers to display
    page_range = range(start_index, end_index + 1)

    # Get the current reference
    reference = get_object_or_404(Reference, pk=ref_id)

    # Determine the first DataCR for the current Reference if cr_id is not provided
    if not cr_id:
        # first_datacr = reference.datacr_set.first()
        first_datacr = reference.datacr_set.filter(approval_status='APPROVED').order_by('cr_id').first()
        if first_datacr:
            cr_id = first_datacr.cr_id
        else:
            cr_id = None

    # Get the current DataCR based on cr_id
    if cr_id:
        datacr = get_object_or_404(DataCR, pk=cr_id, reference_id=ref_id)
    else:
        datacr = None

    # Calculate next and previous Reference IDs
    # next_ref = Reference.objects.filter(ref_id__gt=ref_id).order_by('ref_id').first()
    next_ref = Reference.objects.filter(ref_id__gt=ref_id, approval_status='APPROVED').order_by('ref_id').first()
    # first_datacr = first_reference.datacr_set.filter(approval_status='APPROVED').order_by('cr_id').first()
    prev_ref = Reference.objects.filter(ref_id__lt=ref_id, approval_status='APPROVED').order_by('-ref_id').first()

    # Calculate the first DataCR ID for next and previous References
    if next_ref:
        next_ref_first_datacr = next_ref.datacr_set.first()
    # next_ref_first_datacr = next_ref.datacr_set.filter(approval_status='APPROVED').order_by('cr_id').first()
    # TAKEN FROM: first_datacr = reference.datacr_set.filter(approval_status='APPROVED').order_by('cr_id').first()
    else:
        next_ref_first_datacr = None

    if prev_ref:
        prev_ref_first_datacr = prev_ref.datacr_set.first()
    # prev_ref_first_datacr = prev_ref.datacr_set.filter(approval_status='APPROVED').order_by('cr_id').first()
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
        'page_range': page_range,
        'current_page_number': current_page_number,
        'paginator': paginator,
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
