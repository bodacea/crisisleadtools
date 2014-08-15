from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from views import *

admin.autodiscover()

urlpatterns = patterns('',
    #admin
    url(r'^admin/',  include(admin.site.urls)),

    #Splash page
    url(r'^$', direct_to_template, {'template': 'index.html'}),
##    url(r'^', include('cms.urls')),

    #Login / logout
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),

    #Manage tab groups
    url(r'^groups/', include('groups.urls')), 
    url(r'^channels/', include('channels.urls')), 
)

##if settings.DEBUG:
##    urlpatterns = patterns('',
##    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
##        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
##    url(r'', include('django.contrib.staticfiles.urls')),
##) + urlpatterns
