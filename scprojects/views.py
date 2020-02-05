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
from django.db import IntegrityError, transaction


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def projects(request):
    projects = Project.objects.all()
    response = {}
    print("ccc request auth", request.auth)
    # print("csrf_token", csrf.get_token(request))
    token = ''
    if request.user.is_authenticated:
        token = Token.objects.get(user=request.user)
    # print("auth token", str(token), request.user, request.user.is_authenticated)
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
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user(request):
    response = {}
    print("ccc request auth", request.auth)
    token = ''
    if request.user.is_authenticated:
        token = Token.objects.get(user=request.user)
        print("auth token", str(token), request.user,
              request.user.is_authenticated)
        response["user"] = {
            "name": request.user.username,
            "is_authenticated": request.user.is_authenticated,
            "csrf_token": csrf.get_token(request),
            "auth_token": str(token)
        }
    else:
        response["user"] = ""

    return JsonResponse(response)
# Todo separate projects with auth call


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic
def add_project(request):
    if request.user.is_authenticated and request.method == "POST":
        data = request.data

        # Get repo name and description
        github_url = request.data["github_url"]
        repo_details = github_url.split(
            'https://github.com/')[1]
        response = requests.get(
            'https://api.github.com/repos/'+repo_details)
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
        user_profile.position = request.data['position']
        user_profile.save()
        new_project = Project(
            name=repo_data["name"],
            github_url=data["github_url"],
            description=repo_data["description"],
            looking_for=data["looking_for"],
            lead=user_profile,
            contributors=contributors_list,
        )
        new_project.save()
        return JsonResponse({"result": "success"})
    else:
        return JsonResponse({"result": "error", "reason": "authentication required"})


@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def login(request):
    token = ''
    if request.user.is_authenticated:
        try:
            token = Token.objects.get(user=request.user)
            print("Login token from DB ", token)
            return HttpResponseRedirect("http://localhost:3000/token/"+str(token))
        except Token.DoesNotExist:
            token = None
            return HttpResponseRedirect("http://localhost:3000/")


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.auth.delete()
    return JsonResponse({"result": "success", "type": "logout"})
