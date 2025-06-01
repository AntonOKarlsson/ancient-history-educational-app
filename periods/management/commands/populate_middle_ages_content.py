import os
import django
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import HistoricalPeriod, Civilization
from timeline.models import TimelineEvent
from reference.models import Person, Deity, CulturalTopic
from quiz.models import Quiz, Question

class Command(BaseCommand):
    help = 'Populates the database with Middle Ages content'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database with Middle Ages content...')
        
        # Get the Middle Ages period
        try:
            midaldir = HistoricalPeriod.objects.get(name_is='Miðaldir')
        except HistoricalPeriod.DoesNotExist:
            self.stdout.write(self.style.ERROR('Middle Ages period not found. Run populate_periods command first.'))
            return
        
        # Create sub-periods
        armidaldir = self.create_sub_period(midaldir, 'Early Middle Ages', 'Ármiðaldir', 476, 800, 
            'The Early Middle Ages covers the period from the fall of the Western Roman Empire to the rise of Charlemagne.',
            'Ármiðaldir ná frá falli Vestrómverska ríkisins til uppgangs Karls mikla.')
        
        hamidaldir = self.create_sub_period(midaldir, 'High Middle Ages', 'Hámiðaldir', 800, 1350, 
            'The High Middle Ages covers the period from Charlemagne to the beginning of the Late Middle Ages.',
            'Hámiðaldir ná frá Karli mikla til upphafs síðmiðalda.')
        
        sidmidaldir = self.create_sub_period(midaldir, 'Late Middle Ages', 'Síðmiðaldir', 1350, 1492, 
            'The Late Middle Ages covers the period from the Black Death to the beginning of the Age of Discovery.',
            'Síðmiðaldir ná frá svarta dauða til upphafs landafundatímabilsins.')
        
        # Create civilizations
        byzantine_civ = self.create_civilization(midaldir, 'Byzantine Empire', 'Býsanríkið', 330, 1453, 'Eastern Mediterranean',
            'The Byzantine Empire was the continuation of the Eastern Roman Empire during the Late Antiquity and the Middle Ages.',
            'Býsanríkið var framhald Austrómverska ríkisins á síðfornöld og miðöldum.')
        
        islamic_civ = self.create_civilization(midaldir, 'Islamic Caliphate', 'Íslamskt kalífadæmi', 622, 1258, 'Middle East and North Africa',
            'The Islamic Caliphate was the first of several Islamic states established after the death of Muhammad.',
            'Íslamskt kalífadæmi var fyrsta af nokkrum íslömskum ríkjum sem stofnuð voru eftir dauða Múhameðs.')
        
        frankish_civ = self.create_civilization(midaldir, 'Frankish Kingdom', 'Frankaríkið', 481, 843, 'Western Europe',
            'The Frankish Kingdom was the territory inhabited by the Franks, a Germanic people who conquered most of Roman Gaul.',
            'Frankaríkið var landsvæði Franka, germansks þjóðflokks sem lagði undir sig mest allt rómverska Gallíu.')
        
        # Create timeline events
        self.create_timeline_events(midaldir, armidaldir, hamidaldir, sidmidaldir, byzantine_civ, islamic_civ, frankish_civ)
        
        # Create people
        self.create_people(midaldir, byzantine_civ, islamic_civ, frankish_civ)
        
        # Create cultural topics
        self.create_cultural_topics(midaldir)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated Middle Ages content'))
    
    def create_sub_period(self, parent, name, name_is, start_year, end_year, description, description_is):
        """Helper method to create a sub-period"""
        sub_period, created = HistoricalPeriod.objects.get_or_create(
            name=name,
            name_is=name_is,
            start_year=start_year,
            end_year=end_year,
            description=description,
            description_is=description_is,
            parent=parent
        )
        if created:
            self.stdout.write(f'Created sub-period: {name_is}')
        return sub_period
    
    def create_civilization(self, period, name, name_is, start_year, end_year, region, description, description_is):
        """Helper method to create a civilization"""
        civilization, created = Civilization.objects.get_or_create(
            name=name,
            name_is=name_is,
            start_year=start_year,
            end_year=end_year,
            region=region,
            description=description,
            description_is=description_is,
            period=period
        )
        if created:
            self.stdout.write(f'Created civilization: {name_is}')
        return civilization
    
    def create_timeline_events(self, midaldir, armidaldir, hamidaldir, sidmidaldir, byzantine_civ, islamic_civ, frankish_civ):
        """Create timeline events for the Middle Ages"""
        # Early Middle Ages (Ármiðaldir) 476-800
        TimelineEvent.objects.get_or_create(
            title='Fall of Western Roman Empire',
            title_is='Vestrómverska ríkið hrynur',
            description='The fall of the Western Roman Empire in 476 CE marks the beginning of the Early Middle Ages.',
            description_is='Vestrómverska ríkið hrynur\nUpphaf ármiðalda\nÞjóðflutningar germanska þjóða',
            date_start=476,
            period=armidaldir,
            region='Western Europe',
            category='political',
            importance=5
        )
        
        TimelineEvent.objects.get_or_create(
            title='Germanic Migrations',
            title_is='Þjóðflutningar germanska þjóða',
            description='The Germanic migrations of the 5th-6th centuries reshaped the political landscape of Europe.',
            description_is='Húnar undir Atla ná völdum í Austur-Evrópu\n451: Orrusta á Katalónsvöllum - Húnar sigraðir\nVestgotar stofna ríki á Ítalíu og Spáni\nAustgotar og Langbarðar stofna ríki á Ítalíu\nEnglar, Saxar og Jótar leggja undir sig Bretland',
            date_start=400,
            date_end=600,
            period=armidaldir,
            region='Europe',
            category='political',
            importance=4
        )
        
        TimelineEvent.objects.get_or_create(
            title='Merovingian Period Begins',
            title_is='Tímabil Mervíkinga hefst',
            description='The Merovingian period began with Clovis I becoming king of the Franks.',
            description_is='Kloðvík af ætt Mervíkinga verður konungur Franka\n486: Sigraður rómverski keisarinn Sýagríus\nFrankar ná yfirráðum í Norður-Gallíu\nVestgotar hraktir frá Frakklandi til Spánar',
            date_start=480,
            date_end=511,
            period=armidaldir,
            civilization=frankish_civ,
            region='France',
            category='political',
            importance=4
        )
        
        TimelineEvent.objects.get_or_create(
            title='Kingdom Formation',
            title_is='Ríkjamyndun',
            description='The 6th-7th centuries saw the formation of various kingdoms across Europe.',
            description_is='Frankaríkið mótast á 6. öld\nVestgota og Langbarðaríkin stofnuð\nEngilsaxar setjast að á Englandi á 7. öld\nKloðvík tekur kristna trú',
            date_start=500,
            date_end=700,
            period=armidaldir,
            region='Europe',
            category='political',
            importance=4
        )
        
        TimelineEvent.objects.get_or_create(
            title='Byzantine Empire Timeline',
            title_is='Tímalína Býsanríkisins',
            description='The Byzantine Empire existed from 330 to 1453 CE.',
            description_is='330: Konstantín mikli stofnar Konstantínópel\n395: Rómaveldi skipt í tvo hluta\n476: Austurhlutinn stendur einn eftir\n527-565: Jústiníanus keisari, stærsta útbreiðsla ríkisins\n711: Múslimar leggja undir sig Sýrland, Palestínu og Egyptaland',
            date_start=330,
            date_end=1453,
            period=midaldir,
            civilization=byzantine_civ,
            region='Eastern Mediterranean',
            category='political',
            importance=5
        )
        
        TimelineEvent.objects.get_or_create(
            title='Islamic Expansion',
            title_is='Útbreiðsla íslams',
            description='The Islamic expansion from 622 to 732 CE saw the spread of Islam across the Middle East, North Africa, and parts of Europe.',
            description_is='622: Hijara - Múhameð flýr frá Mekka til Medínu\n630: Dauði Múhameðs\n635-640: Arabar leggja undir sig Sýrland, Írak, Palestínu\n661: Umayyadar ættin tekur völdin, Damaskus höfuðborg\n711: Berbar sigla yfir Gíbraltarsund, leggja undir sig Spán\n732: Orrusta við Poitiers - arabasókn stöðvuð',
            date_start=622,
            date_end=732,
            period=armidaldir,
            civilization=islamic_civ,
            region='Middle East, North Africa, and Southern Europe',
            category='political',
            importance=5
        )
        
        TimelineEvent.objects.get_or_create(
            title='Carolingian Rise',
            title_is='Uppgangur Karlungaættar',
            description='The rise of the Carolingian dynasty from 751 to 800 CE.',
            description_is='751: Pipin litli setr Childerik III í klaustur, verður konungur\nSamskipti við páfastól eflast\nPipin aðstoðar páfa gegn Langbörðum á Ítalíu\n768: Karl mikli tekur við völdum\n800: Karl mikli krýndur keisari',
            date_start=751,
            date_end=800,
            period=armidaldir,
            civilization=frankish_civ,
            region='Western Europe',
            category='political',
            importance=4
        )
        
        # High Middle Ages (Hámiðaldir) 800-1350
        TimelineEvent.objects.get_or_create(
            title='Charlemagne\'s Empire',
            title_is='Ríki Karls mikla',
            description='Charlemagne\'s empire from 800 to 814 CE was the largest in Western Europe since the fall of Rome.',
            description_is='800: Karl mikli krýndur keisari af páfa\nRíkið nær yfir Frakkland, hluta Þýskalands og suður fyrir Róm\nLærdómur og menning eflast\nAlkvin enskur munkur hjálpar við menningarmál\nEndurskoðun biblíuþýðingar (Vulgata)',
            date_start=800,
            date_end=814,
            period=hamidaldir,
            civilization=frankish_civ,
            region='Western Europe',
            category='political',
            importance=5
        )
        
        TimelineEvent.objects.get_or_create(
            title='Empire Division',
            title_is='Skipting ríkisins',
            description='The division of Charlemagne\'s empire after his death in 814 CE.',
            description_is='814: Karl mikli deyr\nLúðvík sonur hans tekur við\nRíkið skipt á milli þriggja sona Lúðvíks\nFrankaríkið klofnar í Vestfrankaríki og Austfrankaríki',
            date_start=814,
            date_end=843,
            period=hamidaldir,
            civilization=frankish_civ,
            region='Western Europe',
            category='political',
            importance=4
        )
        
        TimelineEvent.objects.get_or_create(
            title='Viking Raids and Empire Decline',
            title_is='Víkingaránir og hnignun ríkisins',
            description='Viking raids and the decline of the Carolingian Empire in the 9th century.',
            description_is='Um miðja 9. öld: Víkingaránir á meginland Evrópu hefjast\nMiðhluti Karls mikla ríkis leysist upp\n918: Karlungaættin í Austfrankaríki deyr út\n987: Karlungar missa völd í Vestfrankaríki',
            date_start=850,
            date_end=987,
            period=hamidaldir,
            region='Western Europe',
            category='political',
            importance=4
        )
        
        TimelineEvent.objects.get_or_create(
            title='Byzantine Decline Begins',
            title_is='Hnignun Býsanríkisins hefst',
            description='The Byzantine Empire began to decline around 1000 CE.',
            description_is='Um 1000: Býsanríkið missir Litlu-Asíu til Tyrkja\nStórlandeigendaaðall tekur völd frá smábændum\nHerinn veikist',
            date_start=1000,
            date_end=1100,
            period=hamidaldir,
            civilization=byzantine_civ,
            region='Eastern Mediterranean',
            category='political',
            importance=4
        )
        
        TimelineEvent.objects.get_or_create(
            title='The Great Schism',
            title_is='Kirkjuklofningurinn mikli',
            description='The Great Schism of 1054 CE split the Christian church into Eastern Orthodox and Roman Catholic churches.',
            description_is='Kirkjan klofnar í tvennt\nGríska rétttrúnaðarkirkjan vs. rómversk-kaþólska kirkjan\nÁtök páfa í Róm og patríarka í Konstantínópel',
            date_start=1054,
            period=hamidaldir,
            region='Europe',
            category='religious',
            importance=5
        )
        
        TimelineEvent.objects.get_or_create(
            title='Crusades Era',
            title_is='Tímabil krossferða',
            description='The Crusades era of the 12th-13th centuries saw multiple military campaigns from Western Europe to the Holy Land.',
            description_is='Veldi kirkjunnar nær hápunkti í krossferðunum\n1204: Krossfaraher ræður og rúplaður Konstantínópel',
            date_start=1095,
            date_end=1291,
            period=hamidaldir,
            region='Europe and Middle East',
            category='military',
            importance=5
        )
        
        # Late Middle Ages (Síðmiðaldir) 1350-1492
        TimelineEvent.objects.get_or_create(
            title='The Black Death',
            title_is='Svarti dauði',
            description='The Black Death pandemic of 1347-1351 CE killed 30-60% of Europe\'s population.',
            description_is='1347: Svarti dauði (plágan mikla) kemur til Evrópu\nSkortur á fólki í landbúnaði\nKjör þeirra sem lifa af batna',
            date_start=1347,
            date_end=1351,
            period=sidmidaldir,
            region='Europe',
            category='other',
            importance=5
        )
        
        TimelineEvent.objects.get_or_create(
            title='Political Changes',
            title_is='Stjórnmálabreytingar',
            description='Political changes in Europe from 1350 to 1453 CE.',
            description_is='Vald kirkjunnar minnkar\nVöld konunga aukast á kostnað aðals\nÞjóðríki taka að mótast í Evrópu\nPeningaviðskipti aukast, fyrstu bankastofnanir',
            date_start=1350,
            date_end=1453,
            period=sidmidaldir,
            region='Europe',
            category='political',
            importance=4
        )
        
        TimelineEvent.objects.get_or_create(
            title='Fall of Constantinople',
            title_is='Fall Konstantínópel',
            description='The fall of Constantinople to the Ottoman Turks in 1453 CE marked the end of the Byzantine Empire.',
            description_is='Tyrkir leggja undir sig Konstantínópel\nEnda 1100 ára sögu Býsanríkisins',
            date_start=1453,
            period=sidmidaldir,
            civilization=byzantine_civ,
            region='Constantinople',
            category='military',
            importance=5
        )
        
        TimelineEvent.objects.get_or_create(
            title='Age of Discovery Begins',
            title_is='Landafundatímabilið hefst',
            description='The Age of Discovery began in the late 15th century with European exploration of the world.',
            description_is='Jóhann Gutenberg finnur upp lausaletrið\nPortúgalar sigla fyrir suðurodda Afríku\n1492: Kristófer Kólumbus siglar til Ameríku\nLok miðalda, nýöld tekur við',
            date_start=1450,
            date_end=1492,
            period=sidmidaldir,
            region='Europe',
            category='cultural',
            importance=5
        )
    
    def create_people(self, midaldir, byzantine_civ, islamic_civ, frankish_civ):
        """Create people for the Middle Ages"""
        # Emperors & Kings
        Person.objects.get_or_create(
            name='Constantine the Great',
            name_is='Konstantín mikli',
            birth_date=272,
            death_date=337,
            category='ruler',
            civilization=byzantine_civ,
            period=midaldir,
            biography='Constantine the Great was a Roman emperor who ruled from 306 to 337 CE.',
            biography_is='Rómverskur keisari\nStofnaði Konstantínópel 330\nFyrsti kristni keisarinn\nVildi stofna kristna borg',
            achievements='Constantine was the first Roman emperor to convert to Christianity and founded Constantinople.',
            achievements_is='Konstantín var fyrsti rómverski keisarinn sem tók kristna trú og stofnaði Konstantínópel.'
        )
        
        Person.objects.get_or_create(
            name='Justinian I',
            name_is='Jústiníanus keisari',
            birth_date=483,
            death_date=565,
            category='ruler',
            civilization=byzantine_civ,
            period=midaldir,
            biography='Justinian I was a Byzantine emperor who ruled from 527 to 565 CE.',
            biography_is='Einn frægasti keisari Miklagarðs\nRíkti 527-565\nUndir hans stjórn var Býsanríkið stærst\nSamræmdi lög í ríkinu (Corpus juris civilis)\nLögin höfðu mikil áhrif á Vestur-Evrópu',
            achievements='Justinian I reconquered much of the former Western Roman Empire and codified Roman law.',
            achievements_is='Jústiníanus I endurheimti stóran hluta fyrrum Vestrómverska ríkisins og samræmdi rómversk lög.'
        )
        
        Person.objects.get_or_create(
            name='Attila the Hun',
            name_is='Atli konungur Húna',
            birth_date=406,
            death_date=453,
            category='ruler',
            period=midaldir,
            biography='Attila was the ruler of the Huns from 434 until his death in 453 CE.',
            biography_is='Konungur Húna á hátindi valda þeirra\nRíki hans náði frá Kaspíahafi til miðju Evrópu\n451: Tapaði orrustu á Katalónsvöllum\nEftir dauða hans voru Húnar hraktir burt',
            achievements='Attila led the Hunnic Empire to its greatest extent before being defeated at the Battle of the Catalaunian Plains.',
            achievements_is='Atli leiddi Húnaríkið til sinnar mestu útbreiðslu áður en hann var sigraður í orrustu á Katalónsvöllum.'
        )
        
        Person.objects.get_or_create(
            name='Clovis I',
            name_is='Kloðvík',
            birth_date=466,
            death_date=511,
            category='ruler',
            civilization=frankish_civ,
            period=midaldir,
            biography='Clovis I was the first king of the Franks to unite all of the Frankish tribes under one ruler.',
            biography_is='Sonur Childeric I af ætt Mervíkinga\nVarð konungur Franka 480\nSnjall herforingi\n486: Sigraði rómverska keisarann Sýagríus\nTók kristna trú - lykilatriði í langlífi Frankaríkisins',
            achievements='Clovis I united the Frankish tribes and converted to Christianity, setting the stage for the Frankish Empire.',
            achievements_is='Kloðvík sameinaði Franka og tók kristna trú, sem lagði grunninn að Frankaríkinu.'
        )
        
        Person.objects.get_or_create(
            name='Pepin the Short',
            name_is='Pipin litli',
            birth_date=714,
            death_date=768,
            category='ruler',
            civilization=frankish_civ,
            period=midaldir,
            biography='Pepin the Short was the first King of the Franks of the Carolingian dynasty.',
            biography_is='Ríkisstjóri Mervíkinga\n751: Setti Childerik III í klaustur, varð sjálfur konungur\nStofnaði Karlungaætt\nNáin samskipti við páfastól\nAðstoðaði páfa gegn Langbörðum',
            achievements='Pepin the Short deposed the last Merovingian king and established the Carolingian dynasty.',
            achievements_is='Pipin litli steypti síðasta Mervíkingakonungnum af stóli og stofnaði Karlungaættina.'
        )
        
        Person.objects.get_or_create(
            name='Charlemagne',
            name_is='Karl mikli',
            birth_date=742,
            death_date=814,
            category='ruler',
            civilization=frankish_civ,
            period=midaldir,
            biography='Charlemagne was King of the Franks from 768, King of the Lombards from 774, and Emperor of the Romans from 800.',
            biography_is='Sonur Pipin litla\nKonungur Franka, síðar rómverskur keisari\n800: Krýndur keisari af páfa\nRíki hans náði yfir Frakkland, hluta Þýskalands og suður fyrir Róm\nEfldi menntun og menningu\n"Faðir Evrópu"',
            achievements='Charlemagne united much of Western Europe for the first time since the Roman Empire and laid the foundations for modern France and Germany.',
            achievements_is='Karl mikli sameinaði stóran hluta Vestur-Evrópu í fyrsta sinn síðan Rómaveldi féll og lagði grunninn að nútíma Frakklandi og Þýskalandi.'
        )
        
        Person.objects.get_or_create(
            name='Louis the Pious',
            name_is='Lúðvík hinn trúaði',
            birth_date=778,
            death_date=840,
            category='ruler',
            civilization=frankish_civ,
            period=midaldir,
            biography='Louis the Pious was the King of the Franks and co-emperor with his father, Charlemagne, from 813.',
            biography_is='Sonur Karls mikla\nLagði áherslu á umbætur innan kirkjunnar\nSkipti ríkinu á milli þriggja sona sinna\nÞessi skipting olli sundrungu ríkisins',
            achievements='Louis the Pious continued his father\'s reforms but his division of the empire among his sons led to its fragmentation.',
            achievements_is='Lúðvík hinn trúaði hélt áfram umbótum föður síns en skipting ríkisins milli sona hans leiddi til sundrungar þess.'
        )
        
        # Religious Leaders
        Person.objects.get_or_create(
            name='Muhammad',
            name_is='Múhameð spámaður',
            birth_date=570,
            death_date=632,
            category='religious',
            civilization=islamic_civ,
            period=midaldir,
            biography='Muhammad was the founder of Islam and is considered the last prophet by Muslims.',
            biography_is='Stofnandi íslamstrúar\nFæddur í Mekka\n610: Varð fyrir trúarreynslu\n622: Hijara - flótti til Medínu\n630: Dó eftir að hafa sameinað Arabíu',
            achievements='Muhammad united Arabia under Islam and established the foundation for the Islamic Caliphate.',
            achievements_is='Múhameð sameinaði Arabíu undir íslam og lagði grunninn að íslömsku kalífadæmi.'
        )
        
        Person.objects.get_or_create(
            name='Abu Bakr',
            name_is='Abu-Bakr',
            birth_date=573,
            death_date=634,
            category='religious',
            civilization=islamic_civ,
            period=midaldir,
            biography='Abu Bakr was the first Caliph following Muhammad\'s death and a father-in-law of Muhammad.',
            biography_is='Tengdafaðir Múhameðs\nFyrsti kalífinn eftir Múhameð\nHóf landvinningatímabilið',
            achievements='Abu Bakr consolidated the newly formed Islamic state and began the early Muslim conquests.',
            achievements_is='Abu-Bakr styrkti hið nýstofnaða íslömsku ríki og hóf fyrstu landvinninga múslima.'
        )
        
        Person.objects.get_or_create(
            name='Pope Stephen',
            name_is='Stefán páfi',
            birth_date=None,
            death_date=None,
            category='religious',
            period=midaldir,
            biography='Pope Stephen sought the aid of Pepin the Short against the Lombards in Italy.',
            biography_is='Fékk aðstoð Pipin litla gegn Langbörðum\nStyrktist samband páfastóls og Karlungaættar',
            achievements='Pope Stephen established a strong alliance between the Papacy and the Carolingian dynasty.',
            achievements_is='Stefán páfi kom á sterkum tengslum milli páfastóls og Karlungaættar.'
        )
        
        # Scholars & Cultural Figures
        Person.objects.get_or_create(
            name='Alcuin',
            name_is='Alkvin',
            birth_date=735,
            death_date=804,
            category='philosopher',
            period=midaldir,
            biography='Alcuin was an English scholar, cleric, poet, and teacher from York, Northumbria.',
            biography_is='Enskur munkur\nHjálpaði Karli mikla við menningarmál\nUndir hans forystu:\nEndurskoðun biblíuþýðingar (Vulgata)\nÞýðing og endurskoðun bóka\nSkipulag menntastofnana\nGregoríanskur messusöngur þróaður',
            achievements='Alcuin was a key figure in the Carolingian Renaissance, advising Charlemagne on educational and cultural matters.',
            achievements_is='Alkvin var lykilpersóna í endurreisn Karlungaættar og ráðlagði Karli mikla í mennta- og menningarmálum.'
        )
        
        Person.objects.get_or_create(
            name='Tacitus',
            name_is='Tacitus',
            birth_date=56,
            death_date=120,
            category='philosopher',
            period=midaldir,
            biography='Tacitus was a Roman historian and politician.',
            biography_is='Rómverskur sagnaritari\nSkrifaði "Germanía" um aldamótin 100\nLýsti ættflokkasamfélagi Germana\nJákvæður í garð germanska þjóðflokkanna',
            achievements='Tacitus wrote "Germania," which provides valuable information about the Germanic tribes.',
            achievements_is='Tacitus skrifaði "Germanía," sem veitir mikilvægar upplýsingar um germanska þjóðflokka.'
        )
        
        # Germanic Tribal Leaders
        Person.objects.get_or_create(
            name='Childeric I',
            name_is='Childeric I',
            birth_date=None,
            death_date=None,
            category='ruler',
            civilization=frankish_civ,
            period=midaldir,
            biography='Childeric I was a Merovingian king of the Salian Franks and the father of Clovis I.',
            biography_is='Konungur Franka, faðir Kloðvíks\nAf ætt Mervíkinga\nInnsiglishringur hans fannst í gröf',
            achievements='Childeric I established the Merovingian dynasty that would rule the Franks for nearly 300 years.',
            achievements_is='Childeric I stofnaði Mervíkingaættina sem ríkti yfir Frökkum í næstum 300 ár.'
        )
        
        Person.objects.get_or_create(
            name='Childeric III',
            name_is='Childerik III',
            birth_date=None,
            death_date=None,
            category='ruler',
            civilization=frankish_civ,
            period=midaldir,
            biography='Childeric III was the last Merovingian king of the Franks.',
            biography_is='Síðasti konungur Mervíkinga\n"Konungur eingöngu að nafninu til"\nSettur í klaustur af Pipin litla 751',
            achievements='Childeric III was the last Merovingian king before Pepin the Short deposed him and established the Carolingian dynasty.',
            achievements_is='Childerik III var síðasti Mervíkingakonungurinn áður en Pipin litli steypti honum af stóli og stofnaði Karlungaættina.'
        )
        
        # Byzantine Figures
        Person.objects.get_or_create(
            name='Varangian Guard',
            name_is='Væringjar',
            birth_date=None,
            death_date=None,
            category='military',
            civilization=byzantine_civ,
            period=midaldir,
            biography='The Varangian Guard was an elite unit of the Byzantine Army from the 10th to 14th centuries.',
            biography_is='Víkingar sem voru málaliðar hjá keisara\nEinkum Svíar og nokkrir Íslendingar\nSigldu suður til Miklagarðs gegnum Rússland',
            achievements='The Varangian Guard served as the personal bodyguards of the Byzantine Emperors.',
            achievements_is='Væringjar þjónuðu sem persónulegir lífverðir býsanskra keisara.'
        )
    
    def create_cultural_topics(self, midaldir):
        """Create cultural topics for the Middle Ages"""
        # Germanic Society
        CulturalTopic.objects.get_or_create(
            title='Germanic Society',
            title_is='Germanskt þjóðfélag',
            category='social_classes',
            period=midaldir,
            content='Germanic society was based on tribal organization with elected kings and limited royal power.',
            content_is='Ættflokkasamfélag: Grundvöllur germanska þjóðfélagsins\nKonungar kosnir af höfðingjum: Ákveðnar ættir höfðu rétt á konungstign\nValdalitlir konungar: Nema í hernaði\nVenjuréttur: Löggjöf byggð á fornum siðum og venjum'
        )
        
        # Religious Divisions
        CulturalTopic.objects.get_or_create(
            title='Religious Divisions',
            title_is='Trúardeilur',
            category='religion',
            period=midaldir,
            content='Religious divisions in the Middle Ages included Arianism, Catholicism, Monophysitism, and the Iconoclast Controversy.',
            content_is='Aríusarkristni: Jesús var maður en ekki sonur guðs (germönsk ríki)\nKaþólska trú: Í Rómaveldi, á móti Aríusarkristni\nEineðlismenn: Trúðu á guðlegt eðli Krists eingöngu\nÍkona-deilur: Um helgimyndir á 8. öld'
        )
        
        # Islamic Terms
        CulturalTopic.objects.get_or_create(
            title='Islamic Terms',
            title_is='Íslam hugtök',
            category='religion',
            period=midaldir,
            content='Key Islamic terms and concepts that emerged during the Middle Ages.',
            content_is='Íslam: "Hin sanntrúuðu", trúin sjálf\nMúslimar: Fylgismenn íslam\nHijara: Flótti Múhameðs frá Mekka til Medínu 622\nKalífi: Eftirmaður spámannsins\nJihad: Heilagt stríð á trúarlegum forsendum\nBedúínar: Hirðingjar Arabíu'
        )