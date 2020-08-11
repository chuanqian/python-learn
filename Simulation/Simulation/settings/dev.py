import os, time, sys

# 第二个Simulation路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys

sys.path.insert(0, BASE_DIR)
APPS_DIR = os.path.join(BASE_DIR, 'apps')
sys.path.insert(1, APPS_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^kekymvh$m+_%a@osgyzs@=zpum1c(9x(79ox9b7b**9qz)5az'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# "122.51.26.86"
ALLOWED_HOSTS = ["122.51.26.86"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'station_info',
    'passbasic',
    "opera",
    'lib',
    'chart'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'Simulation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'Simulation.wsgi.application'

DATABASES = {
    # 仿真库
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'suzhou',
        'USER': 'dev',
        'PASSWORD': "1q2w3e@123",
        'HOST': '122.51.26.86',
        'PORT': 5532,
    },
    # 模拟数据中心库
    'slave': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test',
        'USER': 'dev',
        'PASSWORD': '1q2w3e@123',
        'HOST': '122.51.26.86',
        'PORT': 5532,
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]  # 将static加入到环境变量中
# media配置
MEDIA_URL = '/media/'
# 这个文件夹中的图片会提供给前端
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

cur_path = os.path.dirname(os.path.realpath(__file__))  # log_path是存放日志的路径
# log_path = os.path.join(os.path.dirname(cur_path), 'logs')
# if not os.path.exists(log_path): os.mkdir(log_path)  # 如果不存在这个logs文件夹，就自动创建一个
APP_ID = 89
# 统一用户管理系统
BASE_URL = f"http://62.234.70.52:8089/api/v1/apps/{APP_ID}/"
# 苏州仿真系统相关功能的id
FUNC_ID = "8901"
IP = "127.0.0.1"
PORT = "8000"
DOWNLOAD = F"http://122.51.26.86:22085/"
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        # 日志格式
        'standard': {
            'format': '[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] '
                      '[%(levelname)s]- %(message)s'},
        'simple': {  # 简单格式
            'format': '%(levelname)s %(message)s'
        },
    },
    # 过滤
    'filters': {
    },
    # 定义具体处理日志的方式
    'handlers': {
        # 默认记录所有日志
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs", 'all-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
        # 输出错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs",
                                     'error-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码
        },
        # 控制台输出
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        # 输出info日志
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs",
                                     'info-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',  # 设置默认编码
        },
    },
    # 配置用哪几种 handlers 来处理日志
    'loggers': {
        # 类型 为 django 处理所有类型的日志， 默认调用
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        # log 调用时需要当作参数传入
        'logger': {
            'handlers': ['error', 'info', 'console', 'default'],
            'level': 'INFO',
            'propagate': True
        },
    }
}
LINE_DIC = {
    "1号线": "01",
    "2号线": "02",
    "3号线": "03",
    "4号线": '04',
    "5号线": '05',
    "6号线": '06',
    "7号线": '07',
    "8号线": '08',
}

"""
http://122.51.26.86:42080/stationsimulation/#/homepage?tk=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1OTYxOTE4MzgsInVzZXJfbmFtZSI6Ijk1MjciLCJhdXRob3JpdGllcyI6WyJST0xFX1VTRVIiXSwianRpIjoiYTQ0OWYzNTItNDg0Ny00ODg3LTk5MmItYWZkZGFiOGY5MjMxIiwiY2xpZW50X2lkIjoiZm9vQ2xpZW50SWRQYXNzd29yZCIsInNjb3BlIjpbImZvbyIsInJlYWQiLCJ3cml0ZSJdfQ.Pr_f1LLG6qnLPL6huxURBeFCF8ZnwzGtUlLRaht5pKcPdwEs91WYzN4ly73R_MVcCeTFWwyUdW5yBrTwJ5HSA1Vjs2Bc8Sx5sLSaHQ9kTPdpAIGcNU9Pahu_FhOgIbHGvTN7JEquessyxPuurzfnyy8WZ7bDlMmOXIKTW0lZlGfXhkG8jd1q_hHti08nI0qaUMSZhGkwsPhorRDxqsnTNKMfWJEZ2gyzeELxTgKFlD9nnAYYXXWg7iDlkud4gT3wxiEiwY8leOr00W_Szx6_FQrhSXt50thLIS44p46Z-bIsQXNAUfCgYqb4O-F8lvGspal8fC3VzXr51LlmVjlefQ
"""
