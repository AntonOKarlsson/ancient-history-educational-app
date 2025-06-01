from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Extended user profile for tracking progress and preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    # Preferences
    preferred_language = models.CharField(max_length=10, default='is')  # Default to Icelandic

    def __str__(self):
        return f"{self.user.username}'s profile"

class HistoricalPeriod(models.Model):
    """Main historical periods for categorization"""
    name = models.CharField(max_length=100)
    name_is = models.CharField(max_length=100)  # Icelandic name
    start_year = models.IntegerField()  # Can be negative for BCE
    end_year = models.IntegerField()
    description = models.TextField()
    description_is = models.TextField()  # Icelandic description
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subperiods')

    def __str__(self):
        return self.name_is

class Civilization(models.Model):
    """Major civilizations throughout history"""
    name = models.CharField(max_length=100)
    name_is = models.CharField(max_length=100)  # Icelandic name
    start_year = models.IntegerField()  # Can be negative for BCE
    end_year = models.IntegerField()
    region = models.CharField(max_length=100)
    description = models.TextField()
    description_is = models.TextField()  # Icelandic description
    period = models.ForeignKey(HistoricalPeriod, on_delete=models.SET_NULL, null=True, related_name='civilizations')

    def __str__(self):
        return self.name_is

class Favorite(models.Model):
    """User favorites for any content type"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    content_type = models.CharField(max_length=50)  # e.g., 'person', 'event', 'deity'
    object_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    def __str__(self):
        return f"{self.user.username}'s favorite {self.content_type} ({self.object_id})"

class UserNote(models.Model):
    """Personal notes by users on any content"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    content_type = models.CharField(max_length=50)
    object_id = models.PositiveIntegerField()
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s note on {self.content_type} ({self.object_id})"
