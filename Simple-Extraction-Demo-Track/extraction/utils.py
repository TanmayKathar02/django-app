import mimetypes
import threading

from django.core.mail import EmailMessage

from core.settings import EMAIL_HOST_USER


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list, attachment=None, cc=None):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.attachment = attachment
        self.cc = cc
        threading.Thread.__init__(self)

    def run(self):
        mail = EmailMessage(
            subject=self.subject, body=self.html_content, from_email="Habot Data Extraction", to=self.recipient_list,
            cc=self.cc
            )
        attach = self.attachment
        if attach:
            mail.attach(attach.name, attach.read(), mimetypes.guess_type(attach.url)[1])
        mail.content_subtype = "html"
        mail.send()

