# Generated by Django 5.2 on 2025-06-01 16:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('title_is', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('description_is', models.TextField()),
                ('icon', models.ImageField(upload_to='achievements/')),
                ('requirement', models.TextField()),
                ('requirement_is', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('title_is', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('description_is', models.TextField()),
                ('quiz_type', models.CharField(choices=[('period', 'By Period'), ('topic', 'By Topic'), ('comprehensive', 'Comprehensive'), ('custom', 'Custom')], max_length=20)),
                ('topic', models.CharField(blank=True, max_length=50)),
                ('difficulty', models.IntegerField(default=1)),
                ('time_limit', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=False)),
                ('period', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quizzes', to='core.historicalperiod')),
            ],
            options={
                'verbose_name_plural': 'Quizzes',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('question_text_is', models.TextField()),
                ('question_type', models.CharField(choices=[('multiple_choice', 'Multiple Choice'), ('true_false', 'True/False'), ('fill_blank', 'Fill in the Blank'), ('timeline_order', 'Timeline Ordering'), ('map_identification', 'Map Identification'), ('image_recognition', 'Image Recognition')], max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='quiz_questions/')),
                ('options', models.TextField(blank=True)),
                ('correct_answer', models.TextField()),
                ('explanation', models.TextField(blank=True)),
                ('explanation_is', models.TextField(blank=True)),
                ('difficulty', models.IntegerField(default=1)),
                ('points', models.IntegerField(default=1)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='QuizAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('max_score', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='quiz.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_attempts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_answer', models.TextField()),
                ('is_correct', models.BooleanField(default=False)),
                ('points_earned', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='quiz.question')),
                ('attempt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='quiz.quizattempt')),
            ],
        ),
        migrations.CreateModel(
            name='UserAchievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_earned', models.DateTimeField(auto_now_add=True)),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='quiz.achievement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievements', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'achievement')},
            },
        ),
    ]
