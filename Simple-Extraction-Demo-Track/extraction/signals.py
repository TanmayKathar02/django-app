from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy

from extraction.helpers import send_email_
from extraction.models import UploadedDocument


@receiver(post_save, sender=UploadedDocument)
def send_email_to_mto_after_upload(sender, instance, created, **kwargs):
    if created:
        subject = 'New Document Uploaded'
        mto_emails = ["mto1@varaluae.com", "track14@varaluae.com", "track15@varaluae.com"]
        for email in mto_emails:
            email_template = 'extraction/email/document_uploaded_email.html'
            data_extraction_url = reverse_lazy('extraction:create_extraction',
                                               kwargs={'pk': instance.pk, 'email': email})
            domain = Site.objects.all().first().domain
            send_email_(
                subject=subject, to_email=[email],
                data={"name": instance.name, 'extraction_url': data_extraction_url, 'domain': domain},
                email_template=email_template, attachment=instance.document)
