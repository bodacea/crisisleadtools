from django.conf.urls import patterns, url

from channels import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^sandbox$', views.sandbox, name="sandbox"),
    url(r'^action$', views.action, name="action"),
    url(r'^add$', views.addchannel, name="addchannel"),
    url(r'^(?P<channelid>\d+)$', views.viewchannel, name="viewchannel"),
    url(r'^createremote$', views.create_skypechat, name="createremote"),
    url(r'^summarise$', views.upload_skypechat, name="summarise"),
    url(r'^friendall$', views.friend_all, name="friendall"),
    url(r'^nothereyet/$', views.nothereyet, name="nothereyet"),
##    url(r'^xxx$', views.channel, name="channel"),    
##    url(r'^load$', views.channel_load, name="channelload"),    
##    url(r'^save$', views.channel_save, name="channelsave"),    
##    url(r'^create$', views.channel_create, name="channelcreate"),    
)
