# Generated by Django 4.1 on 2022-08-30 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0018_useruserskills_remove_user_userskills_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="UserUserSkills",
            new_name="UserSkills",
        ),
    ]