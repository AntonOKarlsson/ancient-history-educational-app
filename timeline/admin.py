from django.contrib import admin
from .models import TimelineEvent, TimelineRelation

@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ('title_is', 'date_start', 'date_end', 'period', 'civilization', 'category', 'importance')
    search_fields = ('title', 'title_is', 'description', 'description_is', 'region')
    list_filter = ('period', 'civilization', 'category', 'importance')
    ordering = ('date_start', 'importance')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'title_is', 'description', 'description_is')
        }),
        ('Timeline Information', {
            'fields': ('date_start', 'date_end', 'period', 'civilization', 'region', 'category', 'importance')
        }),
        ('Map Information', {
            'fields': ('latitude', 'longitude', 'image')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(TimelineRelation)
class TimelineRelationAdmin(admin.ModelAdmin):
    list_display = ('from_event', 'relation_type', 'to_event')
    search_fields = ('from_event__title', 'to_event__title', 'description', 'description_is')
    list_filter = ('relation_type',)
