from django.urls import path, include
from django.contrib.auth import views as auth
from .views import sign_in, sign_up, activate, confirm_email
from django.views.generic import RedirectView

from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
)

urlpatterns = [
    path('', sign_in, name='sign_in'),
    path('/login', sign_in, name='sign_in'),
    path('/sign-up', sign_up, name='sign_up'),
    path('/logout', LogoutView.as_view(next_page='sign_in'), name='logout'),
    path('/confirm-email', confirm_email, name='confirm_main'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         activate, name='activate')
]

urlpatterns += [
    path('/password-reset', PasswordResetView.as_view(template_name='password-reset/password_reset.html',
                                                      html_email_template_name='password-reset/password_reset_email.html'),
         name='password_reset'),
    path('/password-reset/done', PasswordResetDoneView.as_view(template_name='password-reset/password_reset_done.html'),
         name='password_reset_done'),
    path('/password_reset_confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='password-reset'
                                                                                                    '/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('/password-reset-complete',
         RedirectView.as_view(url='login'),
         name='password_reset_complete'),
]

