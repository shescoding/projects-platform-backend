from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from django.http import HttpResponse
from .models import Project, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt, ensure_csrf_cookie
from rest_framework.decorators import api_view
from django.middleware import csrf
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
def projects(request):
    projects = Project.objects.all()
    response = {}
    print("csrf_token", csrf.get_token(request))
    token = ''
    if request.user.is_authenticated:
        token = Token.objects.get(user=request.user)
    print("auth token", str(token))
    response["user"] = {
        "name": request.user.username,
        "is_authenticated": request.user.is_authenticated,
        "csrf_token": csrf.get_token(request),
        "auth_token": str(token)
    }
    response["projects"] = []
    for project in list(projects):
        json_obj = project.dict_format()
        response["projects"].append(json_obj)

    return JsonResponse(response)


@csrf_exempt
@api_view(['POST'])
def add_project(request):
    print("HELLO WORLD")
    # get params from request
    # pull infor from git repo - description
    # if request.method == "GET":
    #     return JsonResponse({"csrf": csrf.get_token(request)})
    # print("user", request.user.id)
    if request.user.is_authenticated and request.method == "POST":
        user_profile = UserProfile.objects.get(user=request.user)
        print("github_url",
              request)
        for key, value in request.POST.items():
            print('Key: %s' % (key))
        # new_project = Project(
        #     name="", //
        #     github_url="", //
        #     description="", //
        #     looking_for="",
        #     lead="", //
        #     contributors="", //
        # )
        # new_project.save()
        return JsonResponse({"status": "new project"})
    else:
        return JsonResponse({"status": "you need to be authenticated to create project"})


def logout(request):
    django_logout(request)
    return JsonResponse({"status": "logout success"})
