# Generated by Django 5.2 on 2025-06-01 16:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimelineEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('title_is', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('description_is', models.TextField()),
                ('date_start', models.IntegerField()),
                ('date_end', models.IntegerField(blank=True, null=True)),
                ('region', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('political', 'Political'), ('military', 'Military'), ('cultural', 'Cultural'), ('religious', 'Religious'), ('scientific', 'Scientific'), ('economic', 'Economic'), ('other', 'Other')], max_length=20)),
                ('importance', models.IntegerField(default=1)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='events/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('civilization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='core.civilization')),
                ('period', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='core.historicalperiod')),
            ],
            options={
                'ordering': ['date_start', 'importance'],
            },
        ),
        migrations.CreateModel(
            name='TimelineRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation_type', models.CharField(choices=[('cause', 'Cause'), ('effect', 'Effect'), ('related', 'Related'), ('concurrent', 'Concurrent')], max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
                ('description_is', models.TextField(blank=True, null=True)),
                ('from_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations_from', to='timeline.timelineevent')),
                ('to_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations_to', to='timeline.timelineevent')),
            ],
            options={
                'unique_together': {('from_event', 'to_event', 'relation_type')},
            },
        ),
    ]
