from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import DataCR


@login_required
def data_view(request):
    dataobj = DataCR.objects.all()
    return render(request, 'data.html', {'data': dataobj})
