from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import UploadFileForm
from .csvmgr import (import_active_contracts,
                     import_new_admissions,
                     import_move_outs,
                     export_active_tenants,
                     export_housing)


def gen_csv_response(name, method):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(name)
    method(response)
    return response


@login_required
def import_view(request):
    if request.method == 'POST':
        if request.POST.get('export-contracts'):
            return gen_csv_response('active contracts', export_active_tenants)
        elif request.POST.get('export-housing'):
            return gen_csv_response('housing structure', export_housing)
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