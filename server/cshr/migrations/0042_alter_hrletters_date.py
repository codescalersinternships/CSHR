# Generated by Django 4.0.7 on 2022-09-18 09:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0041_merge_20220918_0946"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hrletters",
            name="date",
            field=models.DateField(default=datetime.date(2022, 9, 18)),
        ),
    ]
