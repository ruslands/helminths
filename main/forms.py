from django import forms
import os
import xlrd
from .models import Document

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

IMPORT_FILE_TYPES = ['.xls', ]

class ExcelUploadForm(forms.Form):
    # class Meta:
    #     model = Document
    #     fields = ('docfile', )
    image = forms.FileField()
