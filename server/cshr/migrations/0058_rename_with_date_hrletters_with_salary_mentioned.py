# Generated by Django 4.1.2 on 2022-10-23 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0057_alter_hrletters_date"),
    ]

    operations = [
        migrations.RenameField(
            model_name="hrletters",
            old_name="with_date",
            new_name="with_salary_mentioned",
        ),
    ]
