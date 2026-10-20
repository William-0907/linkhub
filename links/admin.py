from django.contrib import admin

from .models import ClickEvent, Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'platform', 'clicks', 'order', 'created_at')
    list_filter = ('platform',)


@admin.register(ClickEvent)
class ClickEventAdmin(admin.ModelAdmin):
    list_display = ('link', 'referrer', 'created_at')
    list_filter = ('created_at',)
