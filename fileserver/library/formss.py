from django.forms import ModelForm
from .models import Files


class FileForm(ModelForm):
    class Meta:
        model = Files
        fields = ['file', 'title', 'description',  'file_type']

