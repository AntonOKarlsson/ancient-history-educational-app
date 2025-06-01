from django.contrib import admin
from .models import (
    Person, Deity, Government, MilitaryUnit, 
    Weapon, Battle, CulturalTopic
)

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name_is', 'category', 'birth_date', 'death_date', 'civilization', 'period')
    search_fields = ('name', 'name_is', 'biography', 'biography_is', 'achievements', 'achievements_is')
    list_filter = ('category', 'civilization', 'period')
    ordering = ('name_is',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'name_is', 'category', 'birth_date', 'death_date', 'image')
        }),
        ('Affiliations', {
            'fields': ('civilization', 'period')
        }),
        ('Biography', {
            'fields': ('biography', 'biography_is', 'achievements', 'achievements_is')
        }),
    )

@admin.register(Deity)
class DeityAdmin(admin.ModelAdmin):
    list_display = ('name_is', 'civilization', 'domain_is')
    search_fields = ('name', 'name_is', 'domain', 'domain_is', 'mythology', 'mythology_is')
    list_filter = ('civilization',)
    ordering = ('name_is',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'name_is', 'civilization', 'image')
        }),
        ('Domain & Symbols', {
            'fields': ('domain', 'domain_is', 'symbols', 'symbols_is')
        }),
        ('Mythology', {
            'fields': ('mythology', 'mythology_is', 'cultural_significance', 'cultural_significance_is')
        }),
    )

@admin.register(Government)
class GovernmentAdmin(admin.ModelAdmin):
    list_display = ('name_is', 'period')
    search_fields = ('name', 'name_is', 'description', 'description_is', 'examples', 'examples_is')
    list_filter = ('period',)
    ordering = ('name_is',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'name_is', 'period')
        }),
        ('Details', {
            'fields': ('description', 'description_is', 'examples', 'examples_is', 'characteristics', 'characteristics_is')
        }),
    )

@admin.register(MilitaryUnit)
class MilitaryUnitAdmin(admin.ModelAdmin):
    list_display = ('name_is', 'unit_type', 'civilization', 'period')
    search_fields = ('name', 'name_is', 'description', 'description_is', 'equipment', 'equipment_is', 'tactics', 'tactics_is')
    list_filter = ('unit_type', 'civilization', 'period')
    ordering = ('name_is',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'name_is', 'unit_type', 'civilization', 'period', 'image')
        }),
        ('Details', {
            'fields': ('description', 'description_is', 'equipment', 'equipment_is', 'tactics', 'tactics_is')
        }),
    )

@admin.register(Weapon)
class WeaponAdmin(admin.ModelAdmin):
    list_display = ('name_is', 'weapon_type', 'civilization', 'period')
    search_fields = ('name', 'name_is', 'description', 'description_is', 'usage', 'usage_is')
    list_filter = ('weapon_type', 'civilization', 'period')
    ordering = ('name_is',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'name_is', 'weapon_type', 'civilization', 'period', 'image')
        }),
        ('Details', {
            'fields': ('description', 'description_is', 'usage', 'usage_is')
        }),
    )

class CommanderInline(admin.TabularInline):
    model = Battle.commanders.through
    extra = 1
    verbose_name = "Commander"
    verbose_name_plural = "Commanders"

class ParticipantInline(admin.TabularInline):
    model = Battle.participants.through
    extra = 1
    verbose_name = "Participant"
    verbose_name_plural = "Participants"

@admin.register(Battle)
class BattleAdmin(admin.ModelAdmin):
    list_display = ('name_is', 'date', 'location', 'period')
    search_fields = ('name', 'name_is', 'location', 'description', 'description_is', 'outcome', 'outcome_is')
    list_filter = ('period',)
    ordering = ('date',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'name_is', 'date', 'location', 'period', 'image')
        }),
        ('Details', {
            'fields': ('description', 'description_is', 'outcome', 'outcome_is', 'significance', 'significance_is')
        }),
    )
    inlines = [CommanderInline, ParticipantInline]
    exclude = ('commanders', 'participants')

@admin.register(CulturalTopic)
class CulturalTopicAdmin(admin.ModelAdmin):
    list_display = ('title_is', 'category', 'civilization', 'period')
    search_fields = ('title', 'title_is', 'content', 'content_is')
    list_filter = ('category', 'civilization', 'period')
    ordering = ('title_is',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'title_is', 'category', 'civilization', 'period', 'image')
        }),
        ('Content', {
            'fields': ('content', 'content_is')
        }),
    )
