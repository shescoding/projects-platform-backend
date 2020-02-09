# Provider specific settings
SITE_ID = 2
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_STORE_TOKENS = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        # Important: do not commit this to github
        'APP': {
            'client_id': '',
            'secret': '',
            'key': ''
        },
        'SCOPE': [
            'user',
        ]
    }
}
