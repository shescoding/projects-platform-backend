from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from django.http import HttpResponse, HttpResponseRedirect
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
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
import requests


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def projects(request):
    projects = Project.objects.all()
    response = {}
    print("csrf_token", csrf.get_token(request))
    token = ''
    if request.user.is_authenticated:
        token = Token.objects.get(user=request.user)
    print("auth token", str(token), request.user, request.user.is_authenticated)
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_project(request):
    print("HELLO WORLD")
    if request.user.is_authenticated and request.method == "POST":
        data = request.data
        github_url = request.data["github_url"]
        # Get repo name and description
        response = requests.get(
            'https://api.github.com/repos/shescoding/projects-platform-frontend')
        repo_data = response.json()

        # Get contributors
        contributors_url_response = requests.get(
            repo_data["contributors_url"])
        contributors_data = contributors_url_response.json()
        contributors_list = []
        for contrib in contributors_data:
            contributors_list.append(contrib['login'])

        # Get lead
        user_profile = UserProfile.objects.get(user=request.user)
        print("user_profile", user_profile)
        new_project = Project(
            name=repo_data["name"],
            github_url=data["github_url"],
            description=repo_data["description"],
            looking_for=data["looking_for"],
            lead=user_profile,
            contributors=contributors_list,
        )
        # call github api get name, description, contributors - done
        # install library to save contributors list - done
        # save project and update lead with position, project id in one atomic transaction
        # success json response
        new_project.save()
        return JsonResponse({"status": "new project"})
    else:
        return JsonResponse({"status": "you need to be authenticated to create project"})


def login(request):
    print("HELLO WORLD from login")
    token = ''
    if request.user.is_authenticated:
        token = Token.objects.get(user=request.user)
    print("auth token", str(token))
    return HttpResponseRedirect("http://localhost:3000/token/"+str(token))


def logout(request):
    django_logout(request)
    return JsonResponse({"status": "logout success"})
