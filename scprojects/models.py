from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=255)
    github_url = models.URLField(max_length=255, blank=True)
    lead = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="leads")
    description = models.TextField()
    looking_for = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    contributors = models.ManyToManyField(User)

    def __str__(self):
        return self.name


