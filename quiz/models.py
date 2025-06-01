from django.db import models
from django.contrib.auth.models import User
from core.models import HistoricalPeriod
import json

class Quiz(models.Model):
    """Quiz container with metadata"""
    QUIZ_TYPES = [
        ('period', 'By Period'),
        ('topic', 'By Topic'),
        ('comprehensive', 'Comprehensive'),
        ('custom', 'Custom'),
    ]

    title = models.CharField(max_length=200)
    title_is = models.CharField(max_length=200)  # Icelandic title
    description = models.TextField()
    description_is = models.TextField()  # Icelandic description
    quiz_type = models.CharField(max_length=20, choices=QUIZ_TYPES)
    period = models.ForeignKey(HistoricalPeriod, on_delete=models.SET_NULL, null=True, blank=True, related_name='quizzes')
    topic = models.CharField(max_length=50, blank=True)  # For topic-based quizzes
    difficulty = models.IntegerField(default=1)  # 1-5 scale
    time_limit = models.IntegerField(default=0)  # In seconds, 0 means no limit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title_is

    class Meta:
        verbose_name_plural = "Quizzes"

class Question(models.Model):
    """Individual quiz questions"""
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('fill_blank', 'Fill in the Blank'),
        ('timeline_order', 'Timeline Ordering'),
        ('map_identification', 'Map Identification'),
        ('image_recognition', 'Image Recognition'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_text_is = models.TextField()  # Icelandic question text
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    image = models.ImageField(upload_to='quiz_questions/', blank=True, null=True)
    options = models.TextField(blank=True)  # JSON string of options
    correct_answer = models.TextField()  # For multiple choice, this is the index; for others, the actual answer
    explanation = models.TextField(blank=True)
    explanation_is = models.TextField(blank=True)  # Icelandic explanation
    difficulty = models.IntegerField(default=1)  # 1-5 scale
    points = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text_is[:50]

    def get_options(self):
        """Convert JSON string to Python list"""
        if self.options:
            return json.loads(self.options)
        return []

    def set_options(self, options_list):
        """Convert Python list to JSON string"""
        self.options = json.dumps(options_list)

class QuizAttempt(models.Model):
    """Record of a user's attempt at a quiz"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s attempt at {self.quiz.title_is}"

    @property
    def percentage_score(self):
        if self.max_score > 0:
            return (self.score / self.max_score) * 100
        return 0

    @property
    def time_taken(self):
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

class QuestionResponse(models.Model):
    """Individual responses to questions within a quiz attempt"""
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    user_answer = models.TextField()
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)

    def __str__(self):
        return f"Response to {self.question} in {self.attempt}"

class Achievement(models.Model):
    """Badges and achievements for users"""
    title = models.CharField(max_length=100)
    title_is = models.CharField(max_length=100)  # Icelandic title
    description = models.TextField()
    description_is = models.TextField()  # Icelandic description
    icon = models.ImageField(upload_to='achievements/')
    requirement = models.TextField()  # Description of how to earn this achievement
    requirement_is = models.TextField()  # Icelandic requirement

    def __str__(self):
        return self.title_is

class UserAchievement(models.Model):
    """Record of achievements earned by users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='users')
    date_earned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} earned {self.achievement.title_is}"

    class Meta:
        unique_together = ('user', 'achievement')
