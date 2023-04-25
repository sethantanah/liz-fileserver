from django.urls import path, include
from django.contrib.auth import views as auth
from .views import sign_up

urlpatterns = [
    path('/sign-up', sign_up, name='sign_up'),
]
