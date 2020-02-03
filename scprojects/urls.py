from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all/', views.projects, name='projects'),
    path('add_project/', views.add_project, name='add_projects'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # re_path(r'^rest-auth/github/$',
    #         views.GitHubLogin.as_view(), name='github_login')

]
