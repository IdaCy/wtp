from django.contrib.auth.decorators import login_required
from django.contrib.postgres.aggregates import StringAgg
from django.db.models.functions import Cast
from django.db.models.fields import TextField
from django.shortcuts import render
from data_app.models import DataCR, WildlifeGroup, Habitat, RAP, User, Reference


@login_required
def all_reports(request):
    return render(request, 'all_reports.html')


@login_required
def report_user(request):
    details_query = request.GET.get('parameter', '')
    print(details_query)
    approval = request.GET.get('approval_show', '') == 'approval'
    print(approval)
    selection_type = request.GET.get('selection_type', '')
    selection_id = request.GET.get('selection_id', '')

    # Using distinct and order_by to ensure unique and sorted values
    users = User.objects.order_by('first_name').values_list('first_name', flat=True).distinct()
    wildlife_groups = WildlifeGroup.objects.order_by('wildlife_group_name').distinct('wildlife_group_name')
    raps = RAP.objects.order_by('rap_name').distinct('rap_name')

    context = {
        'datacr_list': [],
        'details_query': details_query,
        'approval': approval,
        'users': users,
        'wildlife_groups': wildlife_groups,
        'raps': raps,
        'selection_id': selection_id,
        'selection_type': selection_type,
    }

    filters = {}
    if selection_type and selection_id.isdigit():
        filter_key = 'wildlife_group__wildlife_group_id' if selection_type == 'wildlife' else 'icrp_rap__rap_id'
        filters[filter_key] = int(selection_id)

    if details_query:
        approval_status = "APPROVED" if approval else "REJECTED"
        print(approval_status)
        datacr_list = DataCR.objects.all().filter(
            reference__approval_status=approval_status,
            reference__user__email__isnull=False,
            **filters
        ).values(
            'reference__user__email',
        ).annotate(
            email=StringAgg(Cast('reference__user__email', output_field=TextField()), delimiter=', ', distinct=True),
            salutation=StringAgg(Cast('reference__user__salutation', output_field=TextField()), delimiter=', ',
                                 distinct=True),
            firstname=StringAgg(Cast('reference__user__first_name', output_field=TextField()), delimiter=', ',
                                distinct=True),
            lastname=StringAgg(Cast('reference__user__last_name', output_field=TextField()), delimiter=', ',
                               distinct=True),
            company=StringAgg(Cast('reference__user__company', output_field=TextField()), delimiter=', ',
                              distinct=True),
            # reference_ids=StringAgg(Cast('reference__ref_id', output_field=TextField()), delimiter=', ', distinct=True),
            # approval=StringAgg(Cast('reference__approval_status', output_field=TextField()), delimiter=', ', distinct=True),
        ).distinct().order_by('reference__user__email')

        context['datacr_list'] = datacr_list

    return render(request, 'report_user.html', context)


@login_required
def report_authors(request):
    selection_id = request.GET.get('selection_id', '')

    context = {
        'ref_list': [],
        'selection_id': selection_id,
    }

    if selection_id == 'authors':
        ref_list = Reference.objects.all().values('author').distinct()
        print(ref_list)
        context['ref_list'] = ref_list

    if selection_id == 'users':
        ref_list = Reference.objects.all().filter(
            user__email__isnull=False,
        ).values(
            'user__email',
        ).annotate(
            email=StringAgg(Cast('user__email', output_field=TextField()), delimiter=', ', distinct=True),
            salutation=StringAgg(Cast('user__salutation', output_field=TextField()), delimiter=', ',
                                 distinct=True),
            firstname=StringAgg(Cast('user__first_name', output_field=TextField()), delimiter=', ',
                                distinct=True),
            lastname=StringAgg(Cast('user__last_name', output_field=TextField()), delimiter=', ',
                               distinct=True),
        ).distinct().order_by('user__email')

        print(ref_list)
        context['ref_list'] = ref_list

    return render(request, 'report_authors.html', context)
