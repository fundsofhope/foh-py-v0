import json

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_exempt

from fundsofhope.forms import UploadImageForm
from fundsofhope.models import ProjectPicture, User, Project


# Picture Actions
def index(request):
    return render_to_response('upload.html')


def upload_pic(request, project_id):
    # print project_id
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            m = ProjectPicture()
            m.picture = form.cleaned_data['picture']
            m.project.pk = project_id
            m.save()
            # project = Project.objects.get(pk=project_id)
            # project.photo_set.add(ProjectPicture.objects.get(pk=m.pk))
            # project.save()
            return JsonResponse({'status': 'true'})
    else:
        form = UploadImageForm()
        form.id = project_id
        return render(request, 'upload.html', {'form': form})


@csrf_exempt
def show_image(request, project_id):
    if request.method == 'GET':
        # body = json.loads(request.body)
        # pic = Picture()
        project = Project.objects.get(pk=project_id)
        urls = []
        for image in project.image_set.all():
            urls.append(image.picture.url)
        return JsonResponse({'urls': urls})
        # return JsonResponse({"url":user.picture.picture.url})


# User Actions
@csrf_exempt
def signup(request):
    global fbCred
    if request.method == 'POST':
        body = json.loads(request.body)
        if User.objects.filter(phoneNo=body['phoneNo']).count() > 0:
            user = User.objects.get(phoneNo=body['phoneNo'])
            user.name = body['name']
            user.email = body['email']
            if 'fbCred' in body and 'googleCred' in body and body['googleCred'] != "" and body['fbCred'] != "":
                fbCred = body['fbCred']
                user.fbCred = fbCred
                gcred = body['googleCred']
                user.googleCred = gcred
                user.save()
            elif 'fbCred' in body and body['fbCred'] != "":
                fbCred = body['fbCred']
                user.fbCred = fbCred
                user.save()
            elif 'googleCred' in body and body['googleCred'] != "":
                gcred = body['googleCred']
                user.googleCred = gcred
                user.save()
            return JsonResponse({"status": "User updated", "user_id": User.objects.get(phoneNo=body['phoneNo']).pk},
                                safe=False)
        else:
            user = User(
                name=body['name'],
                phoneNo=body['phoneNo'],
                email=body['email'],
            )
            user.save()
            if 'fbCred' in body and 'googleCred' in body:
                fbCred = body['fbCred']
                user.fbCred = fbCred
                gcred = body['googleCred']
                user.googleCred = gcred
                user.save()
            elif 'fbCred' in body:
                fbCred = body['fbCred']
                user.fbCred = fbCred
                user.save()
            elif 'googleCred' in body:
                gcred = body['googleCred']
                user.googleCred = gcred
                user.save()

        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error"})


@csrf_exempt
def account(request):
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

        return JsonResponse({
            'name': user.name,
            'phoneNo': user.phoneNo,
            'email': user.email,
            'project_donated': projects_donated,
            'googleCred': user.googleCred,
            'fbCred': user.fbCred
        },
            safe=False)


# Project Actions
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
def donate(request):
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
            return JsonResponse({'status': 'Donation Successful'})
        else:
            return HttpResponse({'status': 'Donation Unsuccessful'})
