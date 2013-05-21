## Django se#ttings for ASKBOT enabled project.
import os.path
import logging
import sys
import askbot
import site

import dj_database_url

#sys.stderr.write('\n'.join(sorted(sys.path)))

#this line is added so that we can import pre-packaged askbot dependencies
ASKBOT_ROOT = os.path.abspath(os.path.dirname(askbot.__file__))
site.addsitedir(os.path.join(ASKBOT_ROOT, 'deps'))

DEBUG = False#set to True to enable debugging
TEMPLATE_DEBUG = False#keep false when debugging jinja2 templates
INTERNAL_IPS = ('127.0.0.1',)

ADMINS = (
    ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
#        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'testdb',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'parkside',                  # Not used with sqlite3.
        'HOST': 'askbot-test.ch1lffqhjedf.us-east-1.rds.amazonaws.com',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}

#DATABASES['default'] = dj_database_url.config()
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#outgoing mail server settings
SERVER_EMAIL = ''
DEFAULT_FROM_EMAIL = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_SUBJECT_PREFIX = ''
EMAIL_HOST=''
EMAIL_PORT=''
EMAIL_USE_TLS=False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#incoming mail settings
#after filling out these settings - please
#go to the site's live settings and enable the feature
#"Email settings" -> "allow asking by email"
#
#   WARNING: command post_emailed_questions DELETES all 
#            emails from the mailbox each time
#            do not use your personal mail box here!!!
#
IMAP_HOST = ''
IMAP_HOST_USER = ''
IMAP_HOST_PASSWORD = ''
IMAP_PORT = ''
IMAP_USE_TLS = False

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
LANGUAGE_CODE = 'en'

# Absolute path to the directory that holds uploaded media
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'askbot', 'upfiles')
MEDIA_URL = '/upfiles/'

#STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'askbot.storage.CachedS3BotoStorage'
#STATICFILES_STORAGE = 'django.core.files.storage.FileSystemStorage'
AWS_ACCESS_KEY_ID = 'AKIAJEGKM6KS2VXONDDA'
AWS_SECRET_ACCESS_KEY = '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' 
AWS_STORAGE_BUCKET_NAME = 'askbot-test'

AWS_QUERYSTRING_AUTH = False

#STATIC_URL = '/m/'#this must be different from MEDIA_URL
STATIC_URL = 'https://s3.amazonaws.com/%s/static/' % AWS_STORAGE_BUCKET_NAME #this must be different from MEDIA_URL

PROJECT_ROOT = os.path.dirname(__file__)
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# Make up some unique string, and don't share it with anybody.
SECRET_KEY = '2ffcd89c70e921cb0d0c9b7c038a9f21'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'askbot.skins.loaders.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
    #'django.template.loaders.eggs.load_template_source',
)


MIDDLEWARE_CLASSES = (
    #'django.middleware.gzip.GZipMiddleware',
    #'askbot.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.middleware.sqlprint.SqlPrintingMiddleware',

    #below is askbot stuff for this tuple
    'askbot.middleware.anon_user.ConnectToSessionMessagesMiddleware',
    'askbot.middleware.forum_mode.ForumModeMiddleware',
    'askbot.middleware.cancel.CancelActionMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'askbot.middleware.view_log.ViewLogMiddleware',
    'askbot.middleware.spaceless.SpacelessMiddleware',
)


ROOT_URLCONF = os.path.basename(os.path.dirname(__file__)) + '.urls'


#UPLOAD SETTINGS
FILE_UPLOAD_TEMP_DIR = os.path.join(
                                os.path.dirname(__file__), 
                                'tmp'
                            ).replace('\\','/')

FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)
ASKBOT_ALLOWED_UPLOAD_FILE_TYPES = ('.jpg', '.jpeg', '.gif', '.bmp', '.png', '.tiff')
ASKBOT_MAX_UPLOAD_FILE_SIZE = 1024 * 1024 #result in bytes
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


#TEMPLATE_DIRS = (,) #template have no effect in askbot, use the variable below
#ASKBOT_EXTRA_SKINS_DIR = #path to your private skin collection
#take a look here http://askbot.org/en/question/207/

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'askbot.context.application_settings',
    #'django.core.context_processors.i18n',
    'askbot.user_messages.context_processors.user_messages',#must be before auth
    'django.contrib.auth.context_processors.auth', #this is required for the admin app
    'django.core.context_processors.csrf', #necessary for csrf protection
)


INSTALLED_APPS = (
    'longerusername',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    #all of these are needed for the askbot
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    #'debug_toolbar',
    #Optional, to enable haystack search
    #'haystack',
    'compressor',
    'askbot',
    'askbot.deps.django_authopenid',
    #'askbot.importers.stackexchange', #se loader
    'south',
    'askbot.deps.livesettings',
    'keyedcache',
    'robots',
    'django_countries',
    'djcelery',
    'djkombu',
    'followit',
    'tinymce',
    'group_messaging',
    'gunicorn',
    'storages',
    #'coffin_offline_compressor',
    #'avatar',#experimental use git clone git://github.com/ericflo/django-avatar.git$
)


#setup memcached for production use!
#see http://docs.djangoproject.com/en/1.1/topics/cache/ for details
CACHE_BACKEND = 'locmem://'
#CACHE_BACKEND = 'memcached://127.0.0.1:11211' # local memcached instance
#needed for django-keyedcache
CACHE_TIMEOUT = 6000
#sets a special timeout for livesettings if you want to make them different
LIVESETTINGS_CACHE_TIMEOUT = CACHE_TIMEOUT
CACHE_PREFIX = 'askbot' #make this unique
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
#If you use memcache you may want to uncomment the following line to enable memcached based sessions
#SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'askbot.deps.django_authopenid.backends.AuthBackend',
)

#logging settings
#LOG_FILENAME = 'askbot.log'
#logging.basicConfig(
#    filename=os.path.join(os.path.dirname(__file__), 'log', LOG_FILENAME),
#    level=logging.CRITICAL,
#    format='%(pathname)s TIME: %(asctime)s MSG: %(filename)s:%(funcName)s:%(lineno)d %(message)s',
#)

###########################
#
#   this will allow running your forum with url like http://site.com/forum
#
#   ASKBOT_URL = 'forum/'
#
ASKBOT_URL = '' #no leading slash, default = '' empty string
ASKBOT_TRANSLATE_URL = True #translate specific URLs
_ = lambda v:v #fake translation function for the login url
LOGIN_URL = '/%s%s%s' % (ASKBOT_URL,_('account/'),_('signin/'))
LOGIN_REDIRECT_URL = ASKBOT_URL #adjust, if needed
#note - it is important that upload dir url is NOT translated!!!
#also, this url must not have the leading slash
ALLOW_UNICODE_SLUGS = False
ASKBOT_USE_STACKEXCHANGE_URLS = False #mimic url scheme of stackexchange

#Celery Settings
BROKER_TRANSPORT = "djkombu.transport.DatabaseTransport"
CELERY_ALWAYS_EAGER = True

import djcelery
djcelery.setup_loader()
DOMAIN_NAME = ''

CSRF_COOKIE_NAME = '_csrf'
#https://docs.djangoproject.com/en/1.3/ref/contrib/csrf/
#CSRF_COOKIE_DOMAIN = DOMAIN_NAME

STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")
STATICFILES_DIRS = (
    ('default/media', os.path.join(ASKBOT_ROOT, 'media')),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

RECAPTCHA_USE_SSL = True

#HAYSTACK_SETTINGS
ENABLE_HAYSTACK_SEARCH = False
HAYSTACK_SITECONF = 'askbot.search.haystack'
#more information
#http://django-haystack.readthedocs.org/en/v1.2.7/settings.html
HAYSTACK_SEARCH_ENGINE = 'simple'

TINYMCE_COMPRESSOR = True 
TINYMCE_SPELLCHECKER = False
TINYMCE_JS_ROOT = os.path.join(STATIC_ROOT, 'default/media/js/tinymce/')
#TINYMCE_JS_URL = STATIC_URL + 'default/media/js/tinymce/tiny_mce.js'
TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'askbot_imageuploader,askbot_attachment',
    'convert_urls': False,
    'theme': 'advanced',
    'content_css': STATIC_URL + 'default/media/style/tinymce/content.css',
    'force_br_newlines': True,
    'force_p_newlines': False,
    'forced_root_block': '',
    'mode' : 'textareas',
    'oninit': "TinyMCE.onInitHook",
    'plugins': 'askbot_imageuploader,askbot_attachment',
    'theme_advanced_toolbar_location' : 'top',
    'theme_advanced_toolbar_align': 'left',
    'theme_advanced_buttons1': 'bold,italic,underline,|,bullist,numlist,|,undo,redo,|,link,unlink,askbot_imageuploader,askbot_attachment',
    'theme_advanced_buttons2': '',
    'theme_advanced_buttons3' : '',
    'theme_advanced_path': False,
    'theme_advanced_resizing': True,
    'theme_advanced_resize_horizontal': False,
    'theme_advanced_statusbar_location': 'bottom',
    'width': '730',
    'height': '250'
}

#delayed notifications, time in seconds, 15 mins by default
NOTIFICATION_DELAY_TIME = 60 * 15 

GROUP_MESSAGING = {
    'BASE_URL_GETTER_FUNCTION': 'askbot.models.user_get_profile_url',
    'BASE_URL_PARAMS': {'section': 'messages', 'sort': 'inbox'}
}

ASKBOT_MULTILINGUAL = False

ASKBOT_CSS_DEVEL = False
if 'ASKBOT_CSS_DEVEL' in locals() and ASKBOT_CSS_DEVEL == True:
    COMPRESS_PRECOMPILERS = (
        ('text/less', 'lessc {infile} {outfile}'),
    )

COMPRESS_JS_FILTERS = []
COMPRESS_PARSER = 'compressor.parser.HtmlParser' 
JINJA2_EXTENSIONS = ('compressor.contrib.jinja2ext.CompressorExtension',)

COMPRESS_ROOT = STATIC_ROOT
COMPRESS_STORAGE = STATICFILES_STORAGE
COMPRESS_OFFLINE = True
COMPRESS_URL = STATIC_URL

COMPRESS_CSS_FILTERS = (
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
)
