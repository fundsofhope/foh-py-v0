from django.http import HttpResponse
from django.shortcuts import render_to_response

from fundsofhope.forms import UploadFileForm
from fundsofhope.models import ExampleModel


def upload_pic(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            m = ExampleModel()
            m.picture = form.cleaned_data['picture']
            m.save()
            return HttpResponse('image upload success')


def index(request):
    return render_to_response('upload.html')
