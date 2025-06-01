import os
import django
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import HistoricalPeriod, Civilization
from timeline.models import TimelineEvent
from reference.models import Person, Deity, CulturalTopic
from quiz.models import Quiz, Question

class Command(BaseCommand):
    help = 'Populates the database with historical periods and content'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Creating historical periods...')
        
        # Create main periods
        grikkland, created = HistoricalPeriod.objects.get_or_create(
            name='Ancient Greece',
            name_is='Grikkland',
            start_year=-3000,  # 3000 BCE
            end_year=-323,     # 323 BCE (death of Alexander the Great)
            description='Ancient Greece was a civilization belonging to a period of Greek history from the Greek Dark Ages (12th–9th centuries BC) to the end of antiquity (c. 600 AD).',
            description_is='Grikkland hið forna var menningarsamfélag sem tilheyrði tímabili grískrar sögu frá Myrku öldum Grikklands (12.-9. öld f.Kr.) til loka fornaldar (u.þ.b. 600 e.Kr.).'
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created period: {grikkland.name_is}'))
        
        rom, created = HistoricalPeriod.objects.get_or_create(
            name='Ancient Rome',
            name_is='Róm',
            start_year=-753,   # 753 BCE (traditional founding of Rome)
            end_year=476,      # 476 CE (fall of Western Roman Empire)
            description='Ancient Rome was a civilization that grew out of the city-state of Rome, founded on the Italian peninsula in the 8th century BC.',
            description_is='Rómaveldi hið forna var menningarsamfélag sem þróaðist út frá borgríkinu Róm, sem var stofnað á Ítalíuskaga á 8. öld f.Kr.'
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created period: {rom.name_is}'))
        
        midaldir, created = HistoricalPeriod.objects.get_or_create(
            name='Middle Ages',
            name_is='Miðaldir',
            start_year=476,    # 476 CE (fall of Western Roman Empire)
            end_year=1492,     # 1492 CE (discovery of America)
            description='The Middle Ages was the period of European history from the fall of the Western Roman Empire in the 5th century to the Renaissance and discovery of America in the late 15th century.',
            description_is='Miðaldir voru tímabil evrópskrar sögu frá falli Vesturrómaveldi á 5. öld til endurreisnar og uppgötvunar Ameríku í lok 15. aldar.'
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created period: {midaldir.name_is}'))
        
        # Create sub-periods for Grikkland
        archaic, created = HistoricalPeriod.objects.get_or_create(
            name='Archaic Period',
            name_is='Forngrískt tímabil',
            start_year=-800,
            end_year=-480,
            description='The Archaic period in Greece (800-480 BCE) was a period of ancient Greek history that followed the Greek Dark Ages.',
            description_is='Forngrískt tímabil (800-480 f.Kr.) var tímabil í sögu Grikklands hins forna sem fylgdi Myrku öldum Grikklands.',
            parent=grikkland
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created sub-period: {archaic.name_is}'))
        
        classical, created = HistoricalPeriod.objects.get_or_create(
            name='Classical Period',
            name_is='Klassískt tímabil',
            start_year=-480,
            end_year=-323,
            description='The Classical period in Greece (480-323 BCE) was a 200-year period in Greek culture that flourished after the Persian Wars.',
            description_is='Klassíska tímabilið (480-323 f.Kr.) var 200 ára tímabil í grískri menningu sem blómstraði eftir Persastríðin.',
            parent=grikkland
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created sub-period: {classical.name_is}'))
        
        hellenistic, created = HistoricalPeriod.objects.get_or_create(
            name='Hellenistic Period',
            name_is='Hellenska tímabilið',
            start_year=-323,
            end_year=-31,
            description='The Hellenistic period (323-31 BCE) covers the period of Mediterranean history between the death of Alexander the Great and the emergence of the Roman Empire.',
            description_is='Hellenska tímabilið (323-31 f.Kr.) nær yfir tímabil Miðjarðarhafssögu milli dauða Alexanders mikla og uppgangs Rómaveldis.',
            parent=grikkland
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created sub-period: {hellenistic.name_is}'))
        
        # Create Greek civilization
        greek_civ, created = Civilization.objects.get_or_create(
            name='Ancient Greek',
            name_is='Forngrikkir',
            start_year=-3000,
            end_year=-31,
            region='Mediterranean',
            description='The Ancient Greek civilization developed in the Balkan Peninsula and surrounding islands, and later spread across the Mediterranean.',
            description_is='Menning Forngrikkja þróaðist á Balkanskaga og nærliggjandi eyjum, og dreifðist síðar um Miðjarðarhafið.',
            period=grikkland
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created civilization: {greek_civ.name_is}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully populated historical periods'))