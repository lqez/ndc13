from django.contrib import admin
from ndc.models import Tag, Room, SessionDate, SessionTime, Company, Speaker, Session
from ndc.models import Comment, EmailToken, Profile


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'uid', 'image', 'is_category',)
    search_fields = ('name',)
admin.site.register(Tag, TagAdmin)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
admin.site.register(Room, RoomAdmin)


class SessionDateAdmin(admin.ModelAdmin):
    list_display = ('id', 'day',)
admin.site.register(SessionDate, SessionDateAdmin)


class SessionTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'begin', 'end',)
    ordering = ('begin',)
admin.site.register(SessionTime, SessionTimeAdmin)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    ordering = ('name',)
    search_fields = ('name',)
admin.site.register(Company, CompanyAdmin)


class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'twitter',)
    ordering = ('name',)
    search_fields = ('name', 'company__name', 'twitter',)
admin.site.register(Speaker, SpeakerAdmin)


class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'desc', 'html_get_speakers', 'html_get_companies', 'date', 'room')
    ordering = ('id',)
    filter_horizontal = ('tags', 'times', )
    search_fields = ('name', 'speakers__name', 'speakers__company__name', 'desc',)
admin.site.register(Session, SessionAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'msg', 'session', 'speaker', 'created')
    ordering = ('-id',)
    raw_id_fields = ('user',)
    search_fields = ('user__name', 'session__name', 'speaker__name',)
admin.site.register(Comment, CommentAdmin)


class EmailTokenAdmin(admin.ModelAdmin):
    list_display = ('email', 'token', 'created')
    search_fields = ('email',)
admin.site.register(EmailToken, EmailTokenAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nick', 'use_gravatar')
    raw_id_fields = ('user',)
    search_fields = ('user__email', 'nick',)
admin.site.register(Profile, ProfileAdmin)
