# Generated by Django 4.0.7 on 2022-09-10 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cshr', '0025_event_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('Male', 'male'), ('Female', 'female')], default='Male', max_length=20),
        ),
    ]
