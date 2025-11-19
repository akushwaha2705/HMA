from django.db import models
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')


class UploadedPDF(models.Model):
    pdf_file = models.FileField(upload_to="", validators=[validate_file_extension])
    user_group = models.ForeignKey(Group, on_delete=models.CASCADE)
