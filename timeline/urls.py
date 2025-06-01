from django.urls import path
from . import views

app_name = 'timeline'

urlpatterns = [
    path('', views.timeline, name='timeline'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('filter/', views.filter_events, name='filter_events'),
]