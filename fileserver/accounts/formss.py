from django import forms
import datetime
from django.contrib.auth import get_user_model
from .models import User
from .models import Profile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=30)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone']


class UserForms(forms.Form):
    email = forms.EmailField(max_length=100, required=True, help_text='Email')
    password = forms.CharField(max_length=100, required=True, help_text='Password',
                               widget=forms.PasswordInput(render_value=True))


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = get_user_model()
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email

    def clean_password(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password_confirm")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'],
                                        code='password_mismatch')
        return password2

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.registration_date = datetime.date.today()
        user.last_login = datetime.date.today()
        user.set_password("password")
        if commit:
            user.save()
        return user
