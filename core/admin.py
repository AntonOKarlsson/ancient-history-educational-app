from django.contrib import admin
from .models import UserProfile, HistoricalPeriod, Civilization, Favorite, UserNote

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'last_login', 'preferred_language')
    search_fields = ('user__username', 'user__email')
    list_filter = ('preferred_language', 'created_at')

@admin.register(HistoricalPeriod)
class HistoricalPeriodAdmin(admin.ModelAdmin):
    list_display = ('name_is', 'name', 'start_year', 'end_year', 'parent')
    search_fields = ('name', 'name_is', 'description', 'description_is')
    list_filter = ('parent',)
    ordering = ('start_year',)

@admin.register(Civilization)
class CivilizationAdmin(admin.ModelAdmin):
    list_display = ('name_is', 'name', 'start_year', 'end_year', 'region', 'period')
    search_fields = ('name', 'name_is', 'region', 'description', 'description_is')
    list_filter = ('region', 'period')
    ordering = ('start_year',)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id', 'created_at')
    search_fields = ('user__username', 'content_type')
    list_filter = ('content_type', 'created_at')
    ordering = ('-created_at',)

@admin.register(UserNote)
class UserNoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id', 'created_at', 'updated_at')
    search_fields = ('user__username', 'content_type', 'note')
    list_filter = ('content_type', 'created_at')
    ordering = ('-updated_at',)
