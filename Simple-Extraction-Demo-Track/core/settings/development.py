from .base import *

ALLOWED_HOSTS = ['*']

THIRD_PARTY_APPS += [
    'debug_toolbar',
]

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
