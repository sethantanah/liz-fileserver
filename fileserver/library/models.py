from django.db import models
from django.shortcuts import reverse
import os


def upload_to(instance, filename):
    if instance.file_type == 'audio':
        return os.path.join('media/', filename)
    else:
        pass


class Files(models.Model):
    title = models.CharField(max_length=255, help_text='title', blank=False)
    description = models.CharField(max_length=255, help_text='description', blank=True)
    file_url = models.CharField(max_length=255, help_text='url', blank=True)
    file = models.FileField(help_text='file', blank=True, upload_to='files/')
    file_type = models.CharField(max_length=255, help_text='', blank=True)
    published = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('preview', args=[str(self.id)])

    def get_download_url(self):
        return reverse('download', args=[str(self.id)])

    def get_email_url(self):
        return reverse('email', args=[str(self.id)])

    def get_update_url(self):
        return reverse('update_file', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('delete_file', args=[str(self.id)])

    def get_confirm_delete_url(self):
        return reverse('confirm_delete_file', args=[str(self.id)])


class FileTracker(models.Model):
    file = models.OneToOneField(Files, on_delete=models.CASCADE)
    downloads = models.IntegerField(default=0)
    emails = models.IntegerField(default=0)

    def __str__(self):
        return self.file.title

# 530
# 151