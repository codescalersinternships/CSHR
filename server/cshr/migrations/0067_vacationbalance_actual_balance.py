# Generated by Django 4.1.2 on 2022-11-03 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0066_alter_user_skills"),
    ]

    operations = [
        migrations.AddField(
            model_name="vacationbalance",
            name="actual_balance",
            field=models.JSONField(default=dict, null=True),
        ),
    ]
