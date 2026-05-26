# Generated migration for Timetable, ClassSession, and Reminder models

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('indoor_nav', '0003_node_poi_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ics_file_name', models.CharField(default='timetable.ics', max_length=255)),
                ('imported_at', models.DateTimeField(auto_now=True)),
                ('semester', models.CharField(blank=True, max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='timetable', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ClassSession',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('course_code', models.CharField(max_length=50)),
                ('course_name', models.CharField(blank=True, max_length=255)),
                ('session_type', models.CharField(blank=True, max_length=50)),
                ('room_number', models.CharField(max_length=100)),
                ('building', models.CharField(max_length=50)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('estimated_travel_time_minutes', models.IntegerField(blank=True, help_text='Minutes from previous location', null=True)),
                ('reminder_time', models.DateTimeField(blank=True, help_text='When to send reminder (auto-calculated)', null=True)),
                ('timetable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='indoor_nav.timetable')),
            ],
            options={
                'ordering': ['start_time'],
            },
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_dismissed', models.BooleanField(default=False)),
                ('reminder_sent_at', models.DateTimeField(blank=True, null=True)),
                ('user_dismissed_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('class_session', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reminder', to='indoor_nav.classsession')),
            ],
        ),
    ]
