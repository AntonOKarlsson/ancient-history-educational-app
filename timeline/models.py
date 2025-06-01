from django.db import models
from core.models import HistoricalPeriod, Civilization

class TimelineEvent(models.Model):
    """Historical events for the interactive timeline"""
    EVENT_CATEGORIES = [
        ('political', 'Political'),
        ('military', 'Military'),
        ('cultural', 'Cultural'),
        ('religious', 'Religious'),
        ('scientific', 'Scientific'),
        ('economic', 'Economic'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    title_is = models.CharField(max_length=200)  # Icelandic title
    description = models.TextField()
    description_is = models.TextField()  # Icelandic description
    date_start = models.IntegerField()  # Can be negative for BCE
    date_end = models.IntegerField(null=True, blank=True)  # For events that span multiple years
    period = models.ForeignKey(HistoricalPeriod, on_delete=models.SET_NULL, null=True, related_name='events')
    civilization = models.ForeignKey(Civilization, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    region = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=EVENT_CATEGORIES)
    importance = models.IntegerField(default=1)  # 1-5 scale for filtering importance levels
    latitude = models.FloatField(null=True, blank=True)  # For map placement
    longitude = models.FloatField(null=True, blank=True)  # For map placement
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_is

    class Meta:
        ordering = ['date_start', 'importance']

class TimelineRelation(models.Model):
    """Relationships between timeline events"""
    RELATION_TYPES = [
        ('cause', 'Cause'),
        ('effect', 'Effect'),
        ('related', 'Related'),
        ('concurrent', 'Concurrent'),
    ]

    from_event = models.ForeignKey(TimelineEvent, on_delete=models.CASCADE, related_name='relations_from')
    to_event = models.ForeignKey(TimelineEvent, on_delete=models.CASCADE, related_name='relations_to')
    relation_type = models.CharField(max_length=20, choices=RELATION_TYPES)
    description = models.TextField(blank=True, null=True)
    description_is = models.TextField(blank=True, null=True)  # Icelandic description

    def __str__(self):
        return f"{self.from_event} -> {self.relation_type} -> {self.to_event}"

    class Meta:
        unique_together = ('from_event', 'to_event', 'relation_type')
