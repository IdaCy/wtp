from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# View function for rendering the dashboard
@login_required
def board_view(request):
    return render(request, 'dashboard.html')
