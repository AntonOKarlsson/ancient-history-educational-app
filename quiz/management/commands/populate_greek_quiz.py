import os
import django
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import HistoricalPeriod
from quiz.models import Quiz, Question
import json
import re

class Command(BaseCommand):
    help = 'Populates the database with 60 Greek quiz questions'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database with Greek quiz questions...')
        
        # Get the Greek period
        try:
            grikkland = HistoricalPeriod.objects.get(name_is='Grikkland')
        except HistoricalPeriod.DoesNotExist:
            self.stdout.write(self.style.ERROR('Greek historical period not found. Run populate_periods command first.'))
            return
        
        # Create a quiz for Greek questions
        quiz, created = Quiz.objects.get_or_create(
            title='Greek History Quiz',
            title_is='Próf um sögu Grikklands',
            description='Test your knowledge about Ancient Greek history with these 60 questions.',
            description_is='Prófaðu þekkingu þína á sögu Grikklands hins forna með þessum 60 spurningum.',
            quiz_type='period',
            period=grikkland,
            difficulty=3,
            is_published=True
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created quiz: {quiz.title_is}'))
        else:
            self.stdout.write(f'Using existing quiz: {quiz.title_is}')
            
            # Check if questions already exist
            if Question.objects.filter(quiz=quiz).exists():
                self.stdout.write('Questions already exist for this quiz. Skipping...')
                return
        
        # Parse and create questions
        questions_data = self.parse_questions()
        
        # Create questions in the database
        for q_data in questions_data:
            options = [q_data['a'], q_data['b'], q_data['c'], q_data['d']]
            
            # Find the correct answer index (0-based)
            correct_index = None
            for i, option in enumerate(['a', 'b', 'c', 'd']):
                if q_data[option + '_correct']:
                    correct_index = i
                    break
            
            if correct_index is None:
                self.stdout.write(self.style.WARNING(f"No correct answer found for question: {q_data['question']}"))
                continue
            
            # Create the question
            question = Question.objects.create(
                quiz=quiz,
                question_text=q_data['question'],
                question_text_is=q_data['question'],  # Same text as it's already in Icelandic
                question_type='multiple_choice',
                options=json.dumps(options),
                correct_answer=str(correct_index),
                difficulty=3,
                points=1
            )
            
            self.stdout.write(f"Created question: {question.question_text_is[:50]}...")
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(questions_data)} questions'))
    
    def parse_questions(self):
        """Parse the questions from the predefined text"""
        questions = []
        
        # This is the raw text of questions from the issue description
        raw_questions = """
Hvenær hófst blómatími mínóskrar menningar á Krít?
a) 3000 f.Kr.
b) 2500 f.Kr.
c) 2000 f.Kr. ✓
d) 1500 f.Kr.
Hvað voru "hinar myrku aldir" í sögu Grikklands?
a) 1500-1200 f.Kr.
b) 1200-900 f.Kr.
c) 1100-800 f.Kr. ✓
d) 900-600 f.Kr.
Hvað kallast tímabilið eftir Alexander mikla?
a) Klassíska öldin
b) Hellenismi ✓
c) Rómverska tímabilið
d) Mýkenska tímabilið
Hver var kallaður "faðir heimspekinnar"?
a) Sókrates
b) Platón
c) Þales ✓
d) Aristóteles
Hvað þýðir orðið "filosofía"?
a) Ást á guði
b) Ást á visku ✓
c) Ást á sannleika
d) Ást á náttúru
Hver stofnaði skólann Akademía?
a) Sókrates
b) Platón ✓
c) Aristóteles
d) Þales
Hver taldi grunneindir alls vera tölur og talnakerfi?
a) Þales
b) Pýþagóras ✓
c) Demókrítos
d) Herakleitos
Hver setti fram atómkenninguna?
a) Empedókles
b) Anaxímenes
c) Demókrítos ✓
d) Pýþagóras
Í hvaða orrstu sigruðu Aþeningar Persa 490 f.Kr.?
a) Salamis
b) Maraþon ✓
c) Plateau
d) Laugarskarð
Hvað stóð Trójustríðið lengi samkvæmt goðsögnum?
a) 7 ár
b) 10 ár ✓
c) 12 ár
d) 15 ár
Hvað stóð Pelópsskagastríðið lengi?
a) 20 ár
b) 25 ár
c) 27 ár ✓
d) 30 ár
Hver sigraði í Pelópsskagastríðinu?
a) Aþeningar
b) Spartverjar ✓
c) Þebverjar
d) Korinþumenn
Hver var kallaður "faðir aþenska lýðræðisins"?
a) Sólon
b) Peisístratos
c) Kleisþenes ✓
d) Períkles
Hvað þýðir "leirtaflnadómur"?
a) Dómur um eignir
b) Refsing fyrir glæpi
c) Útlegð í 10 ár ✓
d) Kosningar til embætta
Í hvað skipti Sólon aþenskum borgurum?
a) Þrjár stéttir
b) Fjórar stéttir ✓
c) Fimm stéttir
d) Sex stéttir
Hver var æðstur Ólympsguða?
a) Apollon
b) Póseidon
c) Seifur ✓
d) Hades
Hver var gyðja visku?
a) Hera
b) Aþena ✓
c) Artemis
d) Afródíta
Hvað eru einkennistákn Seifs?
a) Harpa og bogi
b) Þríforkur og hestur
c) Elding og örn ✓
d) Ugla og vopn
Hver drap Mínótáros?
a) Herakles
b) Þeseifur ✓
c) Jason
d) Akkilles
Hver var frægasti grískur skáld?
a) Pindar
b) Hómer ✓
c) Saffo
d) Aiskýlos
Hvað heitir höll guðanna?
a) Parþenon
b) Akrópólis
c) Ólympus ✓
d) Delfí
Hver fann hallarborg Knossos?
a) Heinrich Schliemann
b) Arthur Evans ✓
c) Howard Carter
d) Wilhelm Dörpfeld
Hver var kallaður "faðir læknisfræðinnar"?
a) Asklepíos
b) Hippókrates ✓
c) Galenus
d) Heródótos
Hver skrifaði "Elementa" um stærðfræði?
a) Pýþagóras
b) Arkímedes
c) Evklíð ✓
d) Þales
Hver fann upp Arkímedesarskrúfuna?
a) Evklíð
b) Arkímedes ✓
c) Herófílos
d) Eratosþenes
Hvað hét höfnin í Aþenu?
a) Korinþa
b) Píreus ✓
c) Megara
d) Elevsis
Á hvaða eyju var Mínósk menning?
a) Sikiley
b) Kýpur
c) Krít ✓
d) Ródos
Hvað hét spásagnastaður Apollons?
a) Ólympía
b) Delfí ✓
c) Dodóna
d) Elevsis
Hvað þýðir "pólís"?
a) Höfnarbær
b) Borgríki ✓
c) Markaðstorg
d) Hofbygging
Hvað þýðir "týrann" í grískum skilningi?
a) Grimur konungur
b) Einvaldur ✓
c) Hershöfðingi
d) Prestkonungur
Hvað hét völundarhúsið þar sem Mínótáros dvaldi?
a) Labýrintus ✓
b) Knossos
c) Palladion
d) Tartaros
Hver hjálpaði Þeseifi að rata út úr völundarhúsinu?
a) Medea
b) Aríaðna ✓
c) Helena
d) Kassandra
Hvað heitir fljótið í undirheimum?
a) Lethe
b) Acheron
c) Styx ✓
d) Cocytus
Hver var móðir Akkillesar?
a) Hera
b) Þetis ✓
c) Afródíta
d) Aþena
Hvað varð Akkilles óvörður fyrir?
a) Sár í hælinn ✓
b) Eitur
c) Elding
d) Drukknun
Hver var konungur Spörtu þegar París rænti Helenu?
a) Agamemnon
b) Menelás ✓
c) Príamos
d) Hektor
Hvað hét höfuðborg Trójumanna?
a) Mýkenu
b) Tíryns
c) Trója ✓
d) Ilíon
Hver leiddi Grikki í Trójustríðinu?
a) Menelás
b) Agamemnon ✓
c) Akkilles
d) Odysseifur
Hvað gerðu Grikkir til að komast inn í Tróju?
a) Umkringdu borgina
b) Smíðuðu tunnla
c) Byggu tréhest ✓
d) Notuðu skálaber
Hvað tók Odysseif langan tíma að komast heim?
a) 5 ár
b) 7 ár
c) 10 ár ✓
d) 12 ár
Hvað hét kona Odysseifs?
a) Helena
b) Penelópa ✓
c) Kassandra
d) Andrómacha
Hvað gerði Penelópa til að forðast vonbiðla?
a) Faldi sig
b) Rakti upp vef á nóttunni ✓
c) Flúði úr landi
d) Bað guðina um hjálp
Hvað voru völundarsmiðurinn Daidalos og sonur hans Íkaros að reyna?
a) Fljúga frá Krít ✓
b) Komast í undirheima
c) Finna gullið
d) Byggja skip
Hvað varð um Íkaros?
a) Komst undan
b) Var tekinn af Persum
c) Hrapaði til sjávar ✓
d) Varð að fugli
Hver var faðir Jason sem sótti gullna reyfið?
a) Eeson ✓
b) Pelías
c) Aetes
d) Orfeifu
Hvað hét skipið sem Jason sigldi?
a) Argo ✓
b) Odyssey
c) Triton
d) Pegasus
Hvað áttu Argónaútarnir að sækja?
a) Gullna epli
b) Gullna reyfið ✓
c) Gullna krúnu
d) Gullhring
Hver stofnaði deleyska sjóborgasambandið?
a) Spartverjar
b) Aþeningar ✓
c) Þebverjar
d) Korinþumenn
Á hvaða eyju var miðstöð sjóborgasambandsins í upphafi?
a) Krít
b) Ródos
c) Delos ✓
d) Samos
Hvað var tilgangur sjóborgasambandsins í upphafi?
a) Ráðast á Spörtu
b) Berjast gegn Persum ✓
c) Ná tökum á verslun
d) Verja sig gegn sjóræningjum
Hvað hét samtök Spartverja?
a) Deleyska sambandið
b) Aþenska sambandið
c) Pelópsskagabandalagið ✓
d) Þebverska sambandið
Hvað olli drepsótt í Aþenu á fyrstu árum Pelópsskagastríðs?
a) Skortur á mat
b) Óhreinindi vegna múgaðar ✓
c) Eitur í vatni
d) Kuldaveður
Hvað urðu íbúar Spörtu sem voru ekki Spartverjar kallaðir?
a) Þrælar
b) Helótar og hringbyggjar ✓
c) Perioikar
d) Metoekar
Í hvað skiptust Spartverjar þegar þeir börðust?
a) Falanx ✓
b) Turtur
c) Lín
d) Hringa
Hvað var sérstakt við uppeldi drengja í Spörtu?
a) Lærðu að lesa snemma
b) Sendir í herbúðir 7 ára ✓
c) Dvöldu heima til 18 ára
d) Lærðu handiðn
Hver var "faðir sögunnar"?
a) Þúkydídes
b) Heródótos ✓
c) Xenófón
d) Hómer
Um hvað skrifaði Þúkydídes aðallega?
a) Persastríðin
b) Pelópsskagastríðið ✓
c) Trójustríðið
d) Makedónsku landvinningarnar
Hvað skrifaði Xenófón um för 10 þúsund Grikkja?
a) Ilíad
b) Odyssey
c) Anabasis ✓
d) Historíur
Hvað var helsta framlag Fönikíumanna til menningar?
a) Siglingar
b) Stafrófið ✓
c) Stjörnufræði
d) Landbúnað
Frá hvaða orðum kemur "alfabet"?
a) Alpha og beta ✓
b) Aleph og beth
c) Aleppo og Beirut
d) Alf og bet
        """
        
        # Process the raw text to extract questions
        current_question = None
        current_options = {}
        
        for line in raw_questions.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Check if this is a question line (doesn't start with a letter followed by a closing parenthesis)
            if not re.match(r'^[a-d]\)', line):
                # If we have a complete question, add it to our list
                if current_question and current_options:
                    questions.append({
                        'question': current_question,
                        'a': current_options.get('a', ''),
                        'b': current_options.get('b', ''),
                        'c': current_options.get('c', ''),
                        'd': current_options.get('d', ''),
                        'a_correct': current_options.get('a_correct', False),
                        'b_correct': current_options.get('b_correct', False),
                        'c_correct': current_options.get('c_correct', False),
                        'd_correct': current_options.get('d_correct', False),
                    })
                
                # Start a new question
                current_question = line
                current_options = {}
            else:
                # This is an option line
                option_match = re.match(r'^([a-d])\) (.+?)( ✓)?$', line)
                if option_match:
                    option_letter = option_match.group(1)
                    option_text = option_match.group(2)
                    is_correct = bool(option_match.group(3))
                    
                    current_options[option_letter] = option_text
                    current_options[f'{option_letter}_correct'] = is_correct
        
        # Add the last question if there is one
        if current_question and current_options:
            questions.append({
                'question': current_question,
                'a': current_options.get('a', ''),
                'b': current_options.get('b', ''),
                'c': current_options.get('c', ''),
                'd': current_options.get('d', ''),
                'a_correct': current_options.get('a_correct', False),
                'b_correct': current_options.get('b_correct', False),
                'c_correct': current_options.get('c_correct', False),
                'd_correct': current_options.get('d_correct', False),
            })
        
        return questions