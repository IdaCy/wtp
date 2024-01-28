from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def all_reports(request):
    return render(request, 'all_reports.html')