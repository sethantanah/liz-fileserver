from django.urls import path, include
from django.contrib.auth import views as auth
from .views import sign_in, sign_up, activate, confirm_email

urlpatterns = [
    path('', sign_in, name='sign_in'),
    path('/login', sign_in, name='sign_in'),
    path('/sign-up', sign_up, name='sign_up'),
    path('/confirm-email', confirm_email, name='confirm_main'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         activate, name='activate')
]
