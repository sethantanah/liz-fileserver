from django.contrib import admin

from .models import Files, FileTracker

admin.site.register(Files)
admin.site.register(FileTracker)
