from django.db import models


class Files(models.Model):
    title = models.CharField(max_length=255, help_text='title', blank=False)
    description = models.CharField(max_length=255, help_text='description', blank=True)
    file_url = models.CharField(max_length=255, help_text='url', blank=True)
    file = models.FileField(help_text='file', blank=True)
    file_type = models.CharField(max_length=255, help_text='', blank=True)
    published = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title


class FileTracker(models.Model):
    file = models.OneToOneField(Files, on_delete=models.CASCADE)
    downloads = models.IntegerField(default=0)
    emails = models.IntegerField(default=0)
