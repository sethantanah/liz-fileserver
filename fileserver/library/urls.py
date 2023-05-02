from django.urls import path
from .views import home_page, add_file, file_preview
urlpatterns = [
    path('', home_page, name='index'),
    path('/add', add_file, name='add_file'),
    path(r'^preview/(?P<pk>/d+)$', file_preview, name='preview' )
]