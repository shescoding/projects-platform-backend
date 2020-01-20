from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all/', views.projects, name='projects'),
    path('logout/', views.logout, name='logout'),
]
