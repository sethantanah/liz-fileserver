from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend, UserModel, BaseBackend
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q
from .models import User


class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        print(email)
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None