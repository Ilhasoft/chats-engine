# Generated by Django 4.0.5 on 2022-09-02 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0003_contact_external_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(blank=True, help_text='Contact email', max_length=254, null=True, verbose_name='email'),
        ),
    ]
