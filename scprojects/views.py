from django.shortcuts import render
from django.http import HttpResponse
from .models import Project
from django.core import serializers

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def projects(request):
    projects = Project.objects.all()
    data = serializers.serialize("json", projects)
    return HttpResponse(data)


# next up TODO's
# add project
# add user
# login
