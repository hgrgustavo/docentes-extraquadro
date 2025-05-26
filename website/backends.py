from django.contrib.auth.hashers import check_password
from .models import Usuario
from django.http import HttpRequest


class CustomAuthentication:
    @staticmethod
    def authenticate(request: HttpRequest, email: str, password: str) -> Usuario | None:
        try:
            user = Usuario.objects.get(email=email)
            
        except Usuario.DoesNotExist:
            return None

        if check_password(password, user.password):
            return user

        return None

    def get_user(self, user_id: int) -> Usuario | None:
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None

