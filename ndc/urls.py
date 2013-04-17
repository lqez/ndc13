from django.conf.urls import patterns, include, url
from ndc.views import *
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', home, name='home'),
    url(r'^timetable/$', timetable, name='timetable'),
    url(r'^speakers/$', speaker_list.as_view(), name='speakers'),
    url(r'^speaker/(?P<pk>\d+)/$', speaker_detail.as_view(), name='speaker'),
    url(r'^companies/$', company_list.as_view(), name='companies'),
    url(r'^company/(?P<pk>\d+)/$', company_detail.as_view(), name='company'),
    url(r'^sessions/$', session_list.as_view(), name='sessions'),
    url(r'^session/(?P<pk>\d+)/$', session_detail.as_view(), name='session'),

    url(r'^search/', include('haystack.urls')),
    url(r'^about/$', about, name='about'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

)

# for development
if settings.DEBUG:
    urlpatterns = urlpatterns + patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
    )
