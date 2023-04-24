# Generated by Django 4.2 on 2023-04-17 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auth2", "0001_initial"),
        (
            "actionnetwork",
            "0006_remove_signature_campaign_remove_signature_person_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaign",
            name="action_group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="auth2.usersgroup",
            ),
        ),
        migrations.DeleteModel(
            name="ActionGroup",
        ),
    ]