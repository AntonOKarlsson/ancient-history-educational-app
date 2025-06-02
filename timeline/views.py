from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import TimelineEvent, TimelineRelation
from core.models import HistoricalPeriod, Civilization

def timeline(request):
    """Main timeline view with interactive timeline and map"""
    # Get all periods for filtering
    periods = HistoricalPeriod.objects.all().order_by('start_year')

    # Get all civilizations for filtering
    civilizations = Civilization.objects.all().order_by('name_is')

    # Get initial events (limited to improve performance)
    # Get a balanced set of events from each civilization
    events = []

    # Get all civilizations
    all_civilizations = Civilization.objects.all()

    # Get events from each civilization (up to 20 per civilization)
    for civ in all_civilizations:
        civ_events = TimelineEvent.objects.filter(civilization=civ).order_by('date_start')[:20]
        events.extend(civ_events)

    # Add events without a civilization
    no_civ_events = TimelineEvent.objects.filter(civilization=None).order_by('date_start')[:20]
    events.extend(no_civ_events)

    # Sort all events chronologically
    events = sorted(events, key=lambda x: x.date_start)

    context = {
        'periods': periods,
        'civilizations': civilizations,
        'events': events,
    }

    return render(request, 'timeline/timeline.html', context)

def event_detail(request, event_id):
    """Detailed view of a single timeline event"""
    event = get_object_or_404(TimelineEvent, id=event_id)

    # Get related events
    related_events = []
    relations = TimelineRelation.objects.filter(from_event=event)
    for relation in relations:
        related_events.append({
            'event': relation.to_event,
            'relation_type': relation.relation_type,
            'description': relation.description_is,
        })

    context = {
        'event': event,
        'related_events': related_events,
    }

    return render(request, 'timeline/event_detail.html', context)

def filter_events(request):
    """AJAX view for filtering timeline events"""
    # Get filter parameters from request
    period_id = request.GET.get('period')
    civilization_id = request.GET.get('civilization')
    category = request.GET.get('category')
    start_year = request.GET.get('start_year')
    end_year = request.GET.get('end_year')
    importance = request.GET.get('importance')

    # Start with all events
    events = TimelineEvent.objects.all()

    # Apply filters
    if period_id:
        events = events.filter(period_id=period_id)

    if civilization_id:
        events = events.filter(civilization_id=civilization_id)

    if category:
        events = events.filter(category=category)

    if start_year:
        events = events.filter(date_start__gte=start_year)

    if end_year:
        events = events.filter(date_start__lte=end_year)

    if importance:
        events = events.filter(importance__gte=importance)

    # Order events
    events = events.order_by('date_start')

    # Convert to list of dictionaries for JSON response
    events_data = []
    for event in events:
        events_data.append({
            'id': event.id,
            'title': event.title_is,
            'date_start': event.date_start,
            'date_end': event.date_end,
            'category': event.category,
            'importance': event.importance,
            'latitude': event.latitude,
            'longitude': event.longitude,
        })

    return JsonResponse({'events': events_data})
