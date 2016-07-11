from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from fundsofhope.forms import UploadFileForm
from fundsofhope.models import ExampleModel, User, Project
from django.http import JsonResponse


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
        project.cost -= int(amount)
        project.save()
        return HttpResponse('Donation Successful')


@csrf_exempt
def user_json(request):
    if request.method == 'POST':
        phoneNo = request.POST.get('phoneNo')
        user = User.objects.get(phoneNo=phoneNo)
        projects_donated = []
        for project in user.projects.all():
            name = project.title
            ngo = {"name":project.ngo.name,"ngo_id":project.ngo.ngoId,"email":project.ngo.email,"phone":project.ngo.phoneNo}
            record = {"name": name,"ngo":ngo}
            projects_donated.append(record)
        # for ngo in user.ngo.all():
        #     name = ngo.name
        #     record = {"name":name}
        #     leads_as_json = serializers.serialize('json', user.ngo.all().exclude())
            # ngo_donated.append(record)

        return JsonResponse({'name':user.name,'phoneNo':user.phoneNo,'email':user.email,
                             'project_donated': projects_donated}, safe=False)
