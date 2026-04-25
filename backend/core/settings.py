"""
Django settings for core project (Backend Only — Azure Deployment).
"""

from pathlib import Path
from datetime import timedelta
import os
import mimetypes

mimetypes.add_type("application/javascript", ".js", True)
mimetypes.add_type("text/css", ".css", True)

from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------
# SECURITY
# ---------------------------------------------------------------
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-secret-key-change-this-in-production')
MESSAGE_ENCRYPTION_KEY = os.environ.get('MESSAGE_ENCRYPTION_KEY')

# Use DEBUG=True only if env var says so — False in production
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# ---------------------------------------------------------------
# INSTALLED APPS
# ---------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'storages',
    'corsheaders',   # ← CORS support for Vercel frontend

    # Local apps
    'api',
    'homepage',
]

# ---------------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ← Must be FIRST
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'homepage.activenowuser.ActiveUserMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# ---------------------------------------------------------------
# DATABASE
# ---------------------------------------------------------------
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# ---------------------------------------------------------------
# PASSWORD VALIDATION
# ---------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    {'NAME': 'core.validators.CustomPasswordValidator'},
]

# ---------------------------------------------------------------
# AUTHENTICATION BACKENDS
# ---------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'core.auth.CaseInsensitiveModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# ---------------------------------------------------------------
# CORS — Allow Vercel frontend to call this API
# ---------------------------------------------------------------
# During development: allow all origins
# In production: replace with your exact Vercel URL
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3000,http://127.0.0.1:5500'
).split(',')

# Allow credentials (cookies/auth headers)
CORS_ALLOW_CREDENTIALS = True

# Allow Authorization header (needed for JWT)
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# ---------------------------------------------------------------
# SECURITY — Google OAuth COOP fix
# ---------------------------------------------------------------
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '636039070454-73758bnvf06inavu947k86m1ibsh330j.apps.googleusercontent.com')

# ---------------------------------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------
# STATIC FILES (Admin only — no frontend statics served here)
# ---------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

# ---------------------------------------------------------------
# MEDIA / FILE STORAGE — Supabase S3
# ---------------------------------------------------------------
MEDIA_URL = '/media/'

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'media'
AWS_S3_ENDPOINT_URL = 'https://tyeszjpfmtmftibxibwj.supabase.co/storage/v1/s3'
AWS_S3_REGION_NAME = 'ap-southeast-1'
AWS_S3_FILE_OVERWRITE = True
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
AWS_S3_ADDRESSING_STYLE = "path"
AWS_S3_CUSTOM_DOMAIN = 'tyeszjpfmtmftibxibwj.supabase.co/storage/v1/object/public/media'
AWS_S3_VERIFY = False
AWS_S3_SIGNATURE_VERSION = 's3v4'

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ---------------------------------------------------------------
# DEFAULT PRIMARY KEY FIELD TYPE
# ---------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------
# DJANGO REST FRAMEWORK
# ---------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

# ---------------------------------------------------------------
# SIMPLE JWT
# ---------------------------------------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
}

# ---------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# ---------------------------------------------------------------
# EMAIL CONFIGURATION (SMTP)
# ---------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 465))
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'True') == 'True'
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'False') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '').strip()
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '').strip()
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER).strip()
