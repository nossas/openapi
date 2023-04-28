import sendgrid
# import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email, To, Content, Mail


class EmailClientAbsctract(object):

    def send_mail(self, from_email, to_email, subject, content, **kwargs):
        raise NotImplementedError


class SendGridEmailClient(EmailClientAbsctract):

    def __init__(self, api_key):
        self._api = SendGridAPIClient(api_key=api_key)

    def send_mail(self, from_email, to_email, subject, content, **kwargs):
        from_email = Email(from_email)
        to_email = To(to_email)
        content = Content("text/html", content)
        mail = Mail(from_email, to_email, subject, content)

        return self._api.client.mail.send.post(request_body=mail.get())