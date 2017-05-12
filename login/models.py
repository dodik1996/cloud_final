from __future__ import unicode_literals

from django.db import models

class Person(models.Model):
    username=models.CharField(max_length=100,primary_key=True)
    password=models.CharField(max_length=100)


class Requests(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(max_length=120, null=False, blank=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)