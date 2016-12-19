from django.db import models


# def _upload_path(instance, filename):
#     if instance.classtype == 1 and instance.imagetype == 1:
#         return instance.get_profile_upload_path(filename)
#     elif instance.classtype == 1 and instance.imagetype == 2:
#         return instance.get_head_upload_path(filename)
#     elif instance.classtype == 2:
#         return instance.get_upload_path(filename)


# def _upload_path(instance, filename):
#     return instance.get_upload_path(filename)

def get_ngo_profile_upload_path(self, filename):
    return "uploads/ngo/" + str(self.ngo.pk) + "/profile/" + filename

def get_ngo_head_upload_path(self, filename):
    return "uploads/ngo/" + str(self.ngo.pk) + "/head/" + filename

def get_project_picture_upload_path(self, filename):
    return "uploads/projects/" + str(self.project.pk) + "/" + filename


class Ngo(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField(blank=True)
    phoneNo = models.CharField(max_length=15)
    ngoId = models.CharField(max_length=20, primary_key=True)
    latitude = models.CharField(max_length=5, blank=True)
    longitude = models.CharField(max_length=5, blank=True)
    address = models.CharField(max_length=500)


class NgoPicture(models.Model):
    ngo = models.ForeignKey(Ngo)
    profile = models.ImageField(upload_to=get_ngo_profile_upload_path, default='default/no-img.png')
    head = models.ImageField(upload_to=get_ngo_head_upload_path, default='default/no-img.png')
    # profile = models.ImageField(upload_to=lambda instance,
    #                             filename: "uploads/ngo/".join([str(instance.pk), "/profile/", filename]),
    #                             default='images/default/no-img.jpg')
    # head = models.ImageField(upload_to=lambda instance, filename: "uploads/ngo/".join([str(instance.pk), "/head/",
    #                                                                                    filename]),
    #                          default='images/default/no-img.jpg')
    # picture = models.ImageField(upload_to=_upload_path, default='images/default/no-img.png')

    # def get_upload_path(self, filename):
    #     return "uploads/ngo/" + str(self.ngo.pk) + "/" + filename


class Project(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=10000)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    cost = models.BigIntegerField()
    status = models.BigIntegerField(blank=True)
    ngo = models.ForeignKey(Ngo)


class ProjectPicture(models.Model):
    project = models.ForeignKey(Project)
    picture = models.ImageField(upload_to=get_project_picture_upload_path, default='default/no-img.png')
    # picture = models.ImageField(upload_to=lambda instance,
    #                             filename: "uploads/projects/".join([str(instance.pk), "/", filename]),
    #                             default='images/default/no-img.jpg')


class User(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField()
    phoneNo = models.CharField(max_length=15)
    fbCred = models.CharField(max_length=100, blank=True)
    googleCred = models.CharField(max_length=100, blank=True)


class Picture(models.Model):
    picture = models.ImageField(upload_to='images/uploads', default='images/default/no-img.jpg')


class Donation(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    amount = models.FloatField(null=True)
