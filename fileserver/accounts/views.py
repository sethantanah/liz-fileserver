from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .formss import RegistrationForm, UserForms, ProfileForm
from .models import Profile
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


@login_required()
def profile(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'GET':
        form = ProfileForm(instance=user_profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, message='Profile Updated')
    return render(request, "profile.html", {'form': form, 'profile': user_profile})


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('verification/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                subject=mail_subject, message=message, from_email='sethsyd32@gmail.com', to=[to_email]
            )
            email.send()
            return redirect(reverse('confirm_main'))
        else:
            auth_error = 'Invalid email or password'
            return render(request, 'signup.html', {'form': form, 'auth_error': auth_error})
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})


def confirm_email(request):
    return render(request, 'verification/confirm_password.html')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'verification/activate_account.html',
                      {'message': 'Thank you for your email confirmation. Now you can login your account.'})
    else:
        return render(request, 'verification/activate_account.html', {'message': 'Activation link is invalid!'})


def sign_in(request):
    form = UserForms()
    if request.method == 'GET':
        return render(request, 'login.html', {'form': form})

    if request.method == 'POST':
        form = UserForms(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'You have been logged in!')
                return redirect(reverse('index'))  # render(request, 'login.html', {'form': form})
            else:
                auth_error = 'Invalid email or password'
                messages.error(request, 'Invalid email or password')
                return render(request, 'login.html', {'form': form, 'auth_error': auth_error})

        else:
            return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
