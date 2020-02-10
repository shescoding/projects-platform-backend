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
from projectsplatform.settings import FRONTEND_URL
from django.db import IntegrityError


def index(request):
    return HttpResponse("She's Coding Projects API")


@csrf_exempt
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def projects_public(request):
    print("NOT AUTHENTICATED xxx")
    print('XXXXX request', request)
    projects = Project.objects.all()
    response = {}
    response["projects"] = []
    for project in list(projects):
        json_obj = project.dict_format(False)
        response["projects"].append(json_obj)

    return JsonResponse(response)


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def projects(request):
    print("AUTHENTICATED")
    if request.user.is_authenticated:
        token = Token.objects.get(user=request.user)
        projects = Project.objects.all()
        response = {}
        response["projects"] = []
        for project in list(projects):
            json_obj = project.dict_format(True)
            response["projects"].append(json_obj)
        return JsonResponse(response)


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user(request):
    response = {}
    token = ''
    if request.user.is_authenticated:
        token = Token.objects.get(user=request.user)
        response["user"] = {
            "name": request.user.username,
            "is_authenticated": request.user.is_authenticated,
            "csrf_token": csrf.get_token(request),
            "auth_token": str(token)
        }
    else:
        response["user"] = ""
    return JsonResponse(response)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic
def add_project(request):
    if request.user.is_authenticated and request.method == "POST":
        data = request.data

        # Get repo name and description
        try:
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

            # Field validation
            if len(contributors_list) == 0 or request.data['position'] == "" or request.data['experience_lvl'] == "" or repo_data["name"] == "" or data["github_url"] == "" or repo_data["description"] == "" or data["looking_for"] == "":
                raise KeyError(
                    "Ensure all the fields are filled out and Github Repository has description")

            # Get lead
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.position = request.data['position']
            user_profile.experience_lvl = request.data['experience_lvl']
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
        except KeyError as error:
            return JsonResponse(
                {"result": "error", "error_type": "KeyError", "reason": "KeyError: "+str(error), "message": "Some of the form fields are either empty or filled out wrong"})
        except IndexError as error:
            return JsonResponse(
                {"result": "error", "error_type": "IndexError", "reason": "IndexError: "+str(error)+". Check if github_url is valid", "message": "Check if github_url is valid"})
        except IntegrityError as error:
            return JsonResponse({"result": "error", "error_type": "IntegrityError", "reason": "Something went wrong on tring to create project in DB.", "message": "Please make sure your Github project has description, and it doesn't already exist in the projects list."})
    else:
        return JsonResponse({"result": "error", "error_type": "Unauthenticated", "reason": "authentication required"})


@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def login(request):
    token = ''
    if request.user.is_authenticated:
        try:
            token = Token.objects.get(user=request.user)
            return HttpResponseRedirect(FRONTEND_URL+"/#/token/"+str(token))
        except Token.DoesNotExist:
            print("Token.DoesNotExist")
            return JsonResponse({"result": "error", "reason": "Token.DoesNotExist"})


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.auth.delete()
    return JsonResponse({"result": "success", "type": "logout"})
