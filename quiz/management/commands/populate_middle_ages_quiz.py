import os
import django
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import HistoricalPeriod
from quiz.models import Quiz, Question
import json
import re

class Command(BaseCommand):
    help = 'Populates the database with Middle Ages quiz questions'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database with Middle Ages quiz questions...')
        
        # Get the Middle Ages period
        try:
            midaldir = HistoricalPeriod.objects.get(name_is='Miðaldir')
        except HistoricalPeriod.DoesNotExist:
            self.stdout.write(self.style.ERROR('Middle Ages historical period not found. Run populate_periods command first.'))
            return
        
        # Create a quiz for Middle Ages questions
        quiz, created = Quiz.objects.get_or_create(
            title='Middle Ages Quiz',
            title_is='Próf um Miðaldir',
            description='Test your knowledge about the Middle Ages with these questions.',
            description_is='Prófaðu þekkingu þína á Miðöldum með þessum spurningum.',
            quiz_type='period',
            period=midaldir,
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
Hvenær eru ármiðaldir taldar hefjast?
a) 395 e.Kr.
b) 476 e.Kr. ✓
c) 500 e.Kr.
d) 622 e.Kr.
Hvað afmarkar lok ármiðalda?
a) Dauði Karls mikla
b) Krýningu Karls mikla til keisara ✓
c) Fall Konstantínópels
d) Víkingaránir
Hvenær hófst Svarti dauði?
a) 1347 ✓
b) 1350
c) 1453
d) 1492
Hvað markar lok miðalda samkvæmt textanum?
a) Fall Konstantínópels 1453
b) Landafundir Kólumbusar 1492 ✓
c) Uppfinning lausaletursins
d) Svarti dauði 1347
Hvađ hét konungur Húna sem réð stórum svæðum Evrópu?
a) Kloðvík
b) Atli ✓
c) Childeric
d) Alarik
Í hvaða orrstu voru Húnar sigraðir 451?
a) Adríanópel
b) Katalónsvöllum ✓
c) Poitiers
d) Hastings
Hver var fyrsti þekkti konungur Mervíkinga?
a) Childeric I
b) Kloðvík ✓
c) Pipin litli
d) Karl mikli
Hvað gerði Kloðvík árið 486?
a) Tók kristna trú
b) Sigraði rómverska keisarann Sýagríus ✓
c) Stofnaði París
d) Gerðist páfi
Hvaða germanska þjóð lagði undir sig Bretland?
a) Vestgotar
b) Austgotar
c) Englar, Saxar og Jótar ✓
d) Langbarðar
Hver setti Childerik III í klaustur 751?
a) Karl mikli
b) Pipin litli ✓
c) Lúðvík
d) Karlóman
Hvenær var Karl mikli krýndur keisari?
a) 768
b) 800 ✓
c) 814
d) 843
Hvað hét enskur munkur sem hjálpaði Karli mikla?
a) Beda
b) Alkvin ✓
c) Ansgar
d) Columba
Hvađ hét biblíuþýðingin sem var endurskoðuð á tíma Karls mikla?
a) Septuaginta
b) Vulgata ✓
c) Itala
d) Peshitta
Í hvað skipti Lúðvík ríkið á milli sona sinna?
a) Tvenna hluta
b) Þrenna hluti ✓
c) Fjóra hluti
d) Fimm hluti
Hver stofnaði Konstantínópel 330?
a) Jústiníanus
b) Konstantín mikli ✓
c) Theódósíus
d) Díóklétíanus
Hvenær var Rómaveldi skipt í tvo hluta?
a) 330
b) 395 ✓
c) 476
d) 527
Hver var frægasti keisari Miklagarðs?
a) Konstantín mikli
b) Jústiníanus ✓
c) Theódósíus
d) Heraklíus
Hvað heitir lagasafn Jústiníanusar?
a) Codex Theodosianus
b) Corpus juris civilis ✓
c) Basilika
d) Ecloga
Hvenær klofnaði kirkjan í tvennt?
a) 1054 ✓
b) 1204
c) 1453
d) 1347
Hvað voru Væringjar?
a) Germansk þjóð
b) Víkingar sem voru málaliðar keisara ✓
c) Kristnir munkir
d) Arabskir kaupmenn
Hvenær fæddist Múhameð spámaður?
a) Um 570 ✓
b) Um 610
c) Um 622
d) Um 630
Hvađ þýðir "hijara"?
a) Heilagt stríð
b) Flótti frá Mekka ✓
c) Pílagrímsferð
d) Bæn
Hvenær lést Múhameð?
a) 622
b) 630 ✓
c) 635
d) 640
Hver var fyrsti kalífinn?
a) Ali
b) Abu-Bakr ✓
c) Umar
d) Uthman
Hvenær lögðu arabar undir sig Spán?
a) 711 ✓
b) 732
c) 661
d) 750
Í hvaða orrstu var arabasókn á Evrópu stöðvuð?
a) Katalónsvöllum
b) Poitiers ✓
c) Tours
d) Roncevaux
Hvađ gerðu Umayyadar ættin?
a) Stofnuðu íslamstrú
b) Gerðu Damaskus að höfuðborg ✓
c) Sigruðu við Poitiers
d) Funnu upp arabískar tölur
Hvađ var Aríusarkristni?
a) Jesús var bæði guðlegur og mannlegur
b) Jesús var maður en ekki sonur guðs ✓
c) Jesús var aðeins guðlegur
d) Jesús var spámaður
Hvađ kölluðust hirðingjar Arabíu?
a) Sarasenir
b) Bedúínar ✓
c) Mamelúkar
d) Janitsarar
Hverjir voru eineðlismenn?
a) Þeir sem trúðu á guðlegt eðli Krists ✓
b) Þeir sem trúðu á mannlegt eðli Krists
c) Þeir sem trúðu á báða hluti
d) Þeir sem trúðu ekki á Krist
Hvađ hét rómverskur sagnaritari sem skrifaði um Germana?
a) Livy
b) Tacitus ✓
c) Suetonius
d) Ammianus
Í hvaða riti lýsti Tacitus germanskum þjóðflokkum?
a) Annales
b) Historiae
c) Germanía ✓
d) Agricola
Hvađ var grundvöllur germanskra þjóðfélaga?
a) Borgríki
b) Ættflokkasamfélag ✓
c) Hirðkerfi
d) Lénsveldið
Hverjir ruplaðu Konstantínópel 1204?
a) Tyrkir
b) Krossfaraher ✓
c) Víkingar
d) Arabar
Hvenær tóku Tyrkir Konstantínópel?
a) 1204
b) 1453 ✓
c) 1492
d) 1347
Hvađ olli Svartadauða?
a) Stríð
b) Plágan ✓
c) Hallæri
d) Jarðskjálfti
Hvađ gerðist eftir Svartadauða?
a) Fleiri dóu
b) Kjör þeirra sem lifðu bötnuðu ✓
c) Stríð brutust út
d) Kirkjan varð valdameiri
Hver fann upp lausaletrið?
a) Jóhann Gutenberg ✓
b) Leonardo da Vinci
c) Galileo Galilei
d) Nicolaus Copernicus
Hvađ hét leturgerðin sem varð til á tíma Karlunga?
a) Rómanskur stafur
b) Gotiskur stafur
c) Lágstafaletur Karlunga ✓
d) Uncial
Hvađ kallast skreytingar í handritum?
a) Kalligrafi
b) Lýsingar ✓
c) Míniatúrur
d) Ornament
Í hvađ voru menntastofnanir Karlunga skiptar?
a) Þríveg og fjórveg ✓
b) Tvíveg og þríveg
c) Fimm greinar
d) Sjö listir
Hvađ var í þrívegnum?
a) Stærðfræði, rúmfræði, stjörnufræði
b) Latína, bókmenntir, rökfræði ✓
c) Tónlist, dans, list
d) Heimspeki, guðfræði, lög
Hvađ tók við af Gregoríönskum messusöng?
a) Gregoríanskur messusöngur er enn notaður ✓
b) Annar messusöngur
c) Orgel
d) Ekkert
Hvađ var helsta verslunarvara Býsanríkisins?
a) Gull
b) Silk ✓
c) Krydd
d) Silfur
Hvađ var mikilvægasta verslunaborgin á Arabíuskaganum?
a) Medína
b) Mekka ✓
c) Baghdad
d) Damaskus
Hvađ hét svarti steinninn í Mekka?
a) Háttvirðingarvörður
b) Helgur dómur ✓
c) Guðssteinn
d) Arabiasteinn
Hvađ hét höfuðstóll arabaveldisins undir Abbasísum?
a) Mekka
b) Damaskus
c) Baghdad ✓
d) Kaíró
Hvađ hét ætt sem gerði Damaskus að höfuðborg?
a) Abbasísar
b) Umayyadar ✓
c) Fátimísar
d) Ayybísar
Hvenær var útþenslutímabili araba lokið?
a) Eftir tapið við Poitiers ✓
b) Eftir dauða Múhameðs
c) Þegar Abbasísar tóku völd
d) Þegar Tyrkir komu til valda
Hvađ skipti máli fyrir langlífi Frankaríkisins?
a) Hernaðargáfa
b) Trúskipti Kloðvíks ✓
c) Auður
d) Stjórnskipan
Hvađ hét hetjukvæðið um Karl mikla?
a) Niebelungenlied
b) Rólandskvæði ✓
c) Song of Roland
d) Karlsmagnúskvæði
Hvađ voru fimm meginstoðir íslam?
a) Trúarjátning, bæn, ölmusa, fasta, pílagrímsferð ✓
b) Trú, von, kærleikur, réttlæti, frið
c) Speki, hugrekki, hófsemi, réttlæti, trú
d) Einn guð, einn spámaður, ein bók, ein kirkja, eitt fólk
Hvađ þótti vera svarti steinninn í Mekka?
a) Málmur
b) Helgur dómur ✓
c) Kristall
d) Guðsgjöf
Hvađ var Quarishættin í Mekka?
a) Þrælahald
b) Sú öflugasta ættin ✓
c) Prestastétt
d) Hersveit
Hvađ gerðist þegar Konstantínópel féll 1453?
a) Kristni varð bannað
b) Sögu Býsanríkisins lauk ✓
c) Rómaveldi var endurreist
d) Nýtt keisaradæmi varð til
Hvađ gerði Pipin litli til að réttlæta að taka völdin?
a) Sigraði í stríði
b) Spurði páfa um hvort rétt væri ✓
c) Erfði frá föður
d) Keypti völdin
Hvađ sá kirkjan um á tíma Mervíkinga?
a) Stjórnmál
b) Félagslega aðstoð ✓
c) Herinn
d) Verslun
Hvađ hét embættismenn Karls mikla?
a) Missi dominici ✓
b) Comes
c) Duces
d) Magistri
Hvađ var hlutverk embættismannanna?
a) Safna sköttum
b) Fylgja eftir stefnu konungs ✓
c) Stjórna héruðum
d) Leiða herinn
Hvađ varð um Karlungaætt í Austfrankaríki?
a) Dó út 918 ✓
b) Missti völd 987
c) Flutti til Ítalíu
d) Sameinaðist öðrum ætt
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
