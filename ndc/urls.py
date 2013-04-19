from django.conf.urls import patterns, include, url
from django.conf import settings
from ndc.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

if settings.CLOSED_BY_NEXON:
    urlpatterns = patterns(
        '',
        url(r'', notice),
    )
else:
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
        url(r'^comment/$', comment, name='comment'),
        url(r'^comments/(?P<ctype>\w+)/(?P<cid>\d+)/(?P<page>\d+)/$', comments, name='comments'),

        #url(r'^attend/(?P<id>\d+)/$', attend, name='attend'),

        url(r'^login/$', login, name='login'),
        url(r'^login/req/(?P<token>\w+)$', login_req, name='login_req'),
        url(r'^login/mailsent/$', login_mailsent, name='login_mailsent'),
        url(r'^logout/$', logout, name='logout'),
        url(r'^profile/$', profile, name='profile'),

        url(r'^search/', include('haystack.urls')),
        #url(r'', include('social_auth.urls')),

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
