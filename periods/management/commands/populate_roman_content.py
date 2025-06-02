import os
import django
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import HistoricalPeriod, Civilization
from timeline.models import TimelineEvent
from reference.models import Person, Deity, CulturalTopic, Battle, Government
from quiz.models import Quiz, Question
import json

class Command(BaseCommand):
    help = 'Populates the database with Roman Empire content'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database with Roman Empire content...')
        
        # First, update the Roman period name
        try:
            rom = HistoricalPeriod.objects.get(name='Ancient Rome')
            rom.name_is = 'Rómaveldi'
            rom.save()
            self.stdout.write(self.style.SUCCESS(f'Updated period name to: {rom.name_is}'))
        except HistoricalPeriod.DoesNotExist:
            self.stdout.write(self.style.ERROR('Roman period not found. Run populate_periods command first.'))
            return
        
        # Create Roman sub-periods
        kingdom, created = HistoricalPeriod.objects.get_or_create(
            name='Kingdom Period',
            name_is='Konungaöld',
            start_year=-753,
            end_year=-509,
            description='The Kingdom Period was the first period of Roman history, when Rome was ruled by kings.',
            description_is='Konungaöld var fyrsta tímabil rómverskrar sögu, þegar Róm var stjórnað af konungum.',
            parent=rom
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created sub-period: {kingdom.name_is}'))
        
        republic, created = HistoricalPeriod.objects.get_or_create(
            name='Republic Period',
            name_is='Lýðveldisöld',
            start_year=-509,
            end_year=-30,
            description='The Republic Period was the period of ancient Roman civilization characterized by a republican form of government.',
            description_is='Lýðveldisöld var tímabil fornrómverskrar siðmenningar sem einkenndist af lýðveldisformi stjórnar.',
            parent=rom
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created sub-period: {republic.name_is}'))
        
        empire, created = HistoricalPeriod.objects.get_or_create(
            name='Empire Period',
            name_is='Keisaraöld',
            start_year=-30,
            end_year=476,
            description='The Empire Period was the post-Republican period of ancient Roman civilization, characterized by an autocratic form of government.',
            description_is='Keisaraöld var tímabil fornrómverskrar siðmenningar eftir lýðveldið, sem einkenndist af einræðisformi stjórnar.',
            parent=rom
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created sub-period: {empire.name_is}'))
        
        # Create Roman civilization
        roman_civ, created = Civilization.objects.get_or_create(
            name='Roman',
            name_is='Rómverjar',
            start_year=-753,
            end_year=476,
            region='Mediterranean',
            description='The Roman civilization developed on the Italian Peninsula and later spread across the Mediterranean and beyond.',
            description_is='Menning Rómverja þróaðist á Ítalíuskaga og dreifðist síðar um Miðjarðarhafið og víðar.',
            period=rom
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created civilization: {roman_civ.name_is}'))
        
        # Create timeline events
        self.create_timeline_events(rom, roman_civ, kingdom, republic, empire)
        
        # Create people
        self.create_people(rom, roman_civ, kingdom, republic, empire)
        
        # Create cultural topics
        self.create_cultural_topics(rom, roman_civ)
        
        # Create battles
        self.create_battles(rom, roman_civ)
        
        # Create quiz
        self.create_quiz(rom)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated Roman Empire content'))
    
    def create_timeline_events(self, rom, roman_civ, kingdom, republic, empire):
        # Kingdom Period
        TimelineEvent.objects.get_or_create(
            title='Foundation of Rome',
            title_is='Stofnun Rómar',
            description='The traditional founding date of Rome by Romulus.',
            description_is='Stofnun Rómar samkvæmt Varró. Rómúlus og Remus þjóðsögur. Sjö hæðir, Palatínhæð og Kapítolhæð. 300 landnemar og hefðarættir borgarinnar.',
            date_start=-753,
            period=kingdom,
            civilization=roman_civ,
            region='Italy',
            category='political',
            importance=5
        )
        
        TimelineEvent.objects.get_or_create(
            title='Seven Kings Period',
            title_is='Sjö konunga tímabil',
            description='The period of the seven kings of Rome.',
            description_is='Fjórir fyrstu konungar: þjóðsagnapersónur. Þrír síðustu konungar: etrúskir að uppruna. Öldungaráð (senatus) með 300 fulltrúum. Ættarfundir og þjóðfundir.',
            date_start=-753,
            date_end=-509,
            period=kingdom,
            civilization=roman_civ,
            region='Italy',
            category='political',
            importance=4
        )
        
        TimelineEvent.objects.get_or_create(
            title='End of Kingdom',
            title_is='Lok konungaöld',
            description='Patricians expel Tarquinius Superbus and establish the Republic.',
            description_is='Patríesar hrekja Tarquinius Superbus. Stofnun lýðveldis. Upphaf átaka við Etrúa.',
            date_start=-509,
            period=kingdom,
            civilization=roman_civ,
            region='Italy',
            category='political',
            importance=5
        )
        
        # Early Republic
        TimelineEvent.objects.get_or_create(
            title='Patrician-Plebeian Conflicts',
            title_is='Átök patríesa og plebeja',
            description='Conflicts between patricians and plebeians in early Rome.',
            description_is='494 f.Kr: Stofnun embættis alþýðuforingja. Veto-vald (neitunarvald) innleitt. 450 f.Kr: Tólf bronstöflur settar á Forum Romanum. Jafnrétti fyrir lögum en hjúskapur bannaður.',
            date_start=-509,
            date_end=-450,
            period=republic,
            civilization=roman_civ,
            region='Italy',
            category='political',
            importance=4
        )
        
        TimelineEvent.objects.get_or_create(
            title='Political Development',
            title_is='Stjórnmálaþróun',
            description='Political developments in the 4th century BCE.',
            description_is='Um miðja 4. öld: Auðugir plebejar fá aðgang að æðstu embættum. Skuldaánauð afnumin. 287 f.Kr: Alþýðufundir viðurkenndir sem þjóðfundir. Um 300 f.Kr: Embættismannkerfi fest.',
            date_start=-400,
            date_end=-300,
            period=republic,
            civilization=roman_civ,
            region='Italy',
            category='political',
            importance=3
        )
        
        TimelineEvent.objects.get_or_create(
            title='Gallic Sack of Rome',
            title_is='Gallar ráðast á Róm',
            description='Gauls attack Rome and burn the city.',
            description_is='Gallar réðust á Róm og brenndu borgina. Rómverjar greiddu gull til að losna við þá.',
            date_start=-390,
            period=republic,
            civilization=roman_civ,
            region='Italy',
            category='military',
            importance=4
        )
        
        TimelineEvent.objects.get_or_create(
            title='Conquest of Italy',
            title_is='Undirlagning Ítalíu',
            description='Romans conquer nearly all of Italy.',
            description_is='Rómverjar leggja undir sig nær alla Ítalíu. 280-275 f.Kr: Stríð við Pyrros konung Epeiros. Pyrrhosarsigar við Asculum 279 f.Kr. 275 f.Kr: Endanlegur sigur við Beneventum. Um 260 f.Kr: Öll Ítalía undir rómverskum yfirráðum.',
            date_start=-340,
            date_end=-260,
            period=republic,
            civilization=roman_civ,
            region='Italy',
            category='military',
            importance=4
        )
        
        # Punic Wars
        TimelineEvent.objects.get_or_create(
            title='First Punic War',
            title_is='Fyrsta púnverska stríðið',
            description='Conflict between Rome and Carthage over Sicily.',
            description_is='Átök um yfirráð yfir Sikiley. Rómverjar koma sér upp öflugum flota. 242 f.Kr: Mikill sjósigur Rómverja. 241 f.Kr: Sikiley verður fyrsta skattland Rómverja.',
            date_start=-264,
            date_end=-241,
            period=republic,
            civilization=roman_civ,
            region='Sicily',
            category='military',
            importance=5
        )
        
        TimelineEvent.objects.get_or_create(
            title='Second Punic War',
            title_is='Annað púnverska stríðið',
            description='Hannibal crosses the Alps into Italy.',
            description_is='Hannibal fer yfir Alpafjöll inn í Ítalíu. 216 f.Kr: Rómverjar stórtapa við Cannae. Fabíus Maximus og skæruhernaður. 206 f.Kr: Skípíó nær völdum á Spáni. 202 f.Kr: Úrslitaorusta við Zama - Hannibal sigraður.',
            date_start=-219,
            date_end=-201,
            period=republic,
            civilization=roman_civ,
            region='Mediterranean',
            category='military',
            importance=5
        )
        
        TimelineEvent.objects.get_or_create(
            title='Third Punic War',
            title_is='Þriðja púnverska stríðið',
            description='Carthage is burned and destroyed.',
            description_is='146 f.Kr: Karþagó brennd og eyðilögð. Stráð salti yfir borgina. Nágrenni Karþagó verður skattland "Afríka".',
            date_start=-149,
            date_end=-146,
            period=republic,
            civilization=roman_civ,
            region='North Africa',
            category='military',
            importance=4
        )
        
        # Late Republic
        TimelineEvent.objects.get_or_create(
            title='The Gracchan Reforms',
            title_is='Umbætur Grakkusarbræðra',
            description='Reforms by the Gracchi brothers.',
            description_is='133 f.Kr: Tíberíus Grakkus alþýðuforingi. Endurskipting þjóðjarða. Tíberíus drepinn á kosningadegi. 123 f.Kr: Gajus Grakkus alþýðuforingi. Kornskammtur fyrir öreiga. 121 f.Kr: Gajus stytti sér aldur.',
            date_start=-133,
            date_end=-121,
            period=republic,
            civilization=roman_civ,
            region='Italy',
            category='political',
            importance=4
        )
        
        TimelineEvent.objects.get_or_create(
            title='Marian Reforms and Civil Wars',
            title_is='Umbætur Maríusar og borgarastyrjaldir',
            description='Marius reforms the army and civil wars break out.',
            description_is='110 f.Kr: Stríð við Númidíumenn. Kimbrar og Tevtónar ráðast inn. Maríus endurbætir herinn, tekur öreiga. 90 f.Kr: Bandamannastríðið á Ítalíu. 89 f.Kr: Rómverskur borgararétt veittur bandamönnum.',
            date_start=-110,
            date_end=-80,
            period=republic,
            civilization=roman_civ,
            region='Italy',
            category='military',
            importance=4
        )
        
        TimelineEvent.objects.get_or_create(
            title='First Triumvirate',
            title_is='Fyrra þremenningarsambandið',
            description='Alliance between Pompey, Crassus, and Caesar.',
            description_is='73-71 f.Kr: Spartakus þrælauppreisn. 70 f.Kr: Pompejus og Krassus ræðismenn. 67 f.Kr: Pompejus sigrað sjóræningja. 63 f.Kr: Katilína samsæri, Cíceró ræðismaður. 60 f.Kr: Fyrra þremenningarsambandið. 59 f.Kr: Sesar ræðismaður. 58-50 f.Kr: Sesar leggur undir sig Gallíu.',
            date_start=-60,
            date_end=-53,
            period=republic,
            civilization=roman_civ,
            region='Rome',
            category='political',
            importance=5
        )
        
        TimelineEvent.objects.get_or_create(
            title='End of the Republic',
            title_is='Lok lýðveldisins',
            description='Final years of the Roman Republic.',
            description_is='53 f.Kr: Krassus fellur í Pörþu. 49 f.Kr: Sesar fer yfir Rúbíkon. 48 f.Kr: Pompejus sigraður við Farsalos. 44 f.Kr: Sesar myrtur 15. mars. 43 f.Kr: Síðara þremenningarsambandið. 31 f.Kr: Oktavíanus sigrað við Aktíum. 30 f.Kr: Dauði Antoníusar og Kleópötru.',
            date_start=-50,
            date_end=-30,
            period=republic,
            civilization=roman_civ,
            region='Mediterranean',
            category='political',
            importance=5
        )
        
        # Empire Period
        TimelineEvent.objects.get_or_create(
            title='Julio-Claudian Dynasty',
            title_is='Júlíaska-Kládíanska ættin',
            description='The first imperial dynasty of Rome.',
            description_is='Fyrsta keisaraætt Rómar. Ágústus, Tíberíus, Kalígúla, Kládíus og Neró.',
            date_start=-30,
            date_end=68,
            period=empire,
            civilization=roman_civ,
            region='Roman Empire',
            category='political',
            importance=5
        )
        
        TimelineEvent.objects.get_or_create(
            title='Flavian Dynasty',
            title_is='Flavíanska ættin',
            description='The Flavian dynasty ruled the Roman Empire.',
            description_is='Vespaníus, Títus og Dómitíanus. 69 e.Kr: Ár fjögurra keisara. 79 e.Kr: Vesúvíus gaus, Pompeii og Herkúlaneum.',
            date_start=69,
            date_end=96,
            period=empire,
            civilization=roman_civ,
            region='Roman Empire',
            category='political',
            importance=4
        )
        
        TimelineEvent.objects.get_or_create(
            title='Adoptive Emperors',
            title_is='Kjörkeisararnir',
            description='Period of the Five Good Emperors.',
            description_is='Nerva, Trajanus, Hadríanus, Antonínus Píus og Markús Árelíus. Rómaveldi aldrei stærra en á þessu tímabili.',
            date_start=96,
            date_end=180,
            period=empire,
            civilization=roman_civ,
            region='Roman Empire',
            category='political',
            importance=4
        )
        
        TimelineEvent.objects.get_or_create(
            title='Crisis and Decline',
            title_is='Kreppa og hnignun',
            description='Period of military anarchy and decline.',
            description_is='235-270 e.Kr: 37 keisarar á 35 árum. Hermannakeisararnir. Efnahagsleg upplausn. Verðbólga og peningafall.',
            date_start=180,
            date_end=284,
            period=empire,
            civilization=roman_civ,
            region='Roman Empire',
            category='political',
            importance=4
        )
        
        TimelineEvent.objects.get_or_create(
            title='Diocletian Reforms',
            title_is='Umbætur Díókletíanusar',
            description='Diocletian reorganizes the empire.',
            description_is='Endurskipulagning ríkisins. Dóminatus stjórnarfar.',
            date_start=284,
            date_end=305,
            period=empire,
            civilization=roman_civ,
            region='Roman Empire',
            category='political',
            importance=4
        )
        
        TimelineEvent.objects.get_or_create(
            title='Constantine and Christianity',
            title_is='Konstantín og kristni',
            description='Constantine legalizes Christianity and founds Constantinople.',
            description_is='313 e.Kr: Mílanóskipun - kristni lögleidd. 330 e.Kr: Konstantínópel stofnuð. Kristni verður ríkistrú.',
            date_start=306,
            date_end=337,
            period=empire,
            civilization=roman_civ,
            region='Roman Empire',
            category='religious',
            importance=5
        )
        
        TimelineEvent.objects.get_or_create(
            title='Division of Empire',
            title_is='Klofning ríkisins',
            description='Theodosius divides the empire between his sons.',
            description_is='Þeódósíus síðasti keisari yfir öllu ríkinu. Klofning í Vest- og Austrómverska ríki.',
            date_start=395,
            period=empire,
            civilization=roman_civ,
            region='Roman Empire',
            category='political',
            importance=5
        )
        
        TimelineEvent.objects.get_or_create(
            title='Fall of Western Empire',
            title_is='Fall Vestrómverska ríkisins',
            description='Barbarian invasions lead to the fall of the Western Roman Empire.',
            description_is='375 e.Kr: Húnar ráðast inn í Mið-Evrópu. Vestgotar ná Balkanskaga. 378 e.Kr: Rómverjar sigraðir við Adríanópel. 410 e.Kr: Alarik rænir Róm. 451 e.Kr: Húnar sigraðir á Katalónsvöllum. 453 e.Kr: Attila deyr. 455 e.Kr: Vandalar ræna Róm. 476 e.Kr: Ódóvakar rekur síðasta vestrómverska keisara.',
            date_start=375,
            date_end=476,
            period=empire,
            civilization=roman_civ,
            region='Western Roman Empire',
            category='military',
            importance=5
        )
    
    def create_people(self, rom, roman_civ, kingdom, republic, empire):
        # Legendary Founders & Early Kings
        Person.objects.get_or_create(
            name='Romulus',
            name_is='Rómúlus',
            birth_date=None,
            death_date=None,
            category='ruler',
            civilization=roman_civ,
            period=kingdom,
            biography='Legendary founder and first king of Rome.',
            biography_is='Þjóðsagnakonungur, stofnandi Rómar. Bróðir Remus, afkomandi Eneasar Trójukappa. Drap Remus í reiðiskasti. Taldist fyrstur af sjö konungum Rómar. Safnaði 300 landnemum. Nafnið Róm talið komið frá honum.',
            achievements='Founded Rome and established its first laws and customs.',
            achievements_is='Stofnaði Róm og setti fyrstu lög og siði hennar.'
        )
        
        Person.objects.get_or_create(
            name='Remus',
            name_is='Remus',
            birth_date=None,
            death_date=None,
            category='other',
            civilization=roman_civ,
            period=kingdom,
            biography='Twin brother of Romulus.',
            biography_is='Bróðir Rómúlusar. Systkinin björguð af úlf og alin upp af hirði. Drepinn af Rómúlus í deilu um staðsetningu borgar.',
            achievements='Co-founder of Rome according to legend.',
            achievements_is='Meðstofnandi Rómar samkvæmt þjóðsögum.'
        )
        
        Person.objects.get_or_create(
            name='Aeneas',
            name_is='Eneas',
            birth_date=None,
            death_date=None,
            category='other',
            civilization=roman_civ,
            period=kingdom,
            biography='Trojan hero, ancestor of the Romans according to legend.',
            biography_is='Trójukappi, ættfaðir Rómverja samkvæmt þjóðsögum. Flúði frá Tróju eftir eyðileggingu hennar. Afkomandi hans í 10. lið Rómúlus og Remus.',
            achievements='Escaped from Troy and founded a new settlement in Italy.',
            achievements_is='Flúði frá Tróju og stofnaði nýtt byggðarlag á Ítalíu.'
        )
        
        Person.objects.get_or_create(
            name='Tarquinius Superbus',
            name_is='Tarquinius Superbus',
            birth_date=None,
            death_date=None,
            category='ruler',
            civilization=roman_civ,
            period=kingdom,
            biography='Last king of Rome.',
            biography_is='Síðasti konungur Rómar. Etrúskur að uppruna. Hrakinn frá völdum af patríesum 509 f.Kr. Upphaf lýðveldis.',
            achievements='Built the Temple of Jupiter Optimus Maximus.',
            achievements_is='Byggði musteri Júpíters Optimus Maximus.'
        )
        
        # Republic Leaders
        Person.objects.get_or_create(
            name='Tiberius Gracchus',
            name_is='Tiberius Gracchus',
            birth_date=-163,
            death_date=-133,
            category='political',
            civilization=roman_civ,
            period=republic,
            biography='Roman politician who tried to reform land ownership.',
            biography_is='Kjörinn alþýðuforingi 133 f.Kr. Lagði fram tillögu um endurskiptingu þjóðjarða. Vildi styrkja sjálfseignarbændur og minnka þrælahald. Drepinn á kosningadegi af höfðingjum. Byrjaði stéttaátök síðari hluta lýðveldis.',
            achievements='Attempted to redistribute public land to the poor.',
            achievements_is='Reyndi að endurúthluta opinberu landi til fátækra.'
        )
        
        Person.objects.get_or_create(
            name='Gaius Gracchus',
            name_is='Gaius Gracchus',
            birth_date=-153,
            death_date=-121,
            category='political',
            civilization=roman_civ,
            period=republic,
            biography='Roman politician who continued his brother\'s reforms.',
            biography_is='Bróðir Tíberíusar, alþýðuforingi 123 f.Kr. Kom á kornskammti fyrir öreiga. Fól riddurum dómsvald í málum skattlandsbúa. Stofnaði nýlendur fyrir fátæka. Vildi veita Lötum rómverskan borgararétt. Stytti sér aldur 121 f.Kr. þegar 3000 fylgismenn drepnir.',
            achievements='Established grain subsidies for the poor and reformed the judicial system.',
            achievements_is='Kom á kornstyrkjum fyrir fátæka og endurbætti dómskerfið.'
        )
        
        Person.objects.get_or_create(
            name='Gaius Marius',
            name_is='Gaius Marius',
            birth_date=-157,
            death_date=-86,
            category='military',
            civilization=roman_civ,
            period=republic,
            biography='Roman general and statesman.',
            biography_is='Leiðtogi lýðsinna. Endurbætti herinn - tók öreiga í herinn. Kosinn ræðismaður sex sinnum á sjö árum. Sigraði Kimbra og Tevtóna 102-101 f.Kr. Átök við Súllu. Kosinn í sjöunda sinn 86 f.Kr. en lést snemma.',
            achievements='Reformed the Roman army and defeated the Germanic tribes.',
            achievements_is='Endurbætti rómverska herinn og sigraði germönsku ættbálkana.'
        )
        
        Person.objects.get_or_create(
            name='Lucius Cornelius Sulla',
            name_is='Lucius Cornelius Sulla',
            birth_date=-138,
            death_date=-78,
            category='military',
            civilization=roman_civ,
            period=republic,
            biography='Roman general and statesman.',
            biography_is='Höfðingjasinninn, andstæðingur Maríusar. Sigraði Míþridates á Grikklandi. 82 f.Kr: Alræðismaður. Aftökulistar og harð stjórn. Vildi koma öllum völdum í hendur höfðingja. 79 f.Kr: Lagði niður völd sjálfviljugur.',
            achievements='Became dictator of Rome and reformed the constitution.',
            achievements_is='Varð einræðisherra Rómar og endurbætti stjórnarskrána.'
        )
        
        Person.objects.get_or_create(
            name='Marcus Tullius Cicero',
            name_is='Marcus Tullius Cicero',
            birth_date=-106,
            death_date=-43,
            category='political',
            civilization=roman_civ,
            period=republic,
            biography='Roman statesman, lawyer, scholar, and writer.',
            biography_is='Fremsti ræðusnillingur Rómverja. Ræðismaður 63 f.Kr. Afhjúpaði Katilína samsæri. Fjandmaður Antoníusar. Drepinn í ofsóknum þremenninganna 43 f.Kr. Mikilvægar heimildir um síðlýðveldi.',
            achievements='Exposed the Catiline conspiracy and wrote influential works on rhetoric and philosophy.',
            achievements_is='Afhjúpaði Katilína samsæri og skrifaði áhrifamikil verk um mælskufræði og heimspeki.'
        )
        
        Person.objects.get_or_create(
            name='Spartacus',
            name_is='Spartacus',
            birth_date=-109,
            death_date=-71,
            category='military',
            civilization=roman_civ,
            period=republic,
            biography='Thracian gladiator who led a slave uprising.',
            biography_is='Þrák að uppruna, skylmingaþræll. 73 f.Kr: Hóf þrælauppreisn í Kapúu. Réð yfir her tugþúsunda. Náði mörgum héruðum á sitt vald. Féll í bardaga við Krassus 71 f.Kr. Tákn baráttu fyrir frelsi.',
            achievements='Led the Third Servile War, the largest slave rebellion in Roman history.',
            achievements_is='Leiddi þriðja þrælauppreisnina, stærstu þrælauppreisn í sögu Rómar.'
        )
        
        # First Triumvirate
        Person.objects.get_or_create(
            name='Gnaeus Pompeius Magnus',
            name_is='Gnaeus Pompeius Magnus',
            birth_date=-106,
            death_date=-48,
            category='military',
            civilization=roman_civ,
            period=republic,
            biography='Roman general and statesman.',
            biography_is='Pompejus mikli, frægur herforingi. Þjálfaður undir Súllu. 67 f.Kr: Sigraði sjóræningja á þremur mánuðum. 64-63 f.Kr: Sigraði Míþridates, tók Sýrland. Meðlimur fyrra þremenningasambandsins. 49-48 f.Kr: Borgarastyrjöld við Sesar. Sigraður við Farsalos, drepinn í Egyptalandi.',
            achievements='Cleared the Mediterranean of pirates and conquered much of the East.',
            achievements_is='Hreinsaði Miðjarðarhafið af sjóræningjum og lagði undir sig stóran hluta austursins.'
        )
        
        Person.objects.get_or_create(
            name='Marcus Licinius Crassus',
            name_is='Marcus Licinius Crassus',
            birth_date=-115,
            death_date=-53,
            category='political',
            civilization=roman_civ,
            period=republic,
            biography='Roman general and politician.',
            biography_is='Ríkasti maður Rómar. Kaupti eignir á vægu verði í ógnarstjórn Súllu. 71 f.Kr: Bældi niður Spartakus uppreisn. Meðlimur fyrra þremenningasambandsins. 53 f.Kr: Féll í orrustu í Pörþu (Mesópótamíu).',
            achievements='Suppressed the Spartacus rebellion and became the wealthiest man in Rome.',
            achievements_is='Bældi niður Spartakus uppreisnina og varð ríkasti maður Rómar.'
        )
        
        Person.objects.get_or_create(
            name='Gaius Julius Caesar',
            name_is='Gaius Julius Caesar',
            birth_date=-100,
            death_date=-44,
            category='military',
            civilization=roman_civ,
            period=republic,
            biography='Roman general and statesman.',
            biography_is='Af höfðinglegum uppruna en leiðtogi lýðsinna. Stuðlamaður Pompejusar og Krassusar. 59 f.Kr: Ræðismaður. 58-50 f.Kr: Sigraði alla Gallíu. 49 f.Kr: Fór yfir Rúbíkon með "alea iacta est". 48 f.Kr: Sigraði Pompejus við Farsalos. Dvaldi hjá Kleópötru í Egyptalandi. 45 f.Kr: Náði öllu Rómaveldi undir sig. Alræðismaður til lífsstíðar. 44 f.Kr: Myrtur 15. mars á fundi öldungaráðs. Innleiddi júlíanska tímatal.',
            achievements='Conquered Gaul, won the civil war, and became dictator of Rome.',
            achievements_is='Lagði undir sig Gallíu, vann borgarastyrjöldina og varð einræðisherra Rómar.'
        )
        
        # Second Triumvirate
        Person.objects.get_or_create(
            name='Marcus Antonius',
            name_is='Marcus Antonius',
            birth_date=-83,
            death_date=-30,
            category='military',
            civilization=roman_civ,
            period=republic,
            biography='Roman politician and general.',
            biography_is='Náinn samstarfsmaður Sesars. Meðlimur síðara þremenningasambandsins. Fékk skattlönd við austanvert Miðjarðarhaf. Bandalag og hjónaband með Kleópötru. Móðgaði Oktavíanus með tvíkvænni. 31 f.Kr: Sigraður við Aktíum. 30 f.Kr: Réð sér bana í Egyptalandi.',
            achievements='Ruled the eastern provinces of Rome and allied with Cleopatra.',
            achievements_is='Stjórnaði austurhéruðum Rómar og gerði bandalag við Kleópötru.'
        )
        
        Person.objects.get_or_create(
            name='Marcus Aemilius Lepidus',
            name_is='Marcus Aemilius Lepidus',
            birth_date=-89,
            death_date=-12,
            category='political',
            civilization=roman_civ,
            period=republic,
            biography='Roman general and statesman.',
            biography_is='Þriðji meðlimur síðara þremenningasambandsins. Fékk skattlönd Afríku. Oktavíanus tók Afríku frá honum. Hvarf úr stjórnmálum.',
            achievements='Served as Pontifex Maximus and was a member of the Second Triumvirate.',
            achievements_is='Þjónaði sem Pontifex Maximus og var meðlimur síðara þremenningasambandsins.'
        )
        
        Person.objects.get_or_create(
            name='Marcus Junius Brutus',
            name_is='Marcus Junius Brutus',
            birth_date=-85,
            death_date=-42,
            category='political',
            civilization=roman_civ,
            period=republic,
            biography='Roman politician and one of the assassins of Julius Caesar.',
            biography_is='Leiðtogi samsæris gegn Sesari. Sesar hafði reynst honum vel en tregur til þátttöku. Þótti vera afkomandi þess Brútusar sem rak síðasta konunginn. Réð sér bana eftir ósigur.',
            achievements='Led the assassination of Julius Caesar to preserve the Republic.',
            achievements_is='Leiddi morðið á Júlíusi Sesar til að varðveita lýðveldið.'
        )
        
        # Julio-Claudian Emperors
        Person.objects.get_or_create(
            name='Augustus',
            name_is='Ágústus',
            birth_date=-63,
            death_date=14,
            category='ruler',
            civilization=roman_civ,
            period=empire,
            biography='First Roman Emperor.',
            biography_is='Upphaflega Oktavíanus, kjörsonur Sesars. Fyrsti rómverski keisarinn. Fær titilinn Ágústus (hinn virðulegi). Princeps - fyrstur meðal samborgara. 31 f.Kr: Sigraði við Aktíum. Stofnaði pretoríu lífvarðasveit. Leit á sig sem friðarhöfðingja. Endurreisti mörg hof, "fann Róm úr leir, skildi eftir úr marmara". Ætt Júlíana-Kládíanska nefnd eftir honum.',
            achievements='Established the Roman Empire and a period of peace known as Pax Romana.',
            achievements_is='Stofnaði Rómaveldi og tímabil friðar þekkt sem Pax Romana.'
        )
        
        Person.objects.get_or_create(
            name='Tiberius',
            name_is='Tiberius',
            birth_date=-42,
            death_date=37,
            category='ruler',
            civilization=roman_civ,
            period=empire,
            biography='Second Roman Emperor.',
            biography_is='Stjúpsonur Ágústusar (sonur Liviu). Strangur og íhaldssamur keisari. Svipti þjóðfundi löggjafarvaldi. Dvaldi síðustu 11 árin á Capri. Stjórnaði með bréfaskriftum. Valdatími hans var þegar Jesús starfaði. Óvinsæll hjá þjóðinni.',
            achievements='Continued the policies of Augustus and expanded the imperial treasury.',
            achievements_is='Hélt áfram stefnu Ágústusar og stækkaði fjárhirslur keisaradæmisins.'
        )
        
        Person.objects.get_or_create(
            name='Caligula',
            name_is='Kalígúla',
            birth_date=12,
            death_date=41,
            category='ruler',
            civilization=roman_civ,
            period=empire,
            biography='Third Roman Emperor.',
            biography_is='Réttnafn Gajus, kallaður Kalígúla (smáskór). Þriðji keisarinn. Byrjaði vel en varð geðveikur. Einræðislegt stjórnarfar. Vildi láta tigna sig sem guð. Eyddi fjármunum ríkisins. Myrtur af lífvarðasveitunum eftir fjögur ár.',
            achievements='Built temples to himself and attempted to make his horse a consul.',
            achievements_is='Byggði hof til heiðurs sjálfum sér og reyndi að gera hest sinn að ræðismanni.'
        )
        
        Person.objects.get_or_create(
            name='Claudius',
            name_is='Kládíus',
            birth_date=-10,
            death_date=54,
            category='ruler',
            civilization=roman_civ,
            period=empire,
            biography='Fourth Roman Emperor.',
            biography_is='Föðurbróðir Kalígúla. Valinn af lífvarðasveitunum. Óframfærinn og tauaveiklaður fræðimaður. Góður stjórnandi þrátt fyrir líkamlega vanhæfni. Herför til Englands, stofnuð skattlönd. Bætti innviði í Róm (vatnsleiðslur, höfn). Marggiftur, Messalína síðasta kona. Talið að hann hafi verið eitranður.',
            achievements='Conquered Britain and expanded the empire.',
            achievements_is='Lagði undir sig Bretland og stækkaði heimsveldið.'
        )
        
        Person.objects.get_or_create(
            name='Nero',
            name_is='Neró',
            birth_date=37,
            death_date=68,
            category='ruler',
            civilization=roman_civ,
            period=empire,
            biography='Fifth and last Roman Emperor of the Julio-Claudian dynasty.',
            biography_is='Síðasti Júlíaska-Kládíanski keisarinn. Unglingur þegar hann varð keisari. Dáði listir og íþróttir. Lét drepa móður sína, Seneca og konu sína. 64 e.Kr: Eldur í Róm, kenndi kristnum um. Ofsóknir á kristna, Pétur og Páll drepnir. Sang ljóð sín opinberlega. Keppti á Ólympíuleikum. Uppreisn hermanna 68 e.Kr. Réð sér bana með orðunum "qualis artifex pereo".',
            achievements='Built the Domus Aurea and persecuted Christians.',
            achievements_is='Byggði Domus Aurea og ofsótti kristna.'
        )
        
        # Flavian Dynasty
        Person.objects.get_or_create(
            name='Vespasian',
            name_is='Vespaníus',
            birth_date=9,
            death_date=79,
            category='ruler',
            civilization=roman_civ,
            period=empire,
            biography='Roman Emperor who founded the Flavian dynasty.',
            biography_is='Náði völdum eftir árs-fjögurra-keisara 69 e.Kr. Hafði stýrt her í Gyðingalandi. Kom fljótt á frið og reglu. Strangur fjárhag til að bæta úr bruðli Nerós. Byrjaði að byggja Kólósseum. Efldist en tilgát saga kvað "vae, puto deus fio" (vei, ég held ég verði guð).',
            achievements='Restored stability after the Year of the Four Emperors and began construction of the Colosseum.',
            achievements_is='Kom á stöðugleika eftir ár fjögurra keisara og hóf byggingu Kólósseums.'
        )
        
        # Adoptive Emperors
        Person.objects.get_or_create(
            name='Trajan',
            name_is='Trajanus',
            birth_date=53,
            death_date=117,
            category='ruler',
            civilization=roman_civ,
            period=empire,
            biography='Roman Emperor who presided over the greatest military expansion in Roman history.',
            biography_is='Fyrsti skattlandsbúinn keisari (frá Spáni). Frægur herforingi. 101-106 e.Kr: Sigraði Dakíu (Rúmeníu). Miklar gullnámur í Dakíu. Trajansúlan reist til minningar. Vann sigra allt til Persaflóa. Rómaveldi aldrei stærra en við dauða hans. Dýrkaður sem einn besti keisari.',
            achievements='Expanded the Roman Empire to its greatest territorial extent.',
            achievements_is='Stækkaði Rómaveldi í mesta umfang þess.'
        )
        
        Person.objects.get_or_create(
            name='Hadrian',
            name_is='Hadríanus',
            birth_date=76,
            death_date=138,
            category='ruler',
            civilization=roman_civ,
            period=empire,
            biography='Roman Emperor known for his building projects.',
            biography_is='Einnig fæddur á Spáni. Þekktastur fyrir Hadríanusarmúrinn á Englandi (120 km). Ferðaðist um allt heimsveldið. Bætti samgöngur, kom á póstþjónustu. Stofnaði borgir (t.d. Adríanópel). Endurreisti Panþeon í Róm. Skreytti Aþenu með glæsibyggingum. Talinn einn hæfasti keisari Rómaveldis.',
            achievements='Built Hadrian\'s Wall in Britain and rebuilt the Pantheon in Rome.',
            achievements_is='Byggði Hadríanusarmúrinn á Bretlandi og endurbyggði Panþeon í Róm.'
        )
        
        Person.objects.get_or_create(
            name='Marcus Aurelius',
            name_is='Markús Árelíus',
            birth_date=121,
            death_date=180,
            category='ruler',
            civilization=roman_civ,
            period=empire,
            biography='Roman Emperor and Stoic philosopher.',
            biography_is='Síðasti kjörkeisarinn. Heimspekingur á keisarastól. Stóumaður, aðhylltist meinlætakenningar. Höfundur "Meditationes" (Hugleiðingar). Ófrið við Germana suður frá Dóná. Rómverjar héldu þó sínu. Ævilangt stríð og vandræði.',
            achievements='Wrote "Meditations" and defended the empire against Germanic invasions.',
            achievements_is='Skrifaði "Hugleiðingar" og varði heimsveldið gegn innrásum Germana.'
        )
        
        # Late Empire
        Person.objects.get_or_create(
            name='Diocletian',
            name_is='Díókletíanus',
            birth_date=244,
            death_date=311,
            category='ruler',
            civilization=roman_civ,
            period=empire,
            biography='Roman Emperor who reformed the empire after the Crisis of the Third Century.',
            biography_is='Endurskipulagði ríkið eftir krísutímabilið. Dóminatus stjórnarfar. Skráð verðlag til að berjast við verðbólgu. Ofsóknir á kristna.',
            achievements='Divided the empire into four administrative regions and stabilized the economy.',
            achievements_is='Skipti ríkinu í fjögur stjórnsýslusvæði og kom stöðugleika á efnahaginn.'
        )
        
        Person.objects.get_or_create(
            name='Constantine I',
            name_is='Konstantín I',
            birth_date=272,
            death_date=337,
            category='ruler',
            civilization=roman_civ,
            period=empire,
            biography='Roman Emperor who legalized Christianity and founded Constantinople.',
            biography_is='Fyrsti kristni keisarinn. 313 e.Kr: Mílanóskipun - kristni lögleidd. 325 e.Kr: Kirkjuþing í Níkeu. 330 e.Kr: Konstantínópel stofnuð. Sameinaði ríkið undir einn keisara.',
            achievements='Legalized Christianity and founded Constantinople.',
            achievements_is='Lögleiddi kristni og stofnaði Konstantínópel.'
        )
        
        # Foreign Leaders
        Person.objects.get_or_create(
            name='Hannibal Barca',
            name_is='Hannibal Barca',
            birth_date=-247,
            death_date=-183,
            category='military',
            civilization=None,
            period=republic,
            biography='Carthaginian general who fought against Rome in the Second Punic War.',
            biography_is='Stórhershöfðingi Karþagómanna. Sonur Hamílkar, alin upp í hatri á Rómverjum. 221 f.Kr: Yfirhershöfðingi á Spáni. Fór yfir Alpafjöll inn í Ítalíu. 216 f.Kr: Gersigraði Rómverja við Cannae. 202 f.Kr: Sigraður af Skípíó við Zama. Flúði land, varð súfeti í Karþagó. 183 f.Kr: Tók eitur til að forðast handtöku.',
            achievements='Led Carthaginian forces across the Alps and defeated the Romans at Cannae.',
            achievements_is='Leiddi her Karþagómanna yfir Alpafjöll og sigraði Rómverja við Cannae.'
        )
        
        Person.objects.get_or_create(
            name='Cleopatra VII',
            name_is='Kleópatra VII',
            birth_date=-69,
            death_date=-30,
            category='ruler',
            civilization=None,
            period=republic,
            biography='Last active ruler of the Ptolemaic Kingdom of Egypt.',
            biography_is='Síðasta drottning Egyptalands. Af ætt Ptólemósa. Bandalag með Júlíus Sesar, eignuðust son. Giftist Antoníusi. 31 f.Kr: Sigruð við Aktíum. 30 f.Kr: Réð sér bana með eiturbíti slöngv.',
            achievements='Formed alliances with Julius Caesar and Mark Antony to protect Egypt.',
            achievements_is='Myndaði bandalag við Júlíus Sesar og Markús Antoníus til að vernda Egyptaland.'
        )
        
        # Religious Figures
        Person.objects.get_or_create(
            name='Jesus Christ',
            name_is='Jesús Kristur',
            birth_date=-4,
            death_date=30,
            category='religious',
            civilization=None,
            period=empire,
            biography='Central figure of Christianity.',
            biography_is='Stofnandi kristninnar. Starfaði á valdatíma Tíberíusar. Krossfestur í Jerúsalem. Kenningar hans urðu grunnur kristinnar trúar.',
            achievements='Founded Christianity, which later became the official religion of the Roman Empire.',
            achievements_is='Stofnaði kristni, sem síðar varð opinber trú Rómaveldis.'
        )
        
        # Philosophers & Writers
        Person.objects.get_or_create(
            name='Seneca',
            name_is='Seneca',
            birth_date=-4,
            death_date=65,
            category='philosopher',
            civilization=roman_civ,
            period=empire,
            biography='Roman Stoic philosopher, statesman, and dramatist.',
            biography_is='Lucius Annaeus Seneca. Stóískur heimspekingur. Kennari og ráðgjafi Nerós. Skrifaði um siðfræði og stjórnmálaheimseki. Neyddur til sjálfsmorðs af Neró.',
            achievements='Wrote influential works on Stoicism and served as advisor to Nero.',
            achievements_is='Skrifaði áhrifamikil verk um stóuspeki og þjónaði sem ráðgjafi Nerós.'
        )
        
        Person.objects.get_or_create(
            name='Tacitus',
            name_is='Tacitus',
            birth_date=56,
            death_date=120,
            category='philosopher',
            civilization=roman_civ,
            period=empire,
            biography='Roman historian and politician.',
            biography_is='Publius Cornelius Tacitus. Frægasti rómverski sagnaritari. Skrifaði "Germanía" um germanska þjóð. "Annales" og "Historiae" um keisaraöld. Svartsýnn á spillingu rómverks samfélag.',
            achievements='Wrote major historical works including "Histories" and "Annals."',
            achievements_is='Skrifaði mikilvæg sagnfræðileg verk, þar á meðal "Historiae" og "Annales".'
        )
    
    def create_cultural_topics(self, rom, roman_civ):
        CulturalTopic.objects.get_or_create(
            title='Roman Social Structure',
            title_is='Þjóðfélagsuppbygging Rómar',
            category='social_classes',
            civilization=roman_civ,
            period=rom,
            content='The social structure of ancient Rome was hierarchical.',
            content_is='Patríesar: meðlimir fornu ættanna, jarðeignaraðall. Plebejar: aðkomumenn, borgarastétt. Skjólstæðingar (clients): í þjónustu patríesa. Þrælar: fámennir á konungaöldinni.'
        )
        
        CulturalTopic.objects.get_or_create(
            title='Roman Government',
            title_is='Stjórnskipulag Rómar',
            category='social_classes',
            civilization=roman_civ,
            period=rom,
            content='The government of Rome evolved from monarchy to republic to empire.',
            content_is='Stjórnskipulag Rómar þróaðist frá konungdæmi til lýðveldis til keisaradæmis. Lýðveldið var stjórnað af tveimur ræðismönnum, öldungaráði og þjóðfundum. Keisaradæmið var stjórnað af keisara með stuðningi embættismanna og hersins.'
        )
        
        CulturalTopic.objects.get_or_create(
            title='Roman Architecture',
            title_is='Rómversk byggingarlist',
            category='art',
            civilization=roman_civ,
            period=rom,
            content='Roman architecture was known for its durability, utility, and beauty.',
            content_is='Rómversk byggingarlist var þekkt fyrir endingu, notagildi og fegurð. Rómverjar þróuðu bogann, hvelfinguna og steinsteypu. Þeir byggðu vegakerfi, brýr, vatnsleiðslur, baðhús, amfíteatrar og hof.'
        )
        
        CulturalTopic.objects.get_or_create(
            title='Roman Law',
            title_is='Rómverskur réttur',
            category='daily_life',
            civilization=roman_civ,
            period=rom,
            content='Roman law was one of Rome\'s most important contributions to civilization.',
            content_is='Rómverskur réttur var eitt mikilvægasta framlag Rómar til siðmenningar. Hann var skráður í Tólf bronstöflur og síðar í Corpus Juris Civilis. Rómverskur réttur er grunnur að mörgum nútíma lagakerfum.'
        )
        
        CulturalTopic.objects.get_or_create(
            title='Roman Religion',
            title_is='Rómversk trúarbrögð',
            category='religion',
            civilization=roman_civ,
            period=rom,
            content='Roman religion was polytheistic and influenced by Greek religion.',
            content_is='Rómversk trúarbrögð voru fjölgyðistrú og undir áhrifum frá grískri trú. Rómverjar dýrkuðu marga guði, þar á meðal Júpíter, Júnó, Minervu, Mars og Venus. Kristni varð ríkistrú á 4. öld e.Kr.'
        )
    
    def create_battles(self, rom, roman_civ):
        Battle.objects.get_or_create(
            name='Battle of Cannae',
            name_is='Orrusta við Cannae',
            date=-216,
            location='Cannae, Italy',
            period=rom,
            description='A major battle of the Second Punic War, where Hannibal defeated the Romans.',
            description_is='Mikil orrusta í öðru púnverska stríðinu, þar sem Hannibal sigraði Rómverja. Hannibal umkringdi rómverska herinn og drap um 50.000-70.000 hermenn.',
            outcome='Carthaginian victory',
            outcome_is='Sigur Karþagómanna',
            significance='One of the worst defeats in Roman military history.',
            significance_is='Eitt versta ósigur í hernaðarsögu Rómverja.'
        )
        
        Battle.objects.get_or_create(
            name='Battle of Zama',
            name_is='Orrusta við Zama',
            date=-202,
            location='Zama, North Africa',
            period=rom,
            description='The final battle of the Second Punic War, where Scipio defeated Hannibal.',
            description_is='Lokabardagi annars púnverska stríðsins, þar sem Skípíó sigraði Hannibal. Skípíó notaði svipaða herkænsku og Hannibal hafði notað við Cannae.',
            outcome='Roman victory',
            outcome_is='Sigur Rómverja',
            significance='Ended the Second Punic War and established Rome as the dominant power in the Western Mediterranean.',
            significance_is='Lauk öðru púnverska stríðinu og staðfesti Róm sem ráðandi afl í vesturhluta Miðjarðarhafs.'
        )
        
        Battle.objects.get_or_create(
            name='Battle of Pharsalus',
            name_is='Orrusta við Farsalos',
            date=-48,
            location='Pharsalus, Greece',
            period=rom,
            description='A decisive battle of Caesar\'s Civil War, where Caesar defeated Pompey.',
            description_is='Úrslitaorrusta í borgarastyrjöld Sesars, þar sem Sesar sigraði Pompejus. Þrátt fyrir að vera í minnihluta, sigraði Sesar með betri herkænsku.',
            outcome='Victory for Caesar',
            outcome_is='Sigur fyrir Sesar',
            significance='Effectively ended the Roman Republic and paved the way for the Roman Empire.',
            significance_is='Í raun lauk rómverska lýðveldinu og ruddi brautina fyrir Rómaveldi.'
        )
        
        Battle.objects.get_or_create(
            name='Battle of Actium',
            name_is='Orrusta við Aktíum',
            date=-31,
            location='Actium, Greece',
            period=rom,
            description='A naval battle that decided the Final War of the Roman Republic.',
            description_is='Sjóorrusta sem réð úrslitum í lokastríði rómverska lýðveldisins. Oktavíanus (síðar Ágústus) sigraði Antoníus og Kleópötru.',
            outcome='Victory for Octavian',
            outcome_is='Sigur fyrir Oktavíanus',
            significance='Established Octavian as the sole ruler of Rome and began the Roman Empire.',
            significance_is='Staðfesti Oktavíanus sem einvald Rómar og hóf Rómaveldi.'
        )
        
        Battle.objects.get_or_create(
            name='Battle of Teutoburg Forest',
            name_is='Orrusta í Teutoborgarlandi',
            date=9,
            location='Teutoburg Forest, Germany',
            period=rom,
            description='A battle where Germanic tribes ambushed and destroyed three Roman legions.',
            description_is='Orrusta þar sem germanskir ættbálkar gerðu launsókn á og eyðilögðu þrjár rómverskar hersveitir. Arminius, germanskur höfðingi sem hafði þjálfun í rómverska hernum, leiddi árásina.',
            outcome='Germanic victory',
            outcome_is='Sigur Germana',
            significance='Stopped Roman expansion into Germania and established the Rhine as the border of the Roman Empire.',
            significance_is='Stöðvaði útþenslu Rómverja inn í Germaníu og staðfesti Rín sem landamæri Rómaveldis.'
        )
        
        Battle.objects.get_or_create(
            name='Battle of Adrianople',
            name_is='Orrusta við Adríanópel',
            date=378,
            location='Adrianople, Turkey',
            period=rom,
            description='A battle between the Eastern Roman Empire and the Goths.',
            description_is='Orrusta milli Austrómverska ríkisins og Gota. Gotar sigruðu og drápu keisara Valens.',
            outcome='Gothic victory',
            outcome_is='Sigur Gota',
            significance='Marked the beginning of the fall of the Western Roman Empire.',
            significance_is='Markaði upphaf falls Vestrómverska ríkisins.'
        )
        
        Battle.objects.get_or_create(
            name='Battle of the Catalaunian Plains',
            name_is='Orrusta á Katalónsvöllum',
            date=451,
            location='Catalaunian Plains, France',
            period=rom,
            description='A battle between a coalition led by the Roman general Aetius and the Huns led by Attila.',
            description_is='Orrusta milli bandalags undir forystu rómverska hershöfðingjans Aetius og Húna undir forystu Attila. Bandalagið samanstóð af Rómverjum, Vestgotum og öðrum germönskum ættbálkum.',
            outcome='Roman coalition victory',
            outcome_is='Sigur rómverska bandalagsins',
            significance='Stopped Attila\'s invasion of Western Europe.',
            significance_is='Stöðvaði innrás Attila í Vestur-Evrópu.'
        )
    
    def create_quiz(self, rom):
        # Create a quiz about the Roman Empire
        quiz, created = Quiz.objects.get_or_create(
            title='Roman Empire Quiz',
            title_is='Próf um Rómaveldi',
            description='Test your knowledge about the Roman Empire.',
            description_is='Prófaðu þekkingu þína á Rómaveldi.',
            quiz_type='period',
            period=rom,
            difficulty=3,
            is_published=True
        )
        
        if created:
            # Create questions for the quiz using the provided questions
            questions = [
                {
                    'question': 'According to Varro, when was Rome founded?',
                    'question_is': 'Samkvæmt Varró, hvenær var Róm stofnuð?',
                    'type': 'multiple_choice',
                    'options': '["21. apríl 752 f.Kr.", "21. apríl 753 f.Kr.", "21. apríl 754 f.Kr.", "21. apríl 755 f.Kr."]',
                    'correct': '1',
                    'explanation': 'According to Varro, Rome was founded on April 21, 753 BCE.',
                    'explanation_is': 'Samkvæmt Varró var Róm stofnuð 21. apríl 753 f.Kr.'
                },
                {
                    'question': 'Who were the legendary founders of Rome?',
                    'question_is': 'Hverjir voru þjóðsagnasstofnendur Rómar?',
                    'type': 'multiple_choice',
                    'options': '["Éneas og Lavínus", "Rómúlus og Remus", "Númitor og Amúlíus", "Faunus og Pikus"]',
                    'correct': '1',
                    'explanation': 'According to legend, Rome was founded by the twin brothers Romulus and Remus.',
                    'explanation_is': 'Samkvæmt þjóðsögum var Róm stofnuð af tvíburabræðrunum Rómúlusi og Remus.'
                },
                {
                    'question': 'What was the name of the hill where "Romulus\'s hut" stood?',
                    'question_is': 'Hvað hét hæðin þar sem "kofi Rómúlusar" stóð?',
                    'type': 'multiple_choice',
                    'options': '["Kapítolhæð", "Palatínhæð", "Aventínhæð", "Viminalhæð"]',
                    'correct': '1',
                    'explanation': 'Romulus\'s hut stood on the Palatine Hill.',
                    'explanation_is': 'Kofi Rómúlusar stóð á Palatínhæð.'
                },
                {
                    'question': 'How many settlers came with Romulus according to legend?',
                    'question_is': 'Hve margir landnemar komu með Rómúlus samkvæmt þjóðsögnum?',
                    'type': 'multiple_choice',
                    'options': '["200", "300", "400", "500"]',
                    'correct': '1',
                    'explanation': 'According to legend, 300 settlers came with Romulus.',
                    'explanation_is': 'Samkvæmt þjóðsögum komu 300 landnemar með Rómúlusi.'
                },
                {
                    'question': 'Who was the last king of Rome?',
                    'question_is': 'Hver var síðasti konungur Rómar?',
                    'type': 'multiple_choice',
                    'options': '["Servius Tullius", "Tarquinius Priscus", "Tarquinius Superbus", "Ancus Marcius"]',
                    'correct': '2',
                    'explanation': 'Tarquinius Superbus was the last king of Rome.',
                    'explanation_is': 'Tarquinius Superbus var síðasti konungur Rómar.'
                },
                {
                    'question': 'When was the Republic established?',
                    'question_is': 'Hvenær var lýðveldið stofnað?',
                    'type': 'multiple_choice',
                    'options': '["508 f.Kr.", "509 f.Kr.", "510 f.Kr.", "511 f.Kr."]',
                    'correct': '1',
                    'explanation': 'The Roman Republic was established in 509 BCE.',
                    'explanation_is': 'Rómverska lýðveldið var stofnað árið 509 f.Kr.'
                },
                {
                    'question': 'What were patricians?',
                    'question_is': 'Hvað voru patríesar?',
                    'type': 'multiple_choice',
                    'options': '["Útlendingar", "Þrælar", "Meðlimir fornu ættanna", "Kaupmenn"]',
                    'correct': '2',
                    'explanation': 'Patricians were members of the original families of Rome, the aristocracy.',
                    'explanation_is': 'Patríesar voru meðlimir fornu ættanna, jarðeignaraðall.'
                },
                {
                    'question': 'What were plebeians?',
                    'question_is': 'Hvað voru plebejar?',
                    'type': 'multiple_choice',
                    'options': '["Aðalsmenn", "Aðkomumenn, borgarastétt", "Þrælar", "Hermenn"]',
                    'correct': '1',
                    'explanation': 'Plebeians were the common citizens of Rome.',
                    'explanation_is': 'Plebejar voru aðkomumenn, borgarastétt.'
                },
                {
                    'question': 'When were the Twelve Tables set?',
                    'question_is': 'Hvenær voru tólf bronstöflur settar?',
                    'type': 'multiple_choice',
                    'options': '["449 f.Kr.", "450 f.Kr.", "451 f.Kr.", "452 f.Kr."]',
                    'correct': '1',
                    'explanation': 'The Twelve Tables were set in 450 BCE.',
                    'explanation_is': 'Tólf bronstöflur voru settar árið 450 f.Kr.'
                },
                {
                    'question': 'What did "veto" mean?',
                    'question_is': 'Hvað þýddi "veto"?',
                    'type': 'multiple_choice',
                    'options': '["Ég samþykki", "Ég banna", "Ég efast", "Ég styð"]',
                    'correct': '1',
                    'explanation': 'Veto meant "I forbid" in Latin.',
                    'explanation_is': 'Veto þýddi "Ég banna" á latínu.'
                },
                {
                    'question': 'When did the Gauls attack Rome and burn the city?',
                    'question_is': 'Hvenær réðust Gallar á Róm og brenndu borgina?',
                    'type': 'multiple_choice',
                    'options': '["Um 390 f.Kr.", "Um 380 f.Kr.", "Um 400 f.Kr.", "Um 370 f.Kr."]',
                    'correct': '0',
                    'explanation': 'The Gauls attacked Rome and burned the city around 390 BCE.',
                    'explanation_is': 'Gallar réðust á Róm og brenndu borgina um 390 f.Kr.'
                },
                {
                    'question': 'Who was the king of Epirus who helped Tarentum?',
                    'question_is': 'Hver var konungur Epeiros sem hjálpaði Tarentum?',
                    'type': 'multiple_choice',
                    'options': '["Alexander", "Pyrros", "Démetruis", "Perseifur"]',
                    'correct': '1',
                    'explanation': 'Pyrrhus was the king of Epirus who helped Tarentum.',
                    'explanation_is': 'Pyrros var konungur Epeiros sem hjálpaði Tarentum.'
                },
                {
                    'question': 'What are Pyrrhic victories?',
                    'question_is': 'Hvað eru pyrrhosarsigar?',
                    'type': 'multiple_choice',
                    'options': '["Auðveldur sigur", "Sigur í sjóorrustu", "Dýrkeyptur sigur", "Sigur með blekkingu"]',
                    'correct': '2',
                    'explanation': 'Pyrrhic victories are victories that come at a great cost, making them tantamount to defeat.',
                    'explanation_is': 'Pyrrhosarsigar eru dýrkeyptir sigrar, þar sem kostnaðurinn er svo mikill að sigurinn er nánast jafn slæmur og ósigur.'
                },
                {
                    'question': 'When had the Romans conquered all of Italy?',
                    'question_is': 'Hvenær höfðu Rómverjar náð allri Ítalíu?',
                    'type': 'multiple_choice',
                    'options': '["Um 270 f.Kr.", "Um 260 f.Kr.", "Um 250 f.Kr.", "Um 240 f.Kr."]',
                    'correct': '1',
                    'explanation': 'The Romans had conquered all of Italy by around 260 BCE.',
                    'explanation_is': 'Rómverjar höfðu náð allri Ítalíu um 260 f.Kr.'
                },
                {
                    'question': 'Where was Carthage?',
                    'question_is': 'Hvar var Karþagó?',
                    'type': 'multiple_choice',
                    'options': '["Á Spáni", "Á Sikiley", "Í Norður-Afríku", "Í Litlu-Asíu"]',
                    'correct': '2',
                    'explanation': 'Carthage was in North Africa, in modern-day Tunisia.',
                    'explanation_is': 'Karþagó var í Norður-Afríku, í núverandi Túnis.'
                }
            ]
            
            for q in questions:
                Question.objects.create(
                    quiz=quiz,
                    question_text=q['question'],
                    question_text_is=q['question_is'],
                    question_type=q['type'],
                    options=q['options'],
                    correct_answer=q['correct'],
                    explanation=q['explanation'],
                    explanation_is=q['explanation_is'],
                    difficulty=3,
                    points=1
                )