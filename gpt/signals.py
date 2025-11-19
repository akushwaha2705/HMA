from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UploadedPDF
from fleetAI.conversion import DocumentProcessor


@receiver(post_save, sender=UploadedPDF)
def process_uploaded_pdf(sender, instance, **kwargs):
    _ = DocumentProcessor(
        document=instance.pdf_file.name,
        collection=instance.user_group.name
    )
