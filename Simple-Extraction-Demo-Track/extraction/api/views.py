from rest_framework.generics import ListAPIView

from extraction.api.serializers import UploadedDocumentSerializer
from extraction.models import UploadedDocument


class UploadedDocumentList(ListAPIView):
    """
    List all uploaded documents.
    """
    queryset = UploadedDocument.objects.all()
    serializer_class = UploadedDocumentSerializer
