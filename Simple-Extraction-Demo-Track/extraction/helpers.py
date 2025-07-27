from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from extraction.models import UploadedDocument, ExtractedData, TCExtract
from extraction.utils import EmailThread


def send_email_(subject, to_email, data, email_template, attachment=None, cc=None, extraction_url=None):
    """
    Sends an email with attachment.
    :param extraction_url:
    :param cc:
    :param subject:
    :param to_email:
    :param data:
    :param email_template:
    :param attachment:
    :return:
    """
    print(f"Sending email to {to_email} {type(to_email)}")
    message = render_to_string(email_template, {'data': data, 'extraction_url': extraction_url})
    EmailThread(subject, message, to_email, attachment, cc).start()


def apply_tc_extract(document: UploadedDocument) -> dict:
    """
    Applies TC Extract to the document.
    :param document:
    :return:
    """
    extractions = ExtractedData.objects.filter(document=document)
    data = dict(document=document)
    for extraction in extractions:
        if extractions.filter(surname__icontains=extraction.surname).count() >= 2:
            data['surname'] = extraction.surname
        if extractions.filter(given_name__icontains=extraction.given_name).count() >= 2:
            data['given_name'] = extraction.given_name
        if extractions.filter(nationality__icontains=extraction.nationality).count() >= 2:
            data['nationality'] = extraction.nationality
        if extractions.filter(issue_date=extraction.issue_date).count() >= 2:
            data['issue_date'] = extraction.issue_date
        if extractions.filter(expiry_date=extraction.expiry_date).count() >= 2:
            data['expiry_date'] = extraction.expiry_date
    return data


def create_tc_extract(data: dict) -> bool:
    """
    Creates a TC Extract from the supplied data.
    :param data:
    :return:
    """
    print(f"Creating TC Extract from {data}")
    try:
        instance = TCExtract(**data)
        instance.save()
    except Exception as e:
        email = "track6@varaluae.com"
        subject = 'New Document Uploaded'
        email_template = 'extraction/email/document_uploaded_email.html'
        data_extraction_url = reverse_lazy('extraction:create_extraction',
                                           kwargs={'pk': data['document'].pk, 'email': email})
        domain = Site.objects.all().first().domain
        send_email_(
            subject=subject, to_email=[email],
            data={"name": data['document'].name, 'extraction_url': data_extraction_url, 'domain': domain},
            email_template=email_template, attachment=data['document'].document)


def apply_tc_to_data_extract(pk: int) -> None:
    """
    calls apply_tc_extract and create_tc_extract to apply TC Extract to the document.
    :param pk:
    :return:
    """
    document = get_object_or_404(UploadedDocument, pk=pk)
    data = apply_tc_extract(document)
    if data:
        create_tc_extract(data)
        print("TC Extract created")
    else:
        print("No TC Extract created")
