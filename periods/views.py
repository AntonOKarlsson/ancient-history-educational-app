from django.shortcuts import render, get_object_or_404
from core.models import HistoricalPeriod
from timeline.models import TimelineEvent
from reference.models import Person, Deity, CulturalTopic
from quiz.models import Quiz

def period_home(request, period_slug):
    """Main view for a historical period (Grikkland, Róm, Miðaldir)"""
    # Get the period by slug
    period_names = {
        'grikkland': 'Grikkland',
        'rom': 'Róm',
        'midaldir': 'Miðaldir'
    }

    period_name = period_names.get(period_slug)
    period = get_object_or_404(HistoricalPeriod, name_is=period_name)

    # Get some sample content for each subsection
    timeline_events = TimelineEvent.objects.filter(period=period).order_by('-importance', 'date_start')[:5]
    people = Person.objects.filter(period=period).order_by('name_is')[:5]
    deities = Deity.objects.filter(civilization__period=period).order_by('name_is')[:5]
    cultural_topics = CulturalTopic.objects.filter(period=period).order_by('title_is')[:5]
    quizzes = Quiz.objects.filter(period=period, is_published=True).order_by('-created_at')[:5]

    context = {
        'period': period,
        'timeline_events': timeline_events,
        'people': people,
        'deities': deities,
        'cultural_topics': cultural_topics,
        'quizzes': quizzes,
    }

    return render(request, 'periods/period_home.html', context)

def period_timeline(request, period_slug):
    """Timeline view for a specific historical period"""
    # Get the period by slug
    period_names = {
        'grikkland': 'Grikkland',
        'rom': 'Róm',
        'midaldir': 'Miðaldir'
    }

    period_name = period_names.get(period_slug)
    period = get_object_or_404(HistoricalPeriod, name_is=period_name)

    # Get all events for this period
    events = TimelineEvent.objects.filter(period=period).order_by('date_start')

    context = {
        'period': period,
        'events': events,
    }

    return render(request, 'periods/period_timeline.html', context)

def period_people(request, period_slug):
    """Who's who (Hver-er-hver) view for a specific historical period"""
    # Get the period by slug
    period_names = {
        'grikkland': 'Grikkland',
        'rom': 'Róm',
        'midaldir': 'Miðaldir'
    }

    period_name = period_names.get(period_slug)
    period = get_object_or_404(HistoricalPeriod, name_is=period_name)

    # Get all people for this period
    people = Person.objects.filter(period=period).order_by('name_is')

    # Get all deities related to civilizations in this period
    deities = Deity.objects.filter(civilization__period=period).order_by('name_is')

    # Get categories for filtering
    categories = Person.PERSON_CATEGORIES

    context = {
        'period': period,
        'people': people,
        'deities': deities,
        'categories': categories,
    }

    return render(request, 'periods/period_people.html', context)

def period_culture(request, period_slug):
    """Culture (menning) view for a specific historical period"""
    # Get the period by slug
    period_names = {
        'grikkland': 'Grikkland',
        'rom': 'Róm',
        'midaldir': 'Miðaldir'
    }

    period_name = period_names.get(period_slug)
    period = get_object_or_404(HistoricalPeriod, name_is=period_name)

    # Get all cultural topics for this period
    topics = CulturalTopic.objects.filter(period=period).order_by('category', 'title_is')

    # Group topics by category
    topics_by_category = {}
    for category, display in CulturalTopic.TOPIC_CATEGORIES:
        category_topics = topics.filter(category=category)
        if category_topics.exists():
            topics_by_category[display] = category_topics

    context = {
        'period': period,
        'topics_by_category': topics_by_category,
    }

    return render(request, 'periods/period_culture.html', context)

def period_quiz(request, period_slug):
    """Quiz view for a specific historical period"""
    # Get the period by slug
    period_names = {
        'grikkland': 'Grikkland',
        'rom': 'Róm',
        'midaldir': 'Miðaldir'
    }

    period_name = period_names.get(period_slug)
    period = get_object_or_404(HistoricalPeriod, name_is=period_name)

    # Get all quizzes for this period
    quizzes = Quiz.objects.filter(period=period, is_published=True).order_by('-created_at')

    context = {
        'period': period,
        'quizzes': quizzes,
    }

    return render(request, 'periods/period_quiz.html', context)
