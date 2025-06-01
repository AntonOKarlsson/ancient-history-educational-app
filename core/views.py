from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from timeline.models import TimelineEvent
from reference.models import Person, Deity
from quiz.models import Quiz, QuizAttempt

def home(request):
    """Home/Dashboard view with recent activities and featured content"""
    # Get featured content
    featured_events = TimelineEvent.objects.filter(importance__gte=4).order_by('?')[:3]
    featured_people = Person.objects.order_by('?')[:3]
    featured_deities = Deity.objects.order_by('?')[:3]

    # Get recent quizzes
    recent_quizzes = Quiz.objects.filter(is_published=True).order_by('-created_at')[:5]

    # Get user progress if logged in
    user_progress = None
    recent_attempts = None
    if request.user.is_authenticated:
        recent_attempts = QuizAttempt.objects.filter(user=request.user).order_by('-start_time')[:5]
        # Calculate overall progress (could be more sophisticated)
        total_quizzes = Quiz.objects.filter(is_published=True).count()
        completed_quizzes = QuizAttempt.objects.filter(user=request.user, completed=True).values('quiz').distinct().count()
        if total_quizzes > 0:
            user_progress = (completed_quizzes / total_quizzes) * 100
        else:
            user_progress = 0

    context = {
        'featured_events': featured_events,
        'featured_people': featured_people,
        'featured_deities': featured_deities,
        'recent_quizzes': recent_quizzes,
        'recent_attempts': recent_attempts,
        'user_progress': user_progress,
    }

    return render(request, 'core/home.html', context)

def about(request):
    """About page with information about the application"""
    return render(request, 'core/about.html')

@login_required
def profile(request):
    """User profile page"""
    # Get user's quiz attempts
    quiz_attempts = QuizAttempt.objects.filter(user=request.user).order_by('-start_time')

    # Get user's achievements
    achievements = request.user.achievements.all()

    # Get user's favorites
    favorites = request.user.favorites.all()

    context = {
        'quiz_attempts': quiz_attempts,
        'achievements': achievements,
        'favorites': favorites,
    }

    return render(request, 'core/profile.html', context)

def search(request):
    """Global search functionality"""
    query = request.GET.get('q', '')
    results = {}

    if query:
        # Search in timeline events
        results['events'] = TimelineEvent.objects.filter(title_is__icontains=query)[:10]

        # Search in people
        results['people'] = Person.objects.filter(name_is__icontains=query)[:10]

        # Search in deities
        results['deities'] = Deity.objects.filter(name_is__icontains=query)[:10]

        # Add more search categories as needed

    context = {
        'query': query,
        'results': results,
    }

    return render(request, 'core/search_results.html', context)
