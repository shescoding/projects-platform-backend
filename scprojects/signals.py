from django.db.models.signals import pre_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from allauth.account.signals import user_logged_in
from django.db.models.signals import post_save
from django.core.signals import request_finished
from .models import UserProfile
from django.conf import settings
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        token = Token.objects.create(user=instance)


@receiver(user_logged_in)
def retrieve_social_data(request, user, **kwargs):
    data = SocialAccount.objects.filter(
        user=user, provider='github')[0].extra_data
    try:
        newUser = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        newUser = UserProfile(
            user=user,
            experience_lvl=0,
            position=data["company"],
            is_active=True,
            github_username=data["login"],
            github_id=data["id"],
            github_url=data["html_url"],
            avatar_url=data["avatar_url"],
            gravatar_url=data["gravatar_id"],
        )
        newUser.save()
