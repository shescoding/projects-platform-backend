from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience_lvl = models.PositiveSmallIntegerField(blank=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField()
    github_username = models.CharField(max_length=255, blank=True)
    github_id = models.PositiveIntegerField(blank=True)
    github_url = models.URLField(max_length=255, blank=True)
    avatar_url = models.URLField(max_length=255, blank=True)
    gravatar_url = models.URLField(max_length=255, blank=True)


class Project(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255)
    github_url = models.URLField(null=False, blank=False, max_length=255)
    description = models.TextField(null=False, blank=False)
    looking_for = models.TextField(null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    lead = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, related_name="leads", blank=False)
    contributors = ArrayField(
        models.CharField(max_length=100))

    def __str__(self):
        return self.name

    def getInitials(self, login):
        return login[0].upper()

    def dict_format(self, is_auth):
        contributers_list = [
            self.getInitials(login) for login in self.contributors]
        # get lead info bundle
        lead_obj = {}
        lead_obj["name"] = self.lead.user.first_name + \
            ' ' + self.lead.user.last_name
        lead_obj["position"] = self.lead.position
        lead_obj["experience"] = self.lead.experience_lvl
        github_url = ''
        if is_auth:
            lead_obj["email"] = self.lead.user.email
            github_url = self.github_url

        return {
            "id": self.id,
            "name": self.name,
            "github_url": github_url,
            "lead": lead_obj,
            "description": self.description,
            "looking_for": self.looking_for,
            "created": self.created,
            "updated": self.updated,
            "contributors": contributers_list,
        }
