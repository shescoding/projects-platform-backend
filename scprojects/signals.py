from django.db.models.signals import pre_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from allauth.account.signals import user_logged_in
from django.core.signals import request_finished
from .models import UserProfile

# request_finished.connect(
#     "http://127.0.0.1:8000/accounts/github/login/callback")
# ljsadkjdljs


@receiver(user_logged_in)
def retrieve_social_data(request, user, **kwargs):
    print("hello xxx")
    data = SocialAccount.objects.filter(
        user=user, provider='github')[0].extra_data
    print(data)

    try:
        newUser = UserProfile.objects.get(user=user)
        print("User Profile", newUser)
    except UserProfile.DoesNotExist:
        print("Does not exists, creating new")
        newUser = UserProfile(
            user=user,
            experience_lvl=0,
            position=data["company"],
            is_active=True,
            github_username=data["login"],
            github_id=data["id"],
            github_url=data["html_url"],
            avatar_url=data["avatar_url"],
            gravatar_url=data["gravatar_id"]
        )
        newUser.save()
