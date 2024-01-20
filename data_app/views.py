from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import DataCR, PubType, PubTitle, Language
from .models import Reference
from .forms import DataCRForm


@login_required
def data_view(request):
    dataobj = DataCR.objects.all()
    return render(request, 'data.html', {'data': dataobj})


@login_required
def ref_view(request):
    refobj = Reference.objects.all()
    return render(request, 'reference.html', {'reference': refobj})


@login_required
def add_datacr(request):
    # Handle form submission
    if request.method == 'POST':
        form = DataCRForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Redirect to the data view or any other desired page
            return redirect('data_view')
    else:
        # Render the form for GET requests
        form = DataCRForm()

    return render(request, 'add_datacr.html', {
        'form': form,
        'pub_types': PubType.objects.all(),
        'pub_titles': PubTitle.objects.all(),
        'languages': Language.objects.all(),
    })
