from django.db import models
from django.contrib.auth.models import User
# from .models import UserProfile
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience_lvl = models.PositiveSmallIntegerField()
    position = models.CharField(max_length=255)
    is_active = models.BooleanField()
    github_username = models.CharField(max_length=255)
    github_id = models.PositiveIntegerField()
    github_url = models.URLField(max_length=255)
    avatar_url = models.URLField(max_length=255)
    gravatar_url = models.URLField(max_length=255)


class Project(models.Model):
    name = models.CharField(max_length=255)
    github_url = models.URLField(max_length=255, blank=True)
    description = models.TextField()
    looking_for = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # get lead info bundle
    lead = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, related_name="leads")

    # contributors = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def dict_format(self):
        print(self.lead)
        lead_obj = {}
        lead_obj["name"] = self.lead.user.first_name + \
            ' ' + self.lead.user.last_name
        lead_obj["position"] = self.lead.position
        lead_obj["experience"] = self.lead.experience_lvl
        return {
            "id": self.id,
            "name": self.name,
            "github_url": self.github_url,
            "lead": lead_obj,
            "description": self.description,
            "looking_for": self.looking_for,
            "created": self.created,
            "updated": self.updated,
            # "contributors": self.contributors,
        }
