from django.shortcuts import render
from django.http import HttpResponse
from .models import Project
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django.http import JsonResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def projects(request):
    projects = Project.objects.all()
    response = {}
    response["user"] = {
        "username": request.user.username,
        "is_authenticated": request.user.is_authenticated,
    }
    response["projects"] = []
    for project in list(projects):
        json_obj = project.__dict__()
        response["projects"].append(json_obj)

    return JsonResponse(response)


def logout(request):
    django_logout(request)
    return JsonResponse({"status": "success"})
