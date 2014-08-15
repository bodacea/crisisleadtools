from django.conf.urls import patterns, url

from groups import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^groupsandbox$', views.sandbox, name="groupsandbox"),
    url(r'^action$', views.action, name="action"),
    url(r'^addgroup$', views.addgroup, name="addgroup"),
    url(r'^(?P<groupid>\d+)$', views.viewgroup, name="viewgroup"),
    url(r'^contact/$', views.contact, name="contact"),
    url(r'^nothereyet/$', views.nothereyet, name="nothereyet"),
##    url(r'^xxx$', views.group, name="group"),    
##    url(r'^xxx/channels$', views.channels, name="groupchannels"),    
)

