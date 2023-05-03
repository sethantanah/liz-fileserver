from django.urls import path
from .views import dashboard, upload_file, update_file,delete_file, confirm_delete_file
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('/upload', upload_file, name='upload_file'),
    path(r'^update/(?P<pk>/d+)$', update_file, name='update_file'),
    path(r'^delete/(?P<pk>/d+)$', delete_file, name='delete_file'),
    path(r'^confirm-delete/(?P<pk>/d+)$', confirm_delete_file, name='confirm_delete_file')
]