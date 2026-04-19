"""
mysite 專案的 Django 設定檔。

由 'django-admin startproject' 使用 Django 6.0.3 產生。
"""

from pathlib import Path

# 建立專案內部的路徑，例如：BASE_DIR / '子目錄'。
BASE_DIR = Path(__file__).resolve().parent.parent


# 快速啟動開發設定 - 不適合用於實際正式環境
# 詳見：https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# 安全警告：在正式環境中請務必保持密鑰秘密！
SECRET_KEY = 'django-insecure-k3y&&9bz#ghg$6zv8@m5!6tn5b%m=#ey!em#nd1_k!0@(9w&se'

# 安全警告：正式環境中請將 DEBUG 設為 False！
DEBUG = True

# 允許存取的域名（正式上線時需填入網址）
ALLOWED_HOSTS = []


# 應用程式定義（在此註冊你的 App）

INSTALLED_APPS = [
    'django.contrib.admin',        # 管理員後台
    'django.contrib.auth',         # 認證系統
    'django.contrib.contenttypes', # 內容類型框架
    'django.contrib.sessions',     # 會話管理
    'django.contrib.messages',     # 訊息框架
    'django.contrib.staticfiles',  # 靜態檔案管理
    'members',                     # 你剛剛建立的註冊功能 App
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 總路由設定檔路徑
ROOT_URLCONF = 'mysite.urls'

# mysite/settings.py

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 修改下面這一行，加入 BASE_DIR / 'templates'
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


# 資料庫設定
# 詳見：https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# --- 這裡幫你改成了 Supabase 的連線設定 ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres.ktdiyxfdioejabztjkfi',
        'PASSWORD': 'SaveMoney20266',  # ⚠️ 這裡請填入你創 Supabase 專案時的密碼
        'HOST': 'aws-1-ap-southeast-1.pooler.supabase.com',
        'PORT': '6543',
    }
}


# 密碼驗證
# 詳見：https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# 語言與時區設定（國際化）
# 詳見：https://docs.djangoproject.com/en/6.0/topics/i18n/

# 建議改成正體中文
LANGUAGE_CODE = 'zh-hant'

# 建議改成台灣時區
TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_TZ = True


# 靜態檔案設定 (CSS, JavaScript, Images)
# 詳見：https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# 預設自動產生的主鍵欄位類型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'