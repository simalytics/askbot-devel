"""
main url configuration file for the askbot site
"""
from django.conf import settings
from django.conf.urls.defaults import handler404
from django.conf.urls.defaults import handler500
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse

admin.autodiscover()

if getattr(settings, 'ASKBOT_MULTILINGUAL', False) == True:
    from django.conf.urls.i18n import i18n_patterns
    urlpatterns = i18n_patterns('',
        (r'%s' % settings.ASKBOT_URL, include('askbot.urls'))
    )
else:
    urlpatterns = patterns('',
        (r'%s' % settings.ASKBOT_URL, include('askbot.urls'))
    )

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
    #(r'^cache/', include('keyedcache.urls')), - broken views disable for now
    #(r'^settings/', include('askbot.deps.livesettings.urls')),
    (r'^followit/', include('followit.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^robots.txt$', include('robots.urls')),
    (r'mu-c6e91be8-552c03a2-a6a38111-a6ea6071/', lambda s: HttpResponse("42")),
    url( # TODO: replace with django.conf.urls.static ?
        r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT.replace('\\','/')},
    ),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
                    url(r'^rosetta/', include('rosetta.urls')),
                )
