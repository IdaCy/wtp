from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import DataCR
from .models import Reference


@login_required
def data_view(request):
    dataobj = DataCR.objects.all()
    return render(request, 'data.html', {'data': dataobj})


@login_required
def ref_view(request):
    refobj = Reference.objects.all()
    return render(request, 'reference.html', {'reference': refobj})
