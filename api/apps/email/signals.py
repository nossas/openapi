from .clients import SendGridEmailClient


def post_action_record_email_message(sender, instance, created, **kwargs):
    from apps.actionnetwork.models import ActionRecord
    from apps.actionnetwork.models.campaigns import EmailTemplateOptions
    from apps.actionnetwork.models.details import IntegrationOptions

    if created and issubclass(sender, ActionRecord):
        
        integration = instance.campaign.action_group.integration_set.filter(
            name=IntegrationOptions.SENDGRID
        ).first()

        if integration and "API_KEY" in integration.config:
            client = SendGridEmailClient(api_key=integration.config.get("API_KEY"))

            email_template = instance.campaign.emailtemplate_set.filter(email_type=EmailTemplateOptions.POST_ACTION).first()
            if email_template:
                client.send_mail(
                    from_email=f"{email_template.from_name} <{email_template.from_email}>",
                    to_email=instance.person.email_addresses.first().address,
                    subject=email_template.subject,
                    content=email_template.content
                )
