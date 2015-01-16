from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import UploadFileForm
from .csvmgr import import_active_contracts, import_new_admissions, import_move_outs, export_active_tenants

@login_required
def import_view(request):
    if request.method == 'POST':
        if request.POST.get('export'):
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="active contracts.csv"'
            export_active_tenants(response)
            return response
        else:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                if request.POST.get('new-admissions'):
                    import_new_admissions(form.cleaned_data['file'])
                message = "Successful import"
            else:
                message = "CSV file is required to do the import!!!"

        return render(request, 'import-housing.html', {'message': message})
    else:
        return render(request, 'import-housing.html', {})