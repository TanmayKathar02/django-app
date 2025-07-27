from django.urls import path

from extraction.api.views import UploadedDocumentList

urlpatterns = [
    path('uploaded-documents/', UploadedDocumentList.as_view()),
]
