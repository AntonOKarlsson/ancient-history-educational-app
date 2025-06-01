from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.db import models
from .models import (
    Quiz, Question, QuizAttempt, QuestionResponse, 
    Achievement, UserAchievement
)
from core.models import HistoricalPeriod
import json
import random

def random_history_quiz(request):
    """Take a random 5-question quiz about history (Greek and Middle Ages)"""
    # Find the Greek and Middle Ages quizzes
    history_quizzes = []
    quiz_titles = []

    try:
        greek_quiz = Quiz.objects.get(title_is='Próf um sögu Grikklands')
        history_quizzes.append(greek_quiz)
        quiz_titles.append(greek_quiz.title_is)
    except Quiz.DoesNotExist:
        pass

    try:
        middle_ages_quiz = Quiz.objects.get(title_is='Próf um Miðaldir')
        history_quizzes.append(middle_ages_quiz)
        quiz_titles.append(middle_ages_quiz.title_is)
    except Quiz.DoesNotExist:
        pass

    # If no quizzes found, redirect to the quiz home
    if not history_quizzes:
        return redirect('quiz:quiz_home')

    if request.method == 'POST':
        # Process quiz submission
        # Get the question IDs from the form
        question_ids = request.POST.getlist('question_ids')
        quiz_id = request.POST.get('quiz_id')  # Get the quiz ID from the form

        # Get the quiz that was used
        quiz = Quiz.objects.get(id=quiz_id)

        # Get the questions that were displayed to the user
        questions = [Question.objects.get(id=qid) for qid in question_ids]

        score = 0
        max_score = len(questions)
        results = []

        for question in questions:
            # Get the user's answer for this question
            user_answer = request.POST.get(f'question_{question.id}')

            # Check if the answer is correct
            is_correct = False
            if user_answer and user_answer == question.correct_answer:
                is_correct = True
                score += 1

            # Get the options for display
            options = json.loads(question.options)
            correct_option = options[int(question.correct_answer)]
            user_option = options[int(user_answer)] if user_answer is not None else "No answer"

            # Add to results
            results.append({
                'question': question.question_text_is,
                'user_answer': user_option,
                'correct_answer': correct_option,
                'is_correct': is_correct
            })

        # Calculate percentage
        percentage = (score / max_score) * 100 if max_score > 0 else 0

        # Create context for results
        context = {
            'score': score,
            'max_score': max_score,
            'percentage': percentage,
            'results': results,
            'quiz_title': 'Slembiprófun um sögu'
        }

        # If user is authenticated, save the attempt
        if request.user.is_authenticated:
            attempt = QuizAttempt.objects.create(
                user=request.user,
                quiz=quiz,
                score=score,
                max_score=max_score,
                end_time=timezone.now(),
                completed=True
            )

            # Save individual responses
            for question, result in zip(questions, results):
                QuestionResponse.objects.create(
                    attempt=attempt,
                    question=question,
                    user_answer=request.POST.get(f'question_{question.id}', ''),
                    is_correct=result['is_correct'],
                    points_earned=1 if result['is_correct'] else 0
                )

            # Check for achievements
            check_achievements(request.user)

        return render(request, 'quiz/random_history_quiz_results.html', context)

    # Get all questions from all history quizzes
    all_questions = []
    for quiz in history_quizzes:
        all_questions.extend(list(Question.objects.filter(quiz=quiz)))

    # If there are fewer than 5 questions, use all of them
    if len(all_questions) <= 5:
        questions = all_questions
    else:
        # Randomly select 5 questions
        questions = random.sample(all_questions, 5)

    # Prepare the quiz for display
    context = {
        'quiz_title': 'Slembiprófun um sögu',
        'questions': questions,
        'quiz_id': history_quizzes[0].id if history_quizzes else None  # Use the first quiz's ID
    }

    return render(request, 'quiz/random_history_quiz.html', context)

def quiz_home(request):
    """Quiz section landing page"""
    # Get published quizzes
    period_quizzes = Quiz.objects.filter(is_published=True, quiz_type='period').order_by('-created_at')[:5]
    topic_quizzes = Quiz.objects.filter(is_published=True, quiz_type='topic').order_by('-created_at')[:5]
    comprehensive_quizzes = Quiz.objects.filter(is_published=True, quiz_type='comprehensive').order_by('-created_at')[:5]

    # Get user's recent attempts if logged in
    recent_attempts = None
    if request.user.is_authenticated:
        recent_attempts = QuizAttempt.objects.filter(user=request.user).order_by('-start_time')[:5]

    context = {
        'period_quizzes': period_quizzes,
        'topic_quizzes': topic_quizzes,
        'comprehensive_quizzes': comprehensive_quizzes,
        'recent_attempts': recent_attempts,
    }
    return render(request, 'quiz/quiz_home.html', context)

def quiz_by_period(request):
    """Quizzes organized by historical period"""
    periods = HistoricalPeriod.objects.all().order_by('start_year')

    # Get quizzes for each period
    period_quizzes = {}
    for period in periods:
        period_quizzes[period] = Quiz.objects.filter(is_published=True, period=period)

    context = {
        'periods': periods,
        'period_quizzes': period_quizzes,
    }
    return render(request, 'quiz/quiz_by_period.html', context)

def quiz_by_topic(request):
    """Quizzes organized by topic"""
    # Get unique topics
    topics = Quiz.objects.filter(is_published=True, quiz_type='topic').values_list('topic', flat=True).distinct()

    # Get quizzes for each topic
    topic_quizzes = {}
    for topic in topics:
        topic_quizzes[topic] = Quiz.objects.filter(is_published=True, topic=topic)

    context = {
        'topics': topics,
        'topic_quizzes': topic_quizzes,
    }
    return render(request, 'quiz/quiz_by_topic.html', context)

def comprehensive_quiz(request):
    """Comprehensive review quizzes"""
    quizzes = Quiz.objects.filter(is_published=True, quiz_type='comprehensive').order_by('-created_at')

    context = {
        'quizzes': quizzes,
    }
    return render(request, 'quiz/comprehensive_quiz.html', context)

@login_required
def custom_quiz(request):
    """Create and take custom quizzes"""
    if request.method == 'POST':
        # Process form data to create a custom quiz
        title = request.POST.get('title')
        title_is = request.POST.get('title_is')
        description = request.POST.get('description')
        description_is = request.POST.get('description_is')
        period_id = request.POST.get('period')
        topic = request.POST.get('topic')
        difficulty = request.POST.get('difficulty', 1)
        question_count = int(request.POST.get('question_count', 10))

        # Create the quiz
        quiz = Quiz.objects.create(
            title=title,
            title_is=title_is,
            description=description,
            description_is=description_is,
            quiz_type='custom',
            period_id=period_id if period_id else None,
            topic=topic,
            difficulty=difficulty,
            is_published=True,
        )

        # Add questions to the quiz based on filters
        questions_pool = Question.objects.all()
        if period_id:
            questions_pool = questions_pool.filter(quiz__period_id=period_id)
        if topic:
            questions_pool = questions_pool.filter(quiz__topic=topic)
        if difficulty:
            questions_pool = questions_pool.filter(difficulty=difficulty)

        # Randomly select questions
        selected_questions = list(questions_pool)
        if len(selected_questions) > question_count:
            selected_questions = random.sample(selected_questions, question_count)

        # Add questions to the quiz
        for question in selected_questions:
            new_question = Question.objects.create(
                quiz=quiz,
                question_text=question.question_text,
                question_text_is=question.question_text_is,
                question_type=question.question_type,
                image=question.image,
                options=question.options,
                correct_answer=question.correct_answer,
                explanation=question.explanation,
                explanation_is=question.explanation_is,
                difficulty=question.difficulty,
                points=question.points,
            )

        return redirect('quiz:take_quiz', quiz_id=quiz.id)

    # Display form to create custom quiz
    periods = HistoricalPeriod.objects.all().order_by('start_year')
    topics = Quiz.objects.filter(is_published=True).values_list('topic', flat=True).distinct()

    context = {
        'periods': periods,
        'topics': topics,
    }
    return render(request, 'quiz/custom_quiz.html', context)

@login_required
def take_quiz(request, quiz_id):
    """Take a quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_published=True)

    if request.method == 'POST':
        # Process quiz submission
        data = json.loads(request.body)
        answers = data.get('answers', {})

        # Create quiz attempt
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            max_score=sum(q.points for q in quiz.questions.all()),
            end_time=timezone.now(),
            completed=True,
        )

        # Process each answer
        score = 0
        for question_id, answer in answers.items():
            question = get_object_or_404(Question, id=question_id)
            is_correct = False

            # Check if answer is correct based on question type
            if question.question_type == 'multiple_choice' or question.question_type == 'true_false':
                is_correct = answer == question.correct_answer
            elif question.question_type == 'fill_blank':
                is_correct = answer.lower().strip() == question.correct_answer.lower().strip()
            elif question.question_type == 'timeline_order':
                is_correct = answer == question.correct_answer
            elif question.question_type == 'map_identification':
                # For map identification, check if coordinates are within acceptable range
                correct_coords = json.loads(question.correct_answer)
                answer_coords = json.loads(answer)
                is_correct = (
                    abs(float(answer_coords['lat']) - float(correct_coords['lat'])) < 5 and
                    abs(float(answer_coords['lng']) - float(correct_coords['lng'])) < 5
                )
            elif question.question_type == 'image_recognition':
                is_correct = answer == question.correct_answer

            # Calculate points earned
            points_earned = question.points if is_correct else 0
            score += points_earned

            # Save response
            QuestionResponse.objects.create(
                attempt=attempt,
                question=question,
                user_answer=answer,
                is_correct=is_correct,
                points_earned=points_earned,
            )

        # Update attempt score
        attempt.score = score
        attempt.save()

        # Check for achievements
        check_achievements(request.user)

        return JsonResponse({'success': True, 'attempt_id': attempt.id})

    # Display quiz
    questions = quiz.questions.all()

    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'quiz/take_quiz.html', context)

def quiz_result(request, attempt_id):
    """View quiz results"""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)

    # Check if user is authorized to view this attempt
    if request.user != attempt.user and not request.user.is_staff:
        return redirect('quiz:quiz_home')

    # Get responses
    responses = attempt.responses.all().select_related('question')

    context = {
        'attempt': attempt,
        'responses': responses,
    }
    return render(request, 'quiz/quiz_result.html', context)

@login_required
def progress(request):
    """View user's progress"""
    # Get user's quiz attempts
    attempts = QuizAttempt.objects.filter(user=request.user).order_by('-start_time')

    # Calculate statistics
    total_attempts = attempts.count()
    completed_attempts = attempts.filter(completed=True).count()
    total_score = sum(a.score for a in attempts)
    max_score = sum(a.max_score for a in attempts)
    average_percentage = (total_score / max_score * 100) if max_score > 0 else 0

    # Get attempts by period
    periods = HistoricalPeriod.objects.all()
    period_stats = {}
    for period in periods:
        period_attempts = attempts.filter(quiz__period=period, completed=True)
        if period_attempts.exists():
            period_score = sum(a.score for a in period_attempts)
            period_max = sum(a.max_score for a in period_attempts)
            period_percentage = (period_score / period_max * 100) if period_max > 0 else 0
            period_stats[period] = {
                'attempts': period_attempts.count(),
                'percentage': period_percentage,
            }

    # Get achievements
    achievements = request.user.achievements.all().select_related('achievement')

    context = {
        'attempts': attempts,
        'total_attempts': total_attempts,
        'completed_attempts': completed_attempts,
        'average_percentage': average_percentage,
        'period_stats': period_stats,
        'achievements': achievements,
    }
    return render(request, 'quiz/progress.html', context)

def leaderboard(request):
    """View leaderboard"""
    # Get top users by quiz score
    users_with_attempts = QuizAttempt.objects.values('user').distinct()

    leaderboard_data = []
    for user_dict in users_with_attempts:
        user_id = user_dict['user']
        user_attempts = QuizAttempt.objects.filter(user_id=user_id, completed=True)
        total_score = sum(a.score for a in user_attempts)
        max_score = sum(a.max_score for a in user_attempts)
        percentage = (total_score / max_score * 100) if max_score > 0 else 0

        leaderboard_data.append({
            'user_id': user_id,
            'username': user_attempts.first().user.username,
            'attempts': user_attempts.count(),
            'score': total_score,
            'percentage': percentage,
            'achievements': UserAchievement.objects.filter(user_id=user_id).count(),
        })

    # Sort by percentage
    leaderboard_data.sort(key=lambda x: x['percentage'], reverse=True)

    context = {
        'leaderboard': leaderboard_data[:20],  # Top 20 users
    }
    return render(request, 'quiz/leaderboard.html', context)

def check_achievements(user):
    """Check and award achievements based on user's progress"""
    # Get all achievements
    achievements = Achievement.objects.all()

    # Get user's attempts
    attempts = QuizAttempt.objects.filter(user=user, completed=True)

    # Check each achievement
    for achievement in achievements:
        # Skip if user already has this achievement
        if UserAchievement.objects.filter(user=user, achievement=achievement).exists():
            continue

        # Example achievement checks (would be more sophisticated in production)
        if achievement.title == "First Quiz":
            if attempts.count() >= 1:
                UserAchievement.objects.create(user=user, achievement=achievement)

        elif achievement.title == "Perfect Score":
            if attempts.filter(score=models.F('max_score')).exists():
                UserAchievement.objects.create(user=user, achievement=achievement)

        elif achievement.title == "History Buff":
            if attempts.count() >= 10:
                UserAchievement.objects.create(user=user, achievement=achievement)

        # Add more achievement checks as needed
