from django.db import models


class UploadedDocument(models.Model):
    name = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    file_type = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ExtractedDataAbstract(models.Model):
    document = models.ForeignKey(UploadedDocument, on_delete=models.CASCADE)
    surname = models.CharField(max_length=255, blank=True)
    given_name = models.CharField(max_length=255, blank=True)
    nationality = models.CharField(max_length=255, blank=True)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{str(self.surname)}-{str(self.given_name)}-{str(self.nationality)}"

    class Meta:
        abstract = True


class ExtractedData(ExtractedDataAbstract):
    mto_id = models.CharField(max_length=255, blank=True)


class TCExtract(ExtractedDataAbstract):
    pass
