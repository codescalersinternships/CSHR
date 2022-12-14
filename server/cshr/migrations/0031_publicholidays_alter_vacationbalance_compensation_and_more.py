# Generated by Django 4.0.7 on 2022-09-11 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0030_delete_vacationbalancevalues_vacationbalance_date_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="PublicHolidays",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name="vacationbalance",
            name="compensation",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="vacationbalance",
            name="emergencies",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="vacationbalance",
            name="leave_execuses",
            field=models.IntegerField(),
        ),
        migrations.RemoveField(
            model_name="vacationbalance",
            name="public_holidays",
        ),
        migrations.AlterField(
            model_name="vacationbalance",
            name="sick_leaves",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="vacationbalance",
            name="unpaid",
            field=models.IntegerField(),
        ),
        migrations.AddField(
            model_name="vacationbalance",
            name="public_holidays",
            field=models.ManyToManyField(to="cshr.publicholidays"),
        ),
    ]
