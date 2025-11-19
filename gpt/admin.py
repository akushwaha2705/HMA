from django.contrib import admin
from .models import UploadedPDF


@admin.register(UploadedPDF)
class UploadedPDFAdmin(admin.ModelAdmin):
    list_display = ('pdf_file', 'user_group')
    search_fields = ('pdf_file', 'user_group__name')
    list_filter = ('user_group',)
