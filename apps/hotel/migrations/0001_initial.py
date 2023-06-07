# Generated by Django 4.2.1 on 2023-06-07 08:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                ("category_code", models.CharField(max_length=3)),
                ("category_name", models.CharField(max_length=50)),
                ("beds", models.IntegerField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("image_url", models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                "ordering": ("-updated", "-created"),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                ("room_number", models.IntegerField()),
                ("is_available", models.BooleanField(default=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="hotel.category"
                    ),
                ),
            ],
            options={
                "ordering": ("-updated", "-created"),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Reservation",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                ("check_in", models.DateTimeField()),
                ("check_out", models.DateTimeField()),
                (
                    "status",
                    models.BooleanField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("FULFILLED", "Fulfilled"),
                            ("CANCELLED", "Cancelled"),
                        ],
                        default="PENDING",
                        max_length=50,
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "room",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="hotel.room"
                    ),
                ),
            ],
            options={
                "ordering": ("-updated", "-created"),
                "abstract": False,
            },
        ),
    ]
