# Generated by Django 4.1 on 2022-08-13 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0003_merge_20220811_1617"),
    ]

    operations = [
        migrations.CreateModel(
            name="Evaluations",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(db_index=True)),
                ("link", models.CharField(max_length=150)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="cshr.user"
                    ),
                ),
            ],
            options={"abstract": False, },
        ),
    ]
