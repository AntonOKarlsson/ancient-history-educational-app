from django.db import models
from core.models import HistoricalPeriod, Civilization

class Person(models.Model):
    """Historical figures including rulers, generals, philosophers, etc."""
    PERSON_CATEGORIES = [
        ('ruler', 'Ruler/Emperor'),
        ('military', 'General/Military Leader'),
        ('political', 'Politician/Statesman'),
        ('philosopher', 'Philosopher/Scholar'),
        ('religious', 'Religious Figure'),
        ('artist', 'Artist'),
        ('scientist', 'Scientist'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    name_is = models.CharField(max_length=100)  # Icelandic name
    birth_date = models.IntegerField(null=True, blank=True)  # Can be negative for BCE
    death_date = models.IntegerField(null=True, blank=True)  # Can be negative for BCE
    category = models.CharField(max_length=20, choices=PERSON_CATEGORIES)
    civilization = models.ForeignKey(Civilization, on_delete=models.SET_NULL, null=True, related_name='people')
    period = models.ForeignKey(HistoricalPeriod, on_delete=models.SET_NULL, null=True, related_name='people')
    biography = models.TextField()
    biography_is = models.TextField()  # Icelandic biography
    achievements = models.TextField(blank=True)
    achievements_is = models.TextField(blank=True)  # Icelandic achievements
    image = models.ImageField(upload_to='people/', blank=True, null=True)

    def __str__(self):
        return self.name_is

    class Meta:
        verbose_name_plural = "People"
        ordering = ['name_is']

class Deity(models.Model):
    """Gods and deities from various mythologies"""
    name = models.CharField(max_length=100)
    name_is = models.CharField(max_length=100)  # Icelandic name
    civilization = models.ForeignKey(Civilization, on_delete=models.SET_NULL, null=True, related_name='deities')
    domain = models.CharField(max_length=100)  # e.g., "God of War", "Goddess of Love"
    domain_is = models.CharField(max_length=100)  # Icelandic domain
    symbols = models.CharField(max_length=200, blank=True)
    symbols_is = models.CharField(max_length=200, blank=True)  # Icelandic symbols
    mythology = models.TextField()
    mythology_is = models.TextField()  # Icelandic mythology
    cultural_significance = models.TextField()
    cultural_significance_is = models.TextField()  # Icelandic cultural significance
    image = models.ImageField(upload_to='deities/', blank=True, null=True)

    def __str__(self):
        return self.name_is

    class Meta:
        verbose_name_plural = "Deities"
        ordering = ['name_is']

class Government(models.Model):
    """Types of government and political systems"""
    name = models.CharField(max_length=100)
    name_is = models.CharField(max_length=100)  # Icelandic name
    description = models.TextField()
    description_is = models.TextField()  # Icelandic description
    period = models.ForeignKey(HistoricalPeriod, on_delete=models.SET_NULL, null=True, related_name='governments')
    examples = models.TextField()  # Examples of civilizations using this government type
    examples_is = models.TextField()  # Icelandic examples
    characteristics = models.TextField()
    characteristics_is = models.TextField()  # Icelandic characteristics

    def __str__(self):
        return self.name_is

class MilitaryUnit(models.Model):
    """Military units from different civilizations"""
    name = models.CharField(max_length=100)
    name_is = models.CharField(max_length=100)  # Icelandic name
    civilization = models.ForeignKey(Civilization, on_delete=models.SET_NULL, null=True, related_name='military_units')
    period = models.ForeignKey(HistoricalPeriod, on_delete=models.SET_NULL, null=True, related_name='military_units')
    unit_type = models.CharField(max_length=50)  # e.g., infantry, cavalry, naval
    description = models.TextField()
    description_is = models.TextField()  # Icelandic description
    equipment = models.TextField()
    equipment_is = models.TextField()  # Icelandic equipment
    tactics = models.TextField()
    tactics_is = models.TextField()  # Icelandic tactics
    image = models.ImageField(upload_to='military_units/', blank=True, null=True)

    def __str__(self):
        return self.name_is

class Weapon(models.Model):
    """Weapons and military equipment"""
    name = models.CharField(max_length=100)
    name_is = models.CharField(max_length=100)  # Icelandic name
    weapon_type = models.CharField(max_length=50)  # e.g., sword, spear, bow
    civilization = models.ForeignKey(Civilization, on_delete=models.SET_NULL, null=True, blank=True, related_name='weapons')
    period = models.ForeignKey(HistoricalPeriod, on_delete=models.SET_NULL, null=True, related_name='weapons')
    description = models.TextField()
    description_is = models.TextField()  # Icelandic description
    usage = models.TextField()
    usage_is = models.TextField()  # Icelandic usage
    image = models.ImageField(upload_to='weapons/', blank=True, null=True)

    def __str__(self):
        return self.name_is

class Battle(models.Model):
    """Famous battles throughout history"""
    name = models.CharField(max_length=100)
    name_is = models.CharField(max_length=100)  # Icelandic name
    date = models.IntegerField()  # Can be negative for BCE
    location = models.CharField(max_length=100)
    period = models.ForeignKey(HistoricalPeriod, on_delete=models.SET_NULL, null=True, related_name='battles')
    participants = models.ManyToManyField(Civilization, related_name='battles')
    commanders = models.ManyToManyField(Person, related_name='battles')
    description = models.TextField()
    description_is = models.TextField()  # Icelandic description
    outcome = models.TextField()
    outcome_is = models.TextField()  # Icelandic outcome
    significance = models.TextField()
    significance_is = models.TextField()  # Icelandic significance
    image = models.ImageField(upload_to='battles/', blank=True, null=True)

    def __str__(self):
        return self.name_is

class CulturalTopic(models.Model):
    """Topics related to culture and society"""
    TOPIC_CATEGORIES = [
        ('daily_life', 'Daily Life'),
        ('social_classes', 'Social Classes'),
        ('trade', 'Trade & Commerce'),
        ('art', 'Art & Architecture'),
        ('literature', 'Literature & Writing'),
        ('religion', 'Religion & Rituals'),
        ('science', 'Science & Technology'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=100)
    title_is = models.CharField(max_length=100)  # Icelandic title
    category = models.CharField(max_length=20, choices=TOPIC_CATEGORIES)
    civilization = models.ForeignKey(Civilization, on_delete=models.SET_NULL, null=True, blank=True, related_name='cultural_topics')
    period = models.ForeignKey(HistoricalPeriod, on_delete=models.SET_NULL, null=True, related_name='cultural_topics')
    content = models.TextField()
    content_is = models.TextField()  # Icelandic content
    image = models.ImageField(upload_to='cultural_topics/', blank=True, null=True)

    def __str__(self):
        return self.title_is
