from django.contrib.auth.decorators import login_required
from django.contrib.postgres.aggregates import StringAgg
from django.db.models.functions import Cast
from django.db.models.fields import TextField
from django.shortcuts import render
from data_app.models import DataCR, WildlifeGroup, Habitat, RAP, User


@login_required
def all_reports(request):
    return render(request, 'all_reports.html')


@login_required
def report_user(request):
    details_query = request.GET.get('parameter', '')
    print(details_query)
    accepted = request.GET.get('accepted_show', '') == 'accepted'
    selection_type = request.GET.get('selection_type', '')
    selection_id = request.GET.get('selection_id', '')

    # Using distinct and order_by to ensure unique and sorted values
    users = User.objects.order_by('first_name').values_list('first_name', flat=True).distinct()
    wildlife_groups = WildlifeGroup.objects.order_by('wildlife_group_name').distinct('wildlife_group_name')
    raps = RAP.objects.order_by('rap_name').distinct('rap_name')

    context = {
        'datacr_list': [],
        'details_query': details_query,
        'accepted': accepted,
        'users': users,
        'wildlife_groups': wildlife_groups,
        'raps': raps,
        'selection_id': selection_id,
        'selection_type': selection_type,
    }

    filters = {}
    #filters = {'approval_status': accepted} if details_query else {}
    if selection_type and selection_id.isdigit():
        filter_key = 'wildlife_group__wildlife_group_id' if selection_type == 'wildlife' else 'icrp_rap__rap_id'
        filters[filter_key] = int(selection_id)

    if details_query:
        datacr_list = DataCR.objects.all().filter(
            **filters
        ).values(
            'reference__user__email',
        ).annotate(
            email=StringAgg(Cast('reference__user__email', output_field=TextField()), delimiter=', ', distinct=True),
            salutation=StringAgg(Cast('reference__user__salutation', output_field=TextField()), delimiter=', ', distinct=True),
            firstname=StringAgg(Cast('reference__user__first_name', output_field=TextField()), delimiter=', ', distinct=True),
            lastname=StringAgg(Cast('reference__user__last_name', output_field=TextField()), delimiter=', ', distinct=True),
            company=StringAgg(Cast('reference__user__company', output_field=TextField()), delimiter=', ', distinct=True),
            reference_ids=StringAgg(Cast('reference__ref_id', output_field=TextField()), delimiter=', ', distinct=True)
        ).distinct().order_by('reference__user__email')

        context['datacr_list'] = datacr_list

        # datacr_list = DataCR.objects.filter(**filters).select_related('reference__user').distinct(
        #    'reference__user__first_name').order_by('reference__user__first_name').values('reference__user__first_name')

    """if selection_type and selection_id.isdigit():
        filter_key = 'wildlife_group__wildlife_group_id' if selection_type == 'wildlife' else 'icrp_rap__rap_id'
        filters[filter_key] = int(selection_id)

    filters = {'wildlife_group__wildlife_group_id': selection_type} if selection_type == 'wildlife' else 'icrp_rap__rap_id'
    if accepted:
        filter_key = 'approval_status' if accepted == 'False' else 'True'
        filters[filter_key] = accepted
    filters = {'approval_status': accepted} if accepted else {}
    if selection_type and selection_id.isdigit():
        filter_key = 'wildlife_group__wildlife_group_id' if selection_type == 'wildlife' else 'icrp_rap__rap_id'
        filters[filter_key] = int(selection_id)"""

    """"if details_query:
        datacr_list = DataCR.objects.filter(**filters).values(
            'reference__user__first_name',
        ).values(
            'reference__user__first_name',
        ).annotate(
            first_name='reference__user__first_name',
            lastname='reference__user__lastname',
        ).order_by('radionuclide__element__element_symbol')

    datacr_list = DataCR.objects.filter(**filters).select_related('reference__user').distinct(
        'reference__user__first_name').order_by('reference__user__first_name').values('reference__user__first_name')

    context['datacr_list'] = datacr_list

    if details_query:
        datacr_list = DataCR.objects.filter(**filters).select_related('reference__user').distinct(
            'reference__user__first_name').order_by('reference__user__first_name').values('reference__user__first_name')

        context['datacr_list'] = datacr_list   """

    return render(request, 'report_user.html', context)
