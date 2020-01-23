# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = ''

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Provider specific settings
SITE_ID = 2
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        # todo: do not commit this to github
        'APP': {
            'client_id': '',
            'secret': '',
            'key': ''
        }
    }
}
