"""
mysite 專案的 Django 設定檔。
由 'django-admin startproject' 使用 Django 6.0.3 產生。
"""

from pathlib import Path
import os

# 建立專案內部的路徑
BASE_DIR = Path(__file__).resolve().parent.parent

# 安全警告：在正式環境中請務必保持密鑰秘密！
SECRET_KEY = 'django-insecure-k3y&&9bz#ghg$6zv8@m5!6tn5b%m=#ey!em#nd1_k!0@(9w&se'

# 安全警告：正式環境中請將 DEBUG 設為 False！
DEBUG = True

# 允許 Render 的專屬網址，以及本機測試網址
ALLOWED_HOSTS = ['pxmart-official.onrender.com', 'localhost', '127.0.0.1']

# 應用程式定義
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'members',  # 註冊功能 App
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <-- [新增] 用於在生產環境處理靜態檔案（圖片/CSS/JS）
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# 資料庫設定 (Supabase PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres.ktdiyxfdioejabztjkfi',
        'PASSWORD': 'SaveMoney20266',
        'HOST': 'aws-1-ap-southeast-1.pooler.supabase.com',
        'PORT': '6543',
    }
}

# 密碼驗證
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 語言與時區設定
LANGUAGE_CODE = 'zh-hant'
TIME_ZONE = 'Asia/Taipei'
USE_I18N = True
USE_TZ = True

# --- 靜態檔案與媒體檔案設定 ---

# 靜態檔案 (CSS, JS, 專案圖示)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# [新增] 告訴 Django 在執行 collectstatic 時將所有靜態檔案收集到這個資料夾
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 媒體檔案 (使用者上傳或下載的商品圖片)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'