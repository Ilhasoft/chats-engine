# Generated by Django 4.0.5 on 2022-08-19 17:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import timezone_field.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='Modified on')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('timezone', timezone_field.fields.TimeZoneField(verbose_name='Timezone')),
                ('date_format', models.CharField(choices=[('D', 'DD-MM-YYYY'), ('M', 'MM-DD-YYYY')], default='D', help_text='Whether day comes first or month comes first in dates', max_length=1, verbose_name='Date Format')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='ProjectPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='Modified on')),
                ('role', models.PositiveIntegerField(choices=[(0, 'not set'), (1, 'user'), (2, 'admin'), (3, 'external')], default=0, verbose_name='role')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authorizations', to='projects.project', to_field='uuid', verbose_name='Project')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='email', verbose_name='users')),
            ],
            options={
                'verbose_name': 'Project Permission',
                'verbose_name_plural': 'Project Permissions',
            },
        ),
    ]
