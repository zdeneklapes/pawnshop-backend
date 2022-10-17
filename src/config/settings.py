import os
from os import path
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
BASE_DIR = Path(__file__).resolve().parent.parent

# Env
if load_dotenv(path.join(ROOT_DIR, "env", ".env.local")):
    print("ENV: local")
elif load_dotenv(path.join(ROOT_DIR, "env", ".env.heroku")):
    print("ENV: heroku")
else:  # Docker, because env folder nto available
    print("ENV: docker")

# Django Settings
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "development")
DEBUG = os.environ.get("DJANGO_DEBUG") == "True"
try:
    ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(",")
except AttributeError:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]  # nosec

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    #
    "corsheaders",
    #
    "django_crontab",
    "drf_yasg",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "wkhtmltopdf",
    #
    "authentication",
    "product",
    "customer",
    "shop",
    "statistic",
]
# "rest_framework_swagger",
# "djoser",
# "django_cron",
# "product",
# "offer",

REST_FRAMEWORK = {
    "NON_FIELD_ERRORS_KEY": "errors",
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    # "DATE_INPUT_FORMATS": ["%d/%m/%Y"],
    # 'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    # 'DEFAULT_PARSER_CLASSES': [
    #     'rest_framework.parsers.JSONParser',
    # ]
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    #
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://dev-pawnshop-frontend.vercel.app",
    "https://pawnshop-frontend.vercel.app",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "../templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# DB
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
if os.environ.get("SQL_SERVER") == "True":
    print("DB: postgress")
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("SQL_ENGINE"),
            "NAME": os.environ.get("SQL_NAME"),
            "USER": os.environ.get("SQL_USER"),
            "PASSWORD": os.environ.get("SQL_PASSWORD"),
            "HOST": os.environ.get("SQL_HOST"),
            "PORT": os.environ.get("SQL_PORT"),
        }
    }
else:
    print("DB: sqlite3")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# AUTH
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True

AUTH = False  # Required token
AUTH_USER_MODEL = "authentication.User"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=3),
    # 'ROTATE_REFRESH_TOKENS': False,
    "BLACKLIST_AFTER_ROTATION": False,
    # 'UPDATE_LAST_LOGIN': False,
    #
    # 'ALGORITHM': 'HS256',
    "SIGNING_KEY": SECRET_KEY,
    # 'VERIFYING_KEY': None,
    # 'AUDIENCE': None,
    # 'ISSUER': None,
    # 'JWK_URL': None,
    # 'LEEWAY': 0,
    #
    "AUTH_HEADER_TYPES": ("Bearer",),
    # 'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    # 'USER_ID_FIELD': 'id',
    # 'USER_ID_CLAIM': 'user_id',
    # 'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    #
    # 'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    # 'TOKEN_TYPE_CLAIM': 'token_type',
    # 'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    #
    # 'JTI_CLAIM': 'jti',
    #
    # 'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    # 'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    # 'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Configs Django
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static
STATIC_URL = "/static/"  # os.path.join(BASE_DIR, "staticfiles"),
STATICFILES_DIR = [
    os.path.join(BASE_DIR, "staticfiles"),
]
STATIC_ROOT = path.join(BASE_DIR, "staticfiles")
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Swagger
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Basic": {"type": "basic"},
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"},
    }
}

# Logging
DJANGO_LOG_LEVEL = "DEBUG"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        },
    },
}

# Cron
CRONJOBS = [
    # ("* * * * *", "django.core.management.call_command", ["update_product_status"]),
    # ("* * * * *", "config.cron.fun", f"> {path.join(BASE_DIR, 'cron_fun.txt')} 2>&1"),  # To see errors
    # (
    #     "* * * * *",
    #     "config.cron.update_product_status",
    #     f"> {path.join(BASE_DIR, 'cron_update_product_status.txt')} 2>&1",
    # ),  # To see errors
]
# Note: I think this is a bug in crontab package, because it doesn't take env vars from docker .env file while building
CRONTAB_COMMAND_PREFIX = (
    f"SQL_SERVER={os.environ.get('SQL_SERVER')} "
    f"SQL_ENGINE={os.environ.get('SQL_ENGINE')} "
    f"SQL_NAME={os.environ.get('SQL_NAME')} "
    f"SQL_USER={os.environ.get('SQL_USER')} "
    f"SQL_PASSWORD={os.environ.get('SQL_PASSWORD')} "
    f"SQL_HOST={os.environ.get('SQL_HOST')} "
    f"SQL_PORT={os.environ.get('SQL_PORT')}"
)

# PDF
WKHTMLTOPDF_CMD = os.system("which wkhtmltopdf")  # nosec
WKHTMLTOPDF_CMD_OPTIONS = {}  # nosec
