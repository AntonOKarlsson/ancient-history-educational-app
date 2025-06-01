from django.urls import path
from . import views

app_name = 'reference'

urlpatterns = [
    path('', views.reference_home, name='reference_home'),
    # People & Names
    path('people/', views.people_list, name='people_list'),
    path('people/<int:person_id>/', views.person_detail, name='person_detail'),
    path('people/category/<str:category>/', views.people_by_category, name='people_by_category'),
    
    # Gods & Deities
    path('deities/', views.deities_list, name='deities_list'),
    path('deities/<int:deity_id>/', views.deity_detail, name='deity_detail'),
    path('deities/civilization/<str:civilization>/', views.deities_by_civilization, name='deities_by_civilization'),
    
    # Government Types
    path('governments/', views.governments_list, name='governments_list'),
    path('governments/<int:government_id>/', views.government_detail, name='government_detail'),
    
    # Military & Warfare
    path('military/', views.military_home, name='military_home'),
    path('military/units/', views.military_units, name='military_units'),
    path('military/weapons/', views.military_weapons, name='military_weapons'),
    path('military/battles/', views.battles_list, name='battles_list'),
    path('military/battles/<int:battle_id>/', views.battle_detail, name='battle_detail'),
    
    # Culture & Society
    path('culture/', views.culture_home, name='culture_home'),
    path('culture/daily-life/', views.daily_life, name='daily_life'),
    path('culture/social-classes/', views.social_classes, name='social_classes'),
    path('culture/trade/', views.trade, name='trade'),
    path('culture/art/', views.art, name='art'),
    path('culture/literature/', views.literature, name='literature'),
]