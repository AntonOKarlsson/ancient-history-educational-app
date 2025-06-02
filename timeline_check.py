from timeline.models import TimelineEvent
from core.models import Civilization

# Get all events ordered by date_start
events = TimelineEvent.objects.all().order_by('date_start')[:10]

print("First 10 events by date_start:")
for event in events:
    civ_name = event.civilization.name_is if event.civilization else "No civilization"
    print(f"{event.date_start}: {event.title_is} ({civ_name})")

# Get Roman events
roman_civ = Civilization.objects.filter(name_is='Rómverjar').first()
if roman_civ:
    roman_events = TimelineEvent.objects.filter(civilization=roman_civ).order_by('date_start')
    print("\nRoman events:")
    for event in roman_events:
        print(f"{event.date_start}: {event.title_is}")
else:
    print("\nRoman civilization not found")