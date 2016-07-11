from django.db import models


class Ngo(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField(blank=True)
    phoneNo = models.CharField(max_length=15)
    ngoId = models.CharField(max_length=20, primary_key=True)
    latitude = models.CharField(max_length=5, blank=True)
    longitude = models.CharField(max_length=5, blank=True)
    address = models.CharField(max_length=500)


class Project(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=10000)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    cost = models.BigIntegerField()
    status = models.BigIntegerField(blank=True)
    ngo = models.ForeignKey(Ngo)


class User(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField()
    phoneNo = models.CharField(max_length=15)
    fbCred = models.CharField(max_length=100, blank=True)
    googleCred = models.CharField(max_length=100, blank=True)
    projects = models.ManyToManyField(Project, blank=True)


class ExampleModel(models.Model):
    picture = models.ImageField(upload_to='pic_folder/', default='pic_folder/None/no-img.jpg')
