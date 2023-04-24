# Generated by Django 4.2 on 2023-04-12 01:59

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("actionnetwork", "0004_alter_campaign_api_response_json"),
    ]

    operations = [
        migrations.CreateModel(
            name="Donation",
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
                    "api_response_json",
                    models.JSONField(verbose_name="API Response JSON"),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Amount"
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        default=datetime.datetime(
                            2023, 4, 12, 1, 59, 49, 788685, tzinfo=datetime.timezone.utc
                        ),
                        verbose_name="Created date",
                    ),
                ),
                (
                    "campaign",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="actionnetwork.campaign",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="actionnetwork.person",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
