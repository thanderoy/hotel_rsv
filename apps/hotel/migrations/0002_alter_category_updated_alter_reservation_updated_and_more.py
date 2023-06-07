# Generated by Django 4.2.1 on 2023-06-07 08:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("hotel", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="updated",
            field=models.DateTimeField(
                db_index=True, default=django.utils.timezone.now, editable=False
            ),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="updated",
            field=models.DateTimeField(
                db_index=True, default=django.utils.timezone.now, editable=False
            ),
        ),
        migrations.AlterField(
            model_name="room",
            name="updated",
            field=models.DateTimeField(
                db_index=True, default=django.utils.timezone.now, editable=False
            ),
        ),
    ]
