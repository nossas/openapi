# Generated by Django 4.2 on 2023-04-26 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("actionnetwork", "0005_integration"),
    ]

    operations = [
        migrations.CreateModel(
            name="PhonePressure",
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
                ("created_date", models.DateTimeField(verbose_name="data de criação")),
                (
                    "an_response_json",
                    models.JSONField(verbose_name="resposta da action network"),
                ),
                (
                    "campaign",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="actionnetwork.campaign",
                        verbose_name="campanha",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="actionnetwork.person",
                    ),
                ),
                ("targets", models.ManyToManyField(to="actionnetwork.target")),
            ],
            options={
                "verbose_name": "Pressão",
                "verbose_name_plural": "Pressões",
            },
        ),
        migrations.CreateModel(
            name="Call",
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
                (
                    "sid",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="call sid"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("created", "Created"),
                            ("queued", "Queued"),
                            ("initiated", "Initiated"),
                            ("ringing", "Ringing"),
                            ("in-progress", "In Progress"),
                            ("completed", "Completed"),
                        ],
                        max_length=50,
                        verbose_name="call status",
                    ),
                ),
                ("from_number", models.CharField(max_length=25, verbose_name="from")),
                ("to_number", models.CharField(max_length=25, verbose_name="to")),
                (
                    "phone_pressure",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="phone.phonepressure",
                    ),
                ),
            ],
        ),
    ]
