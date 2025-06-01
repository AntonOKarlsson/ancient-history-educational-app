from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.quiz_home, name='quiz_home'),
    path('random-history/', views.random_history_quiz, name='random_history_quiz'),
    path('by-period/', views.quiz_by_period, name='quiz_by_period'),
    path('by-topic/', views.quiz_by_topic, name='quiz_by_topic'),
    path('comprehensive/', views.comprehensive_quiz, name='comprehensive_quiz'),
    path('custom/', views.custom_quiz, name='custom_quiz'),
    path('take/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
    path('progress/', views.progress, name='progress'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
