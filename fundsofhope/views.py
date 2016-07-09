from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from fundsofhope.forms import UploadFileForm
from fundsofhope.models import ExampleModel, User, Project


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


@csrf_exempt
def donate_project(request):
    if request.method == 'POST':
        phoneNo = request.POST.get('phoneNo')
        amount = request.POST.get('amount')
        id = request.POST.get('project_id')
        user = User.objects.get(phoneNo=phoneNo)
        project = Project.objects.get(pk=id)
        user.projects.add(project)
        user.ngo.add(project.ngo)
        project.cost = project.cost - int(amount)
        project.save()
        return HttpResponse('Donation Successful')
