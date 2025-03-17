from django.forms import ModelForm, TextInput, PasswordInput
from . import models 


class LoginForm(ModelForm):
  

    class Meta:
      
        model = models.Usuario
        fields = [
            "email",
            "senha",
        ]

        widgets = {
            "email": TextInput(attrs={"placeholder": "Email", "pattern" : r'/^[a-zA-Z0-9.!#$%&*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/', "class": "form-control w-25","id": "login_input"}),
            "senha": PasswordInput(attrs={"placeholder": "Senha", "class": "form-control w-25", "id": "login_input"}),
        }


