from django.db import models
from django.contrib.auth.models import User
# from .models import UserProfile
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience_lvl = models.PositiveSmallIntegerField(blank=True)
    position = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField()
    github_username = models.CharField(max_length=255, blank=True)
    github_id = models.PositiveIntegerField(blank=True)
    github_url = models.URLField(max_length=255, blank=True)
    avatar_url = models.URLField(max_length=255, blank=True)
    gravatar_url = models.URLField(max_length=255, blank=True)


class Project(models.Model):
    name = models.CharField(max_length=255)
    github_url = models.URLField(max_length=255, blank=True)
    description = models.TextField()
    looking_for = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    lead = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, related_name="leads")

    contributors = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def getInitials(self, user):
        return user.first_name[0] + user.last_name[0]

    def dict_format(self):
        contributers_list = [
            self.getInitials(user) for user in self.contributors.all()]
        print("contributors", contributers_list)
        # get lead info bundle

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
            "contributors": contributers_list,
        }
