# Generated by Django 4.1 on 2022-08-29 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0011_user_is_active_user_is_admin_user_is_staff_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="cshr.office"
            ),
        ),
    ]
