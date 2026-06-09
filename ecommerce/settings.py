import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env (local)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ========== SÉCURITÉ ==========
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("La variable d'environnement SECRET_KEY n'est pas définie")

DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Récupère ALLOWED_HOSTS depuis l'environnement (ex: ".onrender.com,localhost")
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ========== APPLICATIONS INSTALLÉES ==========
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Applications du projet
    'store',
    'cart',
    'orders',
    'payments',
    'accounts',
    # Third‑party
    'stripe',
]

# ========== MIDDLEWARE ==========
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # fichiers statiques en production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

# ========== TEMPLATES ==========
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]

# ========== BASE DE DONNÉES ==========
# Pour Render : on utilise SQLite (fichier db.sqlite3 déjà présent dans le dépôt)
# Cela permet un déploiement immédiat sans configurer PostgreSQL.
# Attention : les données seront perdues à chaque redémarrage du service (stockage éphémère).
# Pour une production réelle, remplacez par PostgreSQL (voir commentaire plus bas).
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Option PostgreSQL (décommentez et supprimez le bloc ci-dessus si vous avez une base Render PostgreSQL)
# import dj_database_url
# DATABASES = {
#     'default': dj_database_url.config(
#         default='sqlite:///db.sqlite3',
#         conn_max_age=600,
#         ssl_require=True
#     )
# }

# ========== FICHIERS STATIQUES ET MÉDIAS ==========
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ========== STRIPE ==========
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

# ========== KKIAPAY ==========
KKIAPAY_PUBLIC_KEY = os.getenv('KKIAPAY_PUBLIC_KEY')
KKIAPAY_PRIVATE_KEY = os.getenv('KKIAPAY_PRIVATE_KEY')
KKIAPAY_SECRET_KEY = os.getenv('KKIAPAY_SECRET_KEY')
KKIAPAY_SANDBOX = os.getenv('KKIAPAY_SANDBOX', 'True') == 'True'

# ========== EMAIL ==========
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@dipitashop.com')

# ========== SÉCURITÉ PRODUCTION ==========
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True