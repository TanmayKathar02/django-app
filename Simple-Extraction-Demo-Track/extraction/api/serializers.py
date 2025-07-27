from rest_framework import serializers

from extraction.models import UploadedDocument


class UploadedDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedDocument
        fields = ['id', 'name', 'document', 'file_type']
