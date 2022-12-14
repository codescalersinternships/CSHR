# Generated by Django 4.1 on 2022-08-11 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Office",
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
                ("name", models.CharField(max_length=45)),
                ("country", models.CharField(max_length=45)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserSkills",
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
                ("Name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(db_index=True)),
                ("FirstName", models.CharField(max_length=45)),
                ("LastName", models.CharField(max_length=45)),
                ("Email", models.EmailField(max_length=45)),
                (
                    "MobileNumber",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "TelegramLink",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("Birthday", models.DateField()),
                (
                    "Team",
                    models.CharField(
                        choices=[
                            ("Development", "Dev"),
                            ("Quality assurance", "Qa"),
                            ("Operations", "Ops"),
                            ("Marketing", "Marketing"),
                            ("Management", "Management"),
                            ("Accounting", "Accounting"),
                        ],
                        max_length=20,
                    ),
                ),
                ("Salary", models.JSONField(default=list)),
                (
                    "User_type",
                    models.CharField(
                        choices=[
                            ("Admin", "admin"),
                            ("User", "user"),
                            ("Supervisor", "supervisor"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "Location_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cshr.office"
                    ),
                ),
                (
                    "UserSkills_ids",
                    models.ManyToManyField(related_name="skills", to="cshr.userskills"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
