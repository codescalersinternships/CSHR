# Generated by Django 4.0.1 on 2022-10-24 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0065_offcialdocument_approval_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="skills",
            field=models.ManyToManyField(related_name="skills", to="cshr.UserSkills"),
        ),
    ]
