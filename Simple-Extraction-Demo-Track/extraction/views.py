import os

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import CreateView, ListView

from extraction.forms import ExtractionForm, UploadDocumentForm, SendEmailForm
from extraction.helpers import send_email_, apply_tc_to_data_extract
from extraction.models import ExtractedData, UploadedDocument, TCExtract


class ExtractionView(SuccessMessageMixin, CreateView):
    """
    Extracts data from uploaded document and saves it to the database.
    triggers perform TC Extract function if 3 or more data fields are extracted for the same document.
    """
    model = ExtractedData
    template_name = 'extraction/created_extraction.html'
    form_class = ExtractionForm
    success_url = '/'
    success_message = 'Extraction created successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document'] = get_object_or_404(UploadedDocument, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.document = get_object_or_404(UploadedDocument, pk=self.kwargs['pk'])
        instance.mto_id = self.kwargs.get('email')
        instance.save()
        if ExtractedData.objects.filter(document=instance.document).count() >= 3:
            # applying TC Extract
            apply_tc_to_data_extract(instance.document.pk)
        return super().form_valid(form)


class UploadDocumentView(SuccessMessageMixin, CreateView):
    """
    Uploading a document and sending an email to MTOs
    """
    model = UploadedDocument
    template_name = 'extraction/upload_document.html'
    form_class = UploadDocumentForm
    success_message = 'Document Uploaded successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uploaded_documents'] = UploadedDocument.objects.all().order_by('-created_at')
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        document = form.cleaned_data.get('document')
        instance.name = os.path.splitext(f"{document.name}")[0]
        instance.file_type = os.path.splitext(f"{document.name}")[1].replace(".", "")
        instance.save()
        return JsonResponse({'success': True})


def get_tc_extract(request, pk):
    """
    Getting TC Extract for a document and using it to supply initial data for SendEmailForm
    :param request:
    :param pk:
    :return:
    """
    tc_extract = get_object_or_404(TCExtract, pk=pk)
    initial_data = {'surname': tc_extract.surname, 'given_name': tc_extract.given_name,
                    'nationality': tc_extract.nationality, "document": tc_extract.document.document,
                    'issue_date': tc_extract.issue_date, 'expiry_date': tc_extract.expiry_date,
                    'email': 'track20@varaluae.com',
                    }
    form = SendEmailForm(initial=initial_data)
    return render(request, 'extraction/tc_extract.html', {'form': form, 'tc_extract': tc_extract})


class ApplicationView(View):
    """
    Gets all the TC Extracts and sends an email to the emails from SendEmailForm
    """
    template_name = 'extraction/application.html'

    def get(self, request):
        tc_extracts = TCExtract.objects.select_related('document').all().order_by('-created_at')
        return render(request, self.template_name, {'tc_extracts': tc_extracts})

    def post(self, request):
        email = request.POST.get('email')
        cc = request.POST.get('cc')
        subject = request.POST.get('subject')
        tc_id = request.POST.get('tc_id')
        tc_extract = get_object_or_404(TCExtract, pk=tc_id)
        email_template = 'extraction/email/application_email.html'
        send_email_(subject=subject, to_email=[email], data=tc_extract, email_template=email_template,
                    attachment=tc_extract.document.document, cc=[cc])
        messages.success(request, 'Application sent successfully')
        tc_extracts = TCExtract.objects.all().order_by('-created_at')
        return render(request, self.template_name, {'tc_extracts': tc_extracts})


class TCExtractListView(ListView):
    """
    List of all TC Extracts
    """
    model = TCExtract
    template_name = 'extraction/tc_extract_list.html'
    queryset = TCExtract.objects.select_related("document").all().order_by('-created_at')
