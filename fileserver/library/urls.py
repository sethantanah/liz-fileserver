from django.urls import path
from .views import home_page, file_preview, download_file, send_email_with_attachment
urlpatterns = [
    path('', home_page, name='index'),
    path(r'^preview/(?P<pk>/d+)$', file_preview, name='preview'),
    path(r'^download/(?P<pk>/d+)$', download_file, name='download'),
    path(r'^email/(?P<pk>/d+)$', send_email_with_attachment, name='email')
]