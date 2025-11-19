from django.contrib.auth.models import Group
from django import forms

from .models import UploadedPDF


class PDFUploadForm(forms.ModelForm):
    user_group = forms.ModelChoiceField(queryset=Group.objects.all())
    
    class Meta:
        model = UploadedPDF
        fields = ['pdf_file', 'user_group']
