"""
Django settings for midio_mall project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

# ctrl+k 来进行 add 和 commit操作
# ctrl+shift+k来进行 push操作
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bw$npjbx*uw@ch=@uu%ea#6q%p$-&4*v8x13645^li1qz9wous'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['www.meiduo.site', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.user',
    'apps.areas',
    #CORS
    'corsheaders',
    'apps.verifications',
    'apps.goods',
    'apps.contents',
    'haystack', # 全文检索
]

MIDDLEWARE = [
    #CORS中间层
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'midio_mall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'midio_mall.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 3306,  # 数据库端口
        'USER': 'itcast',  # 数据库用户名
        'PASSWORD': '123456',  # 数据库用户密码
        'NAME': 'midio_mall_42'  # 数据库名字

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

###########################django_redis###################################
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",     #默认的redis配置项，采用0号redis库
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            # "PASSWORD": "foobared" # redis密码
        },

    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",     #session采用1号redis库
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },

    "imagecode": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",  # image采用1号redis库
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },

}
# # session存储机制 使用redis保存
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# # 使用名为session的redis配置项存储redis数据
# SESSION_CACHE_ALIAS = "session"
# session使用的存储方式
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# 指明使用哪一个库保存session数据
SESSION_CACHE_ALIAS = "session"


# ##################################log日志###################################

# 配置工程日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False, # 是否禁用已经存在的日志器
    'formatters': {  # 输出日志的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': { # 日志的处理方式
        'console': {  # 终端输出日志
            'level': 'INFO',  # 大于INFO级别，才输出
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple' # 输出简单的样式
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR , "logs/meiduo.log"),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,  # 文件最多存储 300M 的内存   日志文件满了，他会自动新建meiduo1 meiduo2
            'backupCount': 10, # 最多十个文件
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'], # 可以同时在终端跟文件中输出
            'propagate': True,
            'level;':'INFO' # 日至输出的最低级别
        },
    }
}

#############################################################
#通过提供一个值给AUTH_USER_MODEL设置 ， 指向自定义的模型，Django允许你覆盖默认的User模型：
#AUTH_USER_MODEL='appname.UserModel' 这个值是app名字(apps/user)和模块名，中间使用点连接，不用指定模块名。这点要注意。
AUTH_USER_MODEL= 'user.User'

#######CORS#################################
# 配置访问规则或白名单:
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'http://www.midio.com:8080',
)
# 允许所有域名跨域(优先选择) /允许跨域源 二选一 allow..：一般用这个，新出来的
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

##################邮箱配置######################
# 固定写法设置Email引擎
EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com' # 163邮箱 SMTP 服务器地址
EMAIL_PORT = 25 # SMTP服务的端口号
EMAIL_HOST_USER = 'lw880699@163.com' #你的邮箱，邮件发送者的邮箱
EMAIL_HOST_PASSWORD = 'WSRODUFFPQKKOFWO' #你申请的授权码（略）
EMAIL_USE_TLS = False #与SMTP服务器通信时,是否启用安全模式

#######################################################

#指定自定义的DJANGO文集存储类
DEFAULT_FILE_STORAGE = 'utils.fastdfs.storage.MyStorage'



#######################  haystack  ##########################

# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://192.168.44.130:9200/', # Elasticsearch服务器ip地址，端口号固定为9200
        'INDEX_NAME': 'midio_mall', # Elasticsearch建立的索引库的名称
    },
}

# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 设置搜索的内容每页多少条
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 5 #每页五条

#########################################################

