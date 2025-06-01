import os
import django
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import HistoricalPeriod, Civilization
from timeline.models import TimelineEvent
from reference.models import Person, Deity, CulturalTopic
from quiz.models import Quiz, Question

class Command(BaseCommand):
    help = 'Populates the database with Greek content'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database with Greek content...')
        
        # Get the Greek period and civilization
        try:
            grikkland = HistoricalPeriod.objects.get(name_is='Grikkland')
            greek_civ = Civilization.objects.get(name_is='Forngrikkir')
            archaic = HistoricalPeriod.objects.get(name_is='Forngrískt tímabil')
            classical = HistoricalPeriod.objects.get(name_is='Klassískt tímabil')
            hellenistic = HistoricalPeriod.objects.get(name_is='Hellenska tímabilið')
        except HistoricalPeriod.DoesNotExist:
            self.stdout.write(self.style.ERROR('Historical periods not found. Run populate_periods command first.'))
            return
        except Civilization.DoesNotExist:
            self.stdout.write(self.style.ERROR('Greek civilization not found. Run populate_periods command first.'))
            return
        
        # Create timeline events
        self.create_timeline_events(grikkland, greek_civ, archaic, classical, hellenistic)
        
        # Create people
        self.create_people(grikkland, greek_civ)
        
        # Create deities
        self.create_deities(greek_civ)
        
        # Create cultural topics
        self.create_cultural_topics(grikkland, greek_civ)
        
        # Create quiz
        self.create_quiz(grikkland)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated Greek content'))
    
    def create_timeline_events(self, grikkland, greek_civ, archaic, classical, hellenistic):
        # Pre-Greek Civilizations
        TimelineEvent.objects.get_or_create(
            title='Minoan Civilization',
            title_is='Krítverjar (Mínósk menning)',
            description='The Minoan civilization was a Bronze Age Aegean civilization on the island of Crete.',
            description_is='3000 f.Kr: Frumbyggjar mynda menningarsamfélög á Krít\n2500 f.Kr: Læra að vinna úr bronsi, byrja skipsmíði\n2000-1400 f.Kr: Blómatími með siglingum og verslun\nUm 1900: Arthur Evans byrjar fornleifauppgröft í Knossos\n1400 f.Kr: Fall mínóskrar menningar (eldgos eða innrás)',
            date_start=-3000,
            date_end=-1400,
            period=grikkland,
            civilization=greek_civ,
            region='Crete',
            category='cultural',
            importance=4
        )
        
        TimelineEvent.objects.get_or_create(
            title='Mycenaean Civilization',
            title_is='Mýkenumenn (Akkerar)',
            description='The Mycenaean civilization was a Late Bronze Age civilization of Ancient Greece.',
            description_is='2000 f.Kr: Fyrstu Indóevrópumenn streyma til Grikklands\n1600-1100 f.Kr: Mýkenska menning í blóma\n1200 f.Kr: Trójustríð og eyðilegging Tróju\n1100 f.Kr: Innrás Dóra, hrun Mýkenumenningarinnar\n1100-800 f.Kr: Hinar myrku aldir í Grikklandi',
            date_start=-1600,
            date_end=-1100,
            period=grikkland,
            civilization=greek_civ,
            region='Mainland Greece',
            category='cultural',
            importance=4
        )
        
        # Archaic Period
        TimelineEvent.objects.get_or_create(
            title='Beginning of Ancient Greek History',
            title_is='Saga Grikkja hinna fornu hefst',
            description='The beginning of Ancient Greek history with the formation of city-states.',
            description_is='Saga Grikkja hinna fornu hefst, borgríki myndast',
            date_start=-800,
            period=archaic,
            civilization=greek_civ,
            region='Greece',
            category='political',
            importance=5
        )
        
        TimelineEvent.objects.get_or_create(
            title='First Olympic Games',
            title_is='Fyrstu Ólympíuleikarnir',
            description='The first Olympic Games according to the Greeks.',
            description_is='Fyrstu Ólympíuleikarnir (samkvæmt Grikkjum)',
            date_start=-776,
            period=archaic,
            civilization=greek_civ,
            region='Olympia',
            category='cultural',
            importance=4
        )
        
        TimelineEvent.objects.get_or_create(
            title='Greek Colonization Period',
            title_is='Nýlendutíminn',
            description='Greeks establish colonies throughout the Mediterranean.',
            description_is='Nýlendutíminn - Grikkir stofna nýlendur',
            date_start=-750,
            date_end=-550,
            period=archaic,
            civilization=greek_civ,
            region='Mediterranean',
            category='political',
            importance=4
        )
        
        # Classical Period
        TimelineEvent.objects.get_or_create(
            title='Battle of Marathon',
            title_is='Orrusta við Maraþon',
            description='The Battle of Marathon was fought between the citizens of Athens and the Persian Empire.',
            description_is='Orrusta við Maraþon',
            date_start=-490,
            period=classical,
            civilization=greek_civ,
            region='Marathon',
            category='military',
            importance=5
        )
        
        TimelineEvent.objects.get_or_create(
            title='Battles of Thermopylae and Salamis',
            title_is='Orrustur við Laugarskarð og Salamis',
            description='The Battles of Thermopylae and Salamis were fought between the Greeks and Persians.',
            description_is='Orrustur við Laugarskarð og Salamis',
            date_start=-480,
            period=classical,
            civilization=greek_civ,
            region='Thermopylae and Salamis',
            category='military',
            importance=5
        )
        
        TimelineEvent.objects.get_or_create(
            title='Age of Pericles',
            title_is='Períklesaröld í Aþenu',
            description='The Age of Pericles was a period of Athenian political hegemony, economic growth, and cultural flourishing.',
            description_is='Períklesaröld í Aþenu',
            date_start=-460,
            date_end=-430,
            period=classical,
            civilization=greek_civ,
            region='Athens',
            category='political',
            importance=5
        )
        
        TimelineEvent.objects.get_or_create(
            title='Peloponnesian War',
            title_is='Pelópsskagastríð',
            description='The Peloponnesian War was fought between Athens and Sparta.',
            description_is='Pelópsskagastríð',
            date_start=-431,
            date_end=-404,
            period=classical,
            civilization=greek_civ,
            region='Greece',
            category='military',
            importance=5
        )
        
        # Hellenistic Period
        TimelineEvent.objects.get_or_create(
            title='Alexander the Great',
            title_is='Alexander mikli',
            description='Alexander the Great was a king of the ancient Greek kingdom of Macedon.',
            description_is='Alexander mikli',
            date_start=-334,
            date_end=-323,
            period=hellenistic,
            civilization=greek_civ,
            region='Mediterranean and Asia',
            category='political',
            importance=5
        )
    
    def create_people(self, grikkland, greek_civ):
        # Rulers & Political Leaders
        Person.objects.get_or_create(
            name='Solon',
            name_is='Sólon',
            birth_date=-630,
            death_date=-560,
            category='political',
            civilization=greek_civ,
            period=grikkland,
            biography='Solon was an Athenian statesman, lawmaker, and poet.',
            biography_is='Aþenskur löggjafi og stjórnmálamaður\nGerður arkon 595 f.Kr. til að leysa stéttaátök\nLagði bann við þrældómi vegna skulda\nSkipti borgurum í fjórar stéttir eftir eignum\nStofnaði 400 manna ráð og þjóðdómstól\nKallaður merkasti löggjafi Grikkja',
            achievements='Solon enacted reforms to solve the economic and political crisis in Athens.',
            achievements_is='Sólon gerði umbætur til að leysa efnahags- og stjórnmálakreppu í Aþenu.'
        )
        
        Person.objects.get_or_create(
            name='Pericles',
            name_is='Períkles',
            birth_date=-495,
            death_date=-429,
            category='political',
            civilization=greek_civ,
            period=grikkland,
            biography='Pericles was a prominent and influential Greek statesman, orator and general of Athens during its golden age.',
            biography_is='Leiðtogi Aþeninga 460-430 f.Kr.\nKosinn yfirhershöfðingi hvað eftir annað\nMarkmið að gera Aþenu að stórveldi\nLét reisa Parþenon á Akrópólishæð\nVeitti fleiri stéttum aðgang að embættum\nHóf launagreiðslu fyrir opinber störf',
            achievements='Pericles led Athens during its Golden Age and promoted arts and literature.',
            achievements_is='Períkles leiddi Aþenu á gullöld sinni og studdi listir og bókmenntir.'
        )
        
        # Military Leaders
        Person.objects.get_or_create(
            name='Miltiades',
            name_is='Miltíades',
            birth_date=-550,
            death_date=-489,
            category='military',
            civilization=greek_civ,
            period=grikkland,
            biography='Miltiades was an Athenian general who led the victory over the Persians at Marathon.',
            biography_is='Aþenskur herforingi\nSigraði Persa við Maraþon 490 f.Kr.\nBeitti herbragði og umkringdi Persa\n192 Aþeningar féllu en 6000 Persar',
            achievements='Miltiades defeated the Persians at the Battle of Marathon in 490 BCE.',
            achievements_is='Miltíades sigraði Persa í orrustu við Maraþon árið 490 f.Kr.'
        )
        
        Person.objects.get_or_create(
            name='Leonidas',
            name_is='Leónídas',
            birth_date=-540,
            death_date=-480,
            category='military',
            civilization=greek_civ,
            period=grikkland,
            biography='Leonidas was a king of the Greek city-state of Sparta.',
            biography_is='Konungur Spartverja\nVarði Laugarskarð með 300 Spartverjum\nFéll eftir hetjulega vörn gegn Persum\nGerði Persum kleift að komast suður í Grikkland',
            achievements='Leonidas led the defense of Thermopylae against the Persians.',
            achievements_is='Leónídas leiddi vörn Laugarskarðs gegn Persum.'
        )
        
        # Philosophers
        Person.objects.get_or_create(
            name='Socrates',
            name_is='Sókrates',
            birth_date=-469,
            death_date=-399,
            category='philosopher',
            civilization=greek_civ,
            period=grikkland,
            biography='Socrates was a Greek philosopher from Athens who is credited as one of the founders of Western philosophy.',
            biography_is='Fyrsti heimspekingurinn sem gerir siðfræði að aðaláherslu\n"Faðir siðfræðinnar"\nTaldi sannleik felast í siðferðilegum hugtökum\nSagði þekkingu vera dyggð\nDæmdur til dauða og drakk eitur 399 f.Kr.',
            achievements='Socrates developed the Socratic method and influenced the development of Western philosophy.',
            achievements_is='Sókrates þróaði sókratíska aðferð og hafði áhrif á þróun vestrænnar heimspeki.'
        )
        
        Person.objects.get_or_create(
            name='Plato',
            name_is='Platón',
            birth_date=-427,
            death_date=-347,
            category='philosopher',
            civilization=greek_civ,
            period=grikkland,
            biography='Plato was an Athenian philosopher during the Classical period in Ancient Greece.',
            biography_is='Lærisveinn Sókrates\nStofnaði skólann Akademía 387 f.Kr.\nSetti fram frumyndakenninguna\nRitaði um fyrirmyndarríki (útópíu)\nAkademían starfrækt í níu aldir',
            achievements='Plato founded the Academy in Athens and wrote numerous philosophical dialogues.',
            achievements_is='Platón stofnaði Akademíuna í Aþenu og skrifaði fjölda heimspekilegra samræðna.'
        )
        
        Person.objects.get_or_create(
            name='Aristotle',
            name_is='Aristóteles',
            birth_date=-384,
            death_date=-322,
            category='philosopher',
            civilization=greek_civ,
            period=grikkland,
            biography='Aristotle was a Greek philosopher and polymath during the Classical period in Ancient Greece.',
            biography_is='Lærisveinn Platóns\nKennari Alexanders mikla\nStofnaði skólann Lykeion\nFjölhæfastur allra fræðimanna fornaldar\nLagði grunn að hugmyndum um lýðræði',
            achievements='Aristotle made significant contributions to logic, metaphysics, mathematics, physics, biology, botany, ethics, politics, agriculture, medicine, dance, and theatre.',
            achievements_is='Aristóteles lagði mikið af mörkum til rökfræði, frumspeki, stærðfræði, eðlisfræði, líffræði, grasafræði, siðfræði, stjórnmálafræði, landbúnaðar, læknisfræði, dans og leikhúss.'
        )
        
        # Scientists & Scholars
        Person.objects.get_or_create(
            name='Hippocrates',
            name_is='Hippókrates',
            birth_date=-460,
            death_date=-370,
            category='scientist',
            civilization=greek_civ,
            period=grikkland,
            biography='Hippocrates was a Greek physician of the Age of Pericles.',
            biography_is='"Faðir læknisfræðinnar"\nFrá eyjunni Kos\nTaldi sjúkdóma hafa náttúrulegar orsakir\nHippókratesareiðurinn kenndur við hann',
            achievements='Hippocrates is considered one of the most outstanding figures in the history of medicine.',
            achievements_is='Hippókrates er talinn ein af merkustu persónum í sögu læknisfræðinnar.'
        )
    
    def create_deities(self, greek_civ):
        # Olympian Gods
        Deity.objects.get_or_create(
            name='Zeus',
            name_is='Seifur',
            civilization=greek_civ,
            domain='King of the gods, god of the sky, lightning, thunder, law, order, and justice',
            domain_is='Æðstur Ólympsguða, himnaguð og þrumuguð',
            symbols='Thunderbolt, eagle, bull, oak',
            symbols_is='Eldingin, örninn, Ægisskjöldurinn',
            mythology='Zeus was the king of the gods and the god of the sky, lightning, thunder, law, order, and justice. He was the youngest son of Cronus and Rhea.',
            mythology_is='Seifur var æðstur Ólympsguða, himnaguð og þrumuguð. Hann var guð laga og reglu, veðraguð. Hann var dómari í þrætum guðanna og verndari ættartengsla og borgríkjasamfélagsins. Hann var faðir margra guða og hetja (Herakles, Perseifur, Mínos).',
            cultural_significance='Zeus was the most important deity in the Greek pantheon and was widely worshipped across Greece.',
            cultural_significance_is='Seifur var mikilvægasta guðdómurinn í gríska guðaheiminum og var víða dýrkaður um allt Grikkland.'
        )
        
        Deity.objects.get_or_create(
            name='Athena',
            name_is='Aþena',
            civilization=greek_civ,
            domain='Goddess of wisdom, handicraft, and warfare',
            domain_is='Gyðja visku, snilli, hernaðarkænsku, handiðna og lista',
            symbols='Owl, olive tree, snake, Aegis',
            symbols_is='Vopn og herklæði, ugla, Ægisskjöldur',
            mythology='Athena was the goddess of wisdom, handicraft, and warfare. She was born from the forehead of Zeus.',
            mythology_is='Aþena var gyðja visku, snilli, hernaðarkænsku, handiðna og lista. Hún var borgargyðja Aþenu og meygyðja. Hún fæddist úr höfði Seifs, móðir hennar var Metis (viskan). Hún fann upp vagna, plóga, skip, málaralist og höggmyndalist.',
            cultural_significance='Athena was the patron goddess of Athens and was highly revered throughout Greece.',
            cultural_significance_is='Aþena var verndardís Aþenu og var mjög virt um allt Grikkland.'
        )
        
        Deity.objects.get_or_create(
            name='Apollo',
            name_is='Apollon',
            civilization=greek_civ,
            domain='God of music, arts, knowledge, healing, plague, prophecy, poetry, manly beauty, and archery',
            domain_is='Guð ljóss, hreysti, heilbrigðis, líkamsfegurðar',
            symbols='Lyre, laurel wreath, python, bow and arrows',
            symbols_is='Harpa, lárviður og bogi',
            mythology='Apollo was the god of music, arts, knowledge, healing, plague, prophecy, poetry, manly beauty, and archery.',
            mythology_is='Apollon var guð ljóss, hreysti, heilbrigðis og líkamsfegurðar. Hann var einnig guð tónlistar, skáldskapar og bogfimi. Hann glæddi mannlífið með gleði og fegurð. Hann var einn ástsælasti guð Grikkja. Spásagnastaður hans var í Delfí, þar sem hann drap slönguna Pýþon. Hann var faðir Asklepíos lækningaguðs.',
            cultural_significance='Apollo was one of the most important and complex of the Olympian deities in ancient Greek religion and mythology.',
            cultural_significance_is='Apollon var einn af mikilvægustu og flóknustu Ólympsguðunum í trúarbrögðum og goðafræði fornra Grikkja.'
        )
        
        Deity.objects.get_or_create(
            name='Poseidon',
            name_is='Póseidon',
            civilization=greek_civ,
            domain='God of the sea, earthquakes, storms, and horses',
            domain_is='Konungur sjávarins, guð jarðskjálfta',
            symbols='Trident, horse, dolphin',
            symbols_is='Þríforkurinn',
            mythology='Poseidon was the god of the sea, earthquakes, storms, and horses.',
            mythology_is='Póseidon var konungur sjávarins og guð jarðskjálfta. Hestar og naut voru helguð honum. Hann dvaldi í höll sinni á sjávarbotni. Hann keppti við Aþenu um að verða borgarguð Aþenu. Hann var faðir Trítons, Pólýfemos og Pegasos.',
            cultural_significance='Poseidon was widely worshipped throughout Greece, especially in coastal regions.',
            cultural_significance_is='Póseidon var víða dýrkaður um allt Grikkland, sérstaklega á strandsvæðum.'
        )
    
    def create_cultural_topics(self, grikkland, greek_civ):
        # Daily Life
        CulturalTopic.objects.get_or_create(
            title='Greek City-States',
            title_is='Grísk borgríki',
            category='daily_life',
            civilization=greek_civ,
            period=grikkland,
            content='The ancient Greek world was divided into independent city-states (polis) that included a city and its surrounding countryside.',
            content_is='Gríski heimurinn til forna var skiptur í sjálfstæð borgríki (polis) sem samanstóðu af borg og nærliggjandi sveitum. Hver borg hafði sína eigin stjórn, lög og siði. Mikilvægustu borgríkin voru Aþena, Sparta, Kórinþa, Þeba og Sýrakúsa.'
        )
        
        # Social Classes
        CulturalTopic.objects.get_or_create(
            title='Athenian Democracy',
            title_is='Lýðræði Aþenu',
            category='social_classes',
            civilization=greek_civ,
            period=grikkland,
            content='Athenian democracy was established in 508-507 BCE and was a direct democracy, where citizens voted directly on legislation and executive bills.',
            content_is='Lýðræði Aþenu var stofnað 508-507 f.Kr. og var beint lýðræði, þar sem borgarar greiddu atkvæði beint um löggjöf og framkvæmdavald. Þó voru aðeins frjálsir karlmenn með borgararétt, sem útilokaði konur, útlendinga og þræla. Þrátt fyrir þessar takmarkanir var lýðræði Aþenu mikilvægt skref í þróun lýðræðislegra stjórnarhátta.'
        )
        
        # Art & Architecture
        CulturalTopic.objects.get_or_create(
            title='Greek Architecture',
            title_is='Grísk byggingarlist',
            category='art',
            civilization=greek_civ,
            period=grikkland,
            content='Greek architecture is known for its temples, characterized by columnar designs and horizontal structures.',
            content_is='Grísk byggingarlist er þekkt fyrir musteri sín, sem einkennast af súlnahönnun og láréttum byggingum. Þrjár helstu súlnagerðirnar voru dórískar, jónískar og kórinþískar. Parþenon á Akrópólishæð í Aþenu er eitt frægasta dæmið um gríska byggingarlist.'
        )
        
        # Literature
        CulturalTopic.objects.get_or_create(
            title='Greek Drama',
            title_is='Grískt leikrit',
            category='literature',
            civilization=greek_civ,
            period=grikkland,
            content='Greek drama consisted of tragedy, comedy, and the satyr play.',
            content_is='Grískt leikrit samanstóð af harmleik, gamanleik og satýrleik. Harmleikir fjölluðu um hetjur og guði og enduðu oft með harmrænum hætti. Gamanleikir voru oft pólitískir og gagnrýndu samfélagið. Helstu leikskáld voru Aiskýlos, Sófókles og Evripídes í harmleik og Aristófanes í gamanleik.'
        )
    
    def create_quiz(self, grikkland):
        # Create a quiz about Ancient Greece
        quiz, created = Quiz.objects.get_or_create(
            title='Ancient Greece Quiz',
            title_is='Próf um Grikkland hið forna',
            description='Test your knowledge about Ancient Greece.',
            description_is='Prófaðu þekkingu þína á Grikklandi hinu forna.',
            quiz_type='period',
            period=grikkland,
            difficulty=3,
            is_published=True
        )
        
        if created:
            # Create questions for the quiz
            questions = [
                {
                    'question': 'Who was the king of the Greek gods?',
                    'question_is': 'Hver var konungur grísku guðanna?',
                    'type': 'multiple_choice',
                    'options': '["Zeus", "Poseidon", "Apollo", "Hades"]',
                    'correct': '0',
                    'explanation': 'Zeus was the king of the Greek gods and the god of the sky, lightning, thunder, law, order, and justice.',
                    'explanation_is': 'Seifur var konungur grísku guðanna og guð himins, eldinga, þrumu, laga, reglu og réttlætis.'
                },
                {
                    'question': 'Which city-state is known for its military prowess and strict society?',
                    'question_is': 'Hvaða borgríki er þekkt fyrir hernaðarmátt sinn og strangt samfélag?',
                    'type': 'multiple_choice',
                    'options': '["Athens", "Corinth", "Sparta", "Thebes"]',
                    'correct': '2',
                    'explanation': 'Sparta was known for its military prowess and strict society.',
                    'explanation_is': 'Sparta var þekkt fyrir hernaðarmátt sinn og strangt samfélag.'
                },
                {
                    'question': 'Who was the Athenian statesman who led Athens during its Golden Age?',
                    'question_is': 'Hver var aþenski stjórnmálamaðurinn sem leiddi Aþenu á gullöld sinni?',
                    'type': 'multiple_choice',
                    'options': '["Solon", "Pericles", "Themistocles", "Cleisthenes"]',
                    'correct': '1',
                    'explanation': 'Pericles was the Athenian statesman who led Athens during its Golden Age.',
                    'explanation_is': 'Períkles var aþenski stjórnmálamaðurinn sem leiddi Aþenu á gullöld sinni.'
                },
                {
                    'question': 'The Battle of Marathon was fought between the Athenians and which empire?',
                    'question_is': 'Orrusta við Maraþon var háð milli Aþeninga og hvaða heimsveldis?',
                    'type': 'multiple_choice',
                    'options': '["Roman Empire", "Persian Empire", "Egyptian Empire", "Macedonian Empire"]',
                    'correct': '1',
                    'explanation': 'The Battle of Marathon was fought between the Athenians and the Persian Empire in 490 BCE.',
                    'explanation_is': 'Orrusta við Maraþon var háð milli Aþeninga og Persneska heimsveldisins árið 490 f.Kr.'
                },
                {
                    'question': 'Which philosopher was the teacher of Alexander the Great?',
                    'question_is': 'Hvaða heimspekingur var kennari Alexanders mikla?',
                    'type': 'multiple_choice',
                    'options': '["Socrates", "Plato", "Aristotle", "Diogenes"]',
                    'correct': '2',
                    'explanation': 'Aristotle was the teacher of Alexander the Great.',
                    'explanation_is': 'Aristóteles var kennari Alexanders mikla.'
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