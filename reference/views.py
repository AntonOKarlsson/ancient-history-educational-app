from django.shortcuts import render, get_object_or_404
from .models import (
    Person, Deity, Government, MilitaryUnit, 
    Weapon, Battle, CulturalTopic
)
from core.models import HistoricalPeriod, Civilization

# Reference Home
def reference_home(request):
    """Main reference section landing page - Hver-er-hver section"""
    # Get all civilizations
    civilizations = Civilization.objects.all().order_by('name_is')

    # Dictionary to store people and deities for each civilization
    civilization_data = {}

    # Get people and deities for each civilization
    for civ in civilizations:
        people = Person.objects.filter(civilization=civ).order_by('name_is')
        deities = Deity.objects.filter(civilization=civ).order_by('name_is')

        if people.exists() or deities.exists():
            civilization_data[civ] = {
                'people': people,
                'deities': deities
            }

    # Get all people and deities without a civilization
    people_without_civ = Person.objects.filter(civilization=None).order_by('name_is')
    deities_without_civ = Deity.objects.filter(civilization=None).order_by('name_is')

    # For backward compatibility, also get Greek civilization specifically
    try:
        greek_civ = Civilization.objects.get(name_is='Forngrikkir')
        greek_people = Person.objects.filter(civilization=greek_civ).order_by('name_is')
        greek_deities = Deity.objects.filter(civilization=greek_civ).order_by('name_is')
    except Civilization.DoesNotExist:
        greek_people = []
        greek_deities = []

    context = {
        'civilizations': civilizations,
        'civilization_data': civilization_data,
        'people_without_civ': people_without_civ,
        'deities_without_civ': deities_without_civ,
        'greek_people': greek_people,
        'greek_deities': greek_deities,
        'people_count': Person.objects.count(),
        'deities_count': Deity.objects.count(),
        'governments_count': Government.objects.count(),
        'military_units_count': MilitaryUnit.objects.count(),
        'weapons_count': Weapon.objects.count(),
        'battles_count': Battle.objects.count(),
        'cultural_topics_count': CulturalTopic.objects.count(),
    }

    return render(request, 'reference/reference_home.html', context)

# People & Names views
def people_list(request):
    """List of historical people"""
    people = Person.objects.all().order_by('name_is')
    categories = Person.PERSON_CATEGORIES
    periods = HistoricalPeriod.objects.all().order_by('start_year')
    civilizations = Civilization.objects.all().order_by('name_is')

    context = {
        'people': people,
        'categories': categories,
        'periods': periods,
        'civilizations': civilizations,
    }
    return render(request, 'reference/people_list.html', context)

def person_detail(request, person_id):
    """Detailed view of a single person"""
    person = get_object_or_404(Person, id=person_id)

    # Get battles this person commanded
    battles = person.battles.all()

    context = {
        'person': person,
        'battles': battles,
    }
    return render(request, 'reference/person_detail.html', context)

def people_by_category(request, category):
    """List of people filtered by category"""
    people = Person.objects.filter(category=category).order_by('name_is')
    category_display = dict(Person.PERSON_CATEGORIES).get(category, category)

    context = {
        'people': people,
        'category': category,
        'category_display': category_display,
    }
    return render(request, 'reference/people_by_category.html', context)

# Gods & Deities views
def deities_list(request):
    """List of deities from various mythologies"""
    deities = Deity.objects.all().order_by('name_is')
    civilizations = Civilization.objects.all().order_by('name_is')

    context = {
        'deities': deities,
        'civilizations': civilizations,
    }
    return render(request, 'reference/deities_list.html', context)

def deity_detail(request, deity_id):
    """Detailed view of a single deity"""
    deity = get_object_or_404(Deity, id=deity_id)

    context = {
        'deity': deity,
    }
    return render(request, 'reference/deity_detail.html', context)

def deities_by_civilization(request, civilization):
    """List of deities filtered by civilization"""
    civilization_obj = get_object_or_404(Civilization, id=civilization)
    deities = Deity.objects.filter(civilization=civilization_obj).order_by('name_is')

    context = {
        'deities': deities,
        'civilization': civilization_obj,
    }
    return render(request, 'reference/deities_by_civilization.html', context)

# Government Types views
def governments_list(request):
    """List of government types"""
    governments = Government.objects.all().order_by('name_is')
    periods = HistoricalPeriod.objects.all().order_by('start_year')

    context = {
        'governments': governments,
        'periods': periods,
    }
    return render(request, 'reference/governments_list.html', context)

def government_detail(request, government_id):
    """Detailed view of a single government type"""
    government = get_object_or_404(Government, id=government_id)

    context = {
        'government': government,
    }
    return render(request, 'reference/government_detail.html', context)

# Military & Warfare views
def military_home(request):
    """Military & Warfare section landing page"""
    context = {
        'units_count': MilitaryUnit.objects.count(),
        'weapons_count': Weapon.objects.count(),
        'battles_count': Battle.objects.count(),
    }
    return render(request, 'reference/military_home.html', context)

def military_units(request):
    """List of military units"""
    units = MilitaryUnit.objects.all().order_by('name_is')
    civilizations = Civilization.objects.all().order_by('name_is')
    periods = HistoricalPeriod.objects.all().order_by('start_year')

    context = {
        'units': units,
        'civilizations': civilizations,
        'periods': periods,
    }
    return render(request, 'reference/military_units.html', context)

def military_weapons(request):
    """List of weapons and military equipment"""
    weapons = Weapon.objects.all().order_by('name_is')
    civilizations = Civilization.objects.all().order_by('name_is')
    periods = HistoricalPeriod.objects.all().order_by('start_year')

    context = {
        'weapons': weapons,
        'civilizations': civilizations,
        'periods': periods,
    }
    return render(request, 'reference/military_weapons.html', context)

def battles_list(request):
    """List of famous battles"""
    battles = Battle.objects.all().order_by('date')
    periods = HistoricalPeriod.objects.all().order_by('start_year')

    context = {
        'battles': battles,
        'periods': periods,
    }
    return render(request, 'reference/battles_list.html', context)

def battle_detail(request, battle_id):
    """Detailed view of a single battle"""
    battle = get_object_or_404(Battle, id=battle_id)

    context = {
        'battle': battle,
    }
    return render(request, 'reference/battle_detail.html', context)

# Culture & Society views
def culture_home(request):
    """Culture & Society section landing page"""
    daily_life = CulturalTopic.objects.filter(category='daily_life').count()
    social_classes = CulturalTopic.objects.filter(category='social_classes').count()
    trade = CulturalTopic.objects.filter(category='trade').count()
    art = CulturalTopic.objects.filter(category='art').count()
    literature = CulturalTopic.objects.filter(category='literature').count()

    context = {
        'daily_life_count': daily_life,
        'social_classes_count': social_classes,
        'trade_count': trade,
        'art_count': art,
        'literature_count': literature,
    }
    return render(request, 'reference/culture_home.html', context)

def daily_life(request):
    """Daily life topics"""
    topics = CulturalTopic.objects.filter(category='daily_life').order_by('title_is')
    civilizations = Civilization.objects.all().order_by('name_is')
    periods = HistoricalPeriod.objects.all().order_by('start_year')

    context = {
        'topics': topics,
        'civilizations': civilizations,
        'periods': periods,
        'category': 'daily_life',
        'category_display': 'Daily Life',
    }
    return render(request, 'reference/cultural_topics.html', context)

def social_classes(request):
    """Social classes topics"""
    topics = CulturalTopic.objects.filter(category='social_classes').order_by('title_is')
    civilizations = Civilization.objects.all().order_by('name_is')
    periods = HistoricalPeriod.objects.all().order_by('start_year')

    context = {
        'topics': topics,
        'civilizations': civilizations,
        'periods': periods,
        'category': 'social_classes',
        'category_display': 'Social Classes',
    }
    return render(request, 'reference/cultural_topics.html', context)

def trade(request):
    """Trade & Commerce topics"""
    topics = CulturalTopic.objects.filter(category='trade').order_by('title_is')
    civilizations = Civilization.objects.all().order_by('name_is')
    periods = HistoricalPeriod.objects.all().order_by('start_year')

    context = {
        'topics': topics,
        'civilizations': civilizations,
        'periods': periods,
        'category': 'trade',
        'category_display': 'Trade & Commerce',
    }
    return render(request, 'reference/cultural_topics.html', context)

def art(request):
    """Art & Architecture topics"""
    topics = CulturalTopic.objects.filter(category='art').order_by('title_is')
    civilizations = Civilization.objects.all().order_by('name_is')
    periods = HistoricalPeriod.objects.all().order_by('start_year')

    context = {
        'topics': topics,
        'civilizations': civilizations,
        'periods': periods,
        'category': 'art',
        'category_display': 'Art & Architecture',
    }
    return render(request, 'reference/cultural_topics.html', context)

def literature(request):
    """Literature & Writing topics"""
    topics = CulturalTopic.objects.filter(category='literature').order_by('title_is')
    civilizations = Civilization.objects.all().order_by('name_is')
    periods = HistoricalPeriod.objects.all().order_by('start_year')

    context = {
        'topics': topics,
        'civilizations': civilizations,
        'periods': periods,
        'category': 'literature',
        'category_display': 'Literature & Writing',
    }
    return render(request, 'reference/cultural_topics.html', context)
