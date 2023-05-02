from django.urls import path
from .views import home_page, add_file
urlpatterns = [
    path('', home_page, name='index'),
    path('/add', add_file, name='add_file')
]