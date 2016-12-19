import json

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_exempt

from fundsofhope.forms import UploadImageForm
from fundsofhope.models import ProjectPicture, User, Project, Ngo, NgoPicture, Donation


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
        proj = Project.objects.get(pk=project_id)
        urls = []
        for image in proj.image_set.all():
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
        for proj in user.projects.all():
            name = proj.title
            entry = {
                "name": proj.ngo.name,
                "ngo_id": proj.ngo.ngoId,
                "email": proj.ngo.email,
                "phone": proj.ngo.phoneNo
            }
            record = {"name": name, "ngo": entry}
            projects_donated.append(record)
        for donation in Donation.objects.all():
            if user.id == donation.user.id:
                name = donation.project.title
                ngo = {
                    "name": donation.project.ngo.name,
                    "ngo_id": donation.project.ngo.ngoId,
                    "email": donation.project.ngo.email,
                    "phone": donation.project.ngo.phoneNo
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
            'project_donated': projects_donated,
            'googleCred': user.googleCred,
            'fbCred': user.fbCred
        },
            safe=False)


# Project Actions
@csrf_exempt
def project(request):
    if request.method == 'GET':
        if '_id' in request.GET:
            _id = request.GET['_id']
            proj = Project.objects.get(pk=_id)
            entry = {
                'id': proj.ngo.ngoId,
                'name': proj.ngo.name,
            }
            image_arr = []
            for img in ProjectPicture.objects.filter(project=proj):
                image_arr.append(img.picture.url)
            return JsonResponse({
                'title': proj.title,
                'description': proj.description,
                'startDate': proj.startDate,
                'endDate': proj.endDate,
                'cost': proj.cost,
                'status': proj.status,
                'ngo': entry,
                'images': image_arr
            }, safe=False)
        else:
            projects_arr = []
            for proj in Project.objects.all():
                entry = {
                    'id': proj.ngo.ngoId,
                    'name': proj.ngo.name,
                }
                img = ProjectPicture.objects.filter(project=proj).first()
                record = {
                    'id': proj.pk,
                    'title': proj.title,
                    'cost': proj.cost,
                    'status': proj.status,
                    'header': img.picture.url,
                    'ngo': entry
                }
                projects_arr.append(record)
            return JsonResponse(projects_arr, safe=False)


@csrf_exempt
def donate(request):
    if request.method == 'POST':
        donation = Donation()
        donation.user = User.objects.get(pk=request.POST.get('user_id'))
        donation.project = Project.objects.get(pk=request.POST.get('project_id'))
        donation.amount = request.POST.get('amount')
        donation.save()
        return JsonResponse({'status': 'Donation Successful'})
    else:
        return JsonResponse({'status': 'Donation Failed'})


# NGO Actions
@csrf_exempt
def ngo(request):
    if request.method == 'GET':
        if '_id' in request.GET:
            _id = request.GET['_id']
            res = Ngo.objects.get(pk=_id)
            image = NgoPicture.objects.filter(ngo=res).first()
            return JsonResponse({
                'name': res.name,
                'email': res.email,
                'phoneNo': res.phoneNo,
                'head': image.head.url,
                'profile': image.profile.url
            }, safe=False)
        else:
            ngos_arr = []
            for res in Ngo.objects.all():
                image = NgoPicture.objects.filter(ngo=res).first()
                entry = {
                    'id': res.ngoId,
                    'name': res.name,
                    'head': image.head.url
                }
                ngos_arr.append(entry)
            return JsonResponse(ngos_arr, safe=False)

# @csrf_exempt
# def trending(request):
    # if request.method == 'GET':
        # for project in Project.objects.all():
