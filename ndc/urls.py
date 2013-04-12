from django.conf.urls import patterns, include, url
from ndc.views import *
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^speakers/$', speaker_list.as_view(), name='speakers'),
    url(r'^speaker/(?P<pk>\d+)$', speaker_detail.as_view(), name='speaker'),
    url(r'^sessions/$', session_list.as_view(), name='sessions'),
    url(r'^session/(?P<pk>\d+)$', session_detail.as_view(), name='session'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # for development
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
)
