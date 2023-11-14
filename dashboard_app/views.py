# board_app/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def board_view(request):
    return render(request, 'board.html')
