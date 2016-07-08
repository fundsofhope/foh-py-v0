from django.db import models


class User(models.Model):
    name = models.CharField(max_length=500, null=False)
    email = models.EmailField(null=False)
    phoneNo = models.CharField(max_length=15, null=False)
    fbCred = models.CharField(max_length=100)
    googleCred = models.CharField(max_length=100)


class Ngo(models.Model):
    name = models.CharField(max_length=500, null=False)
    email = models.EmailField(null=False)
    phoneNo = models.CharField(max_length=15, null=False)
    ngoId = models.CharField(max_length=20, primary_key=True)
    latitude = models.CharField(max_length=5)
    longitude = models.CharField(max_length=5)
    address = models.CharField(max_length=500, null=False)


class Project(models.Model):
    title = models.CharField(max_length=500, null=False)
    description = models.CharField(max_length=10000, null=False)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    cost = models.BigIntegerField()
    status = models.BigIntegerField()
