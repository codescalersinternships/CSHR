# Generated by Django 4.0.7 on 2022-09-08 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0029_vacationbalancevalues"),
    ]

    operations = [
        migrations.DeleteModel(
            name="VacationBalanceValues",
        ),
        migrations.AddField(
            model_name="vacationbalance",
            name="date",
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name="vacationbalance",
            name="old_balance",
            field=models.JSONField(default=dict, null=True),
        ),
    ]