from django.contrib import admin

from extraction.models import UploadedDocument, ExtractedData, TCExtract

admin.site.site_header = 'Extraction'
admin.site.site_title = 'Extraction'
admin.site.index_title = 'Extraction'

admin.site.register(UploadedDocument)
admin.site.register(ExtractedData)
admin.site.register(TCExtract)
