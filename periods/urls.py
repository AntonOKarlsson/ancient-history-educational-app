from django.urls import path
from . import views

app_name = 'periods'

urlpatterns = [
    # Main period pages
    path('<str:period_slug>/', views.period_home, name='period_home'),
    
    # Subsection pages
    path('<str:period_slug>/timeline/', views.period_timeline, name='period_timeline'),
    path('<str:period_slug>/people/', views.period_people, name='period_people'),
    path('<str:period_slug>/culture/', views.period_culture, name='period_culture'),
    path('<str:period_slug>/quiz/', views.period_quiz, name='period_quiz'),
]