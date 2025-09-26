import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

# .env-driven settings
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY", "dev-not-secure")

# Better default for production:
DEBUG = os.getenv("DEBUG", "0") in ("1", "true", "True")

ALLOWED_HOSTS = [h.strip() for h in os.getenv(
    "ALLOWED_HOSTS", "127.0.0.1,localhost"
).split(",")]

CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.getenv(
    "CSRF_TRUSTED_ORIGINS", ""
).split(",") if o.strip()]

# Heroku behind a proxy
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
    'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
    'core','bookings',
    'django_filters',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'mountain_tours_v2.urls'
TEMPLATES = [{
    'BACKEND':'django.template.backends.django.DjangoTemplates',
    'DIRS':[BASE_DIR/'templates'],
    'APP_DIRS':True,
    'OPTIONS':{'context_processors':[
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]
WSGI_APPLICATION = 'mountain_tours_v2.wsgi.application'
ASGI_APPLICATION = 'mountain_tours_v2.asgi.application'

# ----- Database (Postgres on Heroku via DATABASE_URL; SQLite locally) -----
DATABASE_URL = os.getenv("DATABASE_URL", "")
if DATABASE_URL:
    # use SSL in production (when DEBUG is false)
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=not DEBUG
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE':'django.db.backends.sqlite3',
            'NAME': BASE_DIR/'db.sqlite3'
        }
    }
# --------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS=[
    {'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
LANGUAGE_CODE='en-gb'
TIME_ZONE='Europe/London'
USE_I18N=True
USE_TZ=True
STATIC_URL='/static/'
STATICFILES_DIRS=[BASE_DIR/'assets']
STATIC_ROOT=BASE_DIR/'staticfiles'
STATICFILES_STORAGE='whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
LOGIN_REDIRECT_URL='index'
LOGOUT_REDIRECT_URL='index'

# --- Email feature flag & defaults ---

ENABLE_EMAIL_NOTIFICATIONS = True

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend"  # dev-friendly
)
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@example.com")

# Optional SMTP (leave blank in dev; set via Heroku config when needed)
EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "1") == "1"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
