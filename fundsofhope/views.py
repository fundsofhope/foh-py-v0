from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from fundsofhope.forms import UploadFileForm
from fundsofhope.models import Picture, User, Project


def upload_pic(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            m = Picture()
            m.picture = form.cleaned_data['picture']
            m.save()
            return HttpResponse('image upload success')


def index(request):
    return render_to_response('upload.html')


@csrf_exempt
def donate_project(request):
    if request.method == 'POST':
        phone_no = request.POST.get('phoneNo')
        amount = request.POST.get('amount')
        _id = request.POST.get('project_id')
        user = User.objects.get(phoneNo=phone_no)
        project = Project.objects.get(pk=_id)
        if amount <= project.cost:
            user.projects.add(project)
            project.cost -= int(amount)
            project.save()
            return HttpResponse('Donation Successful')
        else:
            return HttpResponse('Donation Unsuccessful')


@csrf_exempt
def user_json(request):
    if request.method == 'POST':
        phone_no = request.POST.get('phoneNo')
        user = User.objects.get(phoneNo=phone_no)
        projects_donated = []
        for project in user.projects.all():
            name = project.title
            ngo = {
                "name": project.ngo.name,
                "ngo_id": project.ngo.ngoId,
                "email": project.ngo.email,
                "phone": project.ngo.phoneNo
            }
            record = {"name": name, "ngo": ngo}
            projects_donated.append(record)
            # for ngo in user.ngo.all():
            #     name = ngo.name
            #     record = {"name":name}
            #     leads_as_json = serializers.serialize('json', user.ngo.all().exclude())
            # ngo_donated.append(record)

        return JsonResponse({
            'name': user.name,
            'phoneNo': user.phoneNo,
            'email': user.email,
            'project_donated': projects_donated
        },
            safe=False)


@csrf_exempt
def projects(request):
    if request.method == 'GET':
        projects_arr = []
        for project in Project.objects.all():
            ngo = {
                'id': project.ngo.ngoId,
                'name': project.ngo.name,
                'email': project.ngo.email,
                'phoneNo': project.ngo.phoneNo
            }
            record = {
                'id': project.pk,
                'title': project.title,
                'description': project.description,
                'startDate': project.startDate,
                'endDate': project.endDate,
                'cost': project.cost,
                'status': project.status,
                'ngo': ngo
            }
            projects_arr.append(record)
        return JsonResponse(projects_arr, safe=False)


@csrf_exempt
def signup(request):
    global fbCred
    if request.method == 'POST':
        if User.objects.filter(phoneNo=request.POST['phoneNo']).count() > 0:
           return JsonResponse({"status" : "User already exist", "user_id":User.objects.get(phoneNo=request.POST['phoneNo']).pk}, safe=False)
        else:
            user = User(
                name=request.POST['name'],
                phoneNo=request.POST['phoneNo'],
                email=request.POST['email'],
                )
            user.save()
            if 'fbCred' in request.POST and 'googleCred' in request.POST:
                fbCred = request.POST['fbCred']
                user.fbCred = fbCred
                googleCred = request.POST['googleCred']
                user.googleCred = googleCred
                user.save()
            elif 'fbCred' in request.POST:
                fbCred = request.POST['fbCred']
                user.fbCred = fbCred
                user.save()
            elif 'googleCred' in request.POST:
                googleCred = request.POST['googleCred']
                user.googleCred = googleCred
                user.save()

        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status":"error"})