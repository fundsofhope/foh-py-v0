from django.db import models


def _upload_path(instance, filename):
    return instance.get_upload_path(filename)


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
    picture = models.ImageField(upload_to=_upload_path, default='images/default/no-img.jpg')

    def get_upload_path(self, filename):
        return "uploads/ngo/" + str(self.ngo.pk) + "/" + filename


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
    picture = models.ImageField(upload_to=_upload_path, default='images/default/no-img.jpg')

    def get_upload_path(self, filename):
        return "uploads/projects/" + str(self.project.pk) + "/" + filename


class User(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField()
    phoneNo = models.CharField(max_length=15)
    fbCred = models.CharField(max_length=100, blank=True)
    googleCred = models.CharField(max_length=100, blank=True)
    projects = models.ManyToManyField(Project, blank=True)
