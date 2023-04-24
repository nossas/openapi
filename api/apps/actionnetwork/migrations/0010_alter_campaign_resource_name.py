# Generated by Django 4.2 on 2023-04-24 19:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("actionnetwork", "0009_alter_campaign_api_response_json"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaign",
            name="resource_name",
            field=models.CharField(
                choices=[
                    ("forms", "Submissions"),
                    ("fundraising_pages", "Donations"),
                    ("petitions", "Signatures"),
                    ("advocacy_campaigns", "Outreaches"),
                ],
                max_length=50,
                verbose_name="API Resource name",
            ),
        ),
    ]