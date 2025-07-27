from django import forms
from django.forms import ModelForm, Form

from extraction.models import ExtractedData, UploadedDocument


class ExtractionForm(ModelForm):
    class Meta:
        model = ExtractedData
        exclude = ['created_at', 'updated', 'mto_id', 'document']


class UploadDocumentForm(ModelForm):
    class Meta:
        model = UploadedDocument
        fields = ['name', 'document']


class SendEmailForm(Form):
    """
    Form for sending an email after the extraction is completed.
    """
    email = forms.EmailField()
    subject = forms.CharField(max_length=255)
    cc = forms.EmailField()
    document = forms.FileField()
    surname = forms.CharField(max_length=255, required=False)
    given_name = forms.CharField(max_length=255, required=False)
    nationality = forms.CharField(max_length=255, required=False)
    issue_date = forms.DateField()
    expiry_date = forms.DateField()

