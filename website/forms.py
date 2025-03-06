from django.forms import ModelForm, TextInput, PasswordInput
from . import models 


class LoginForm(ModelForm):
  

    class Meta:
        tailwind_input = "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"


        model = models.Usuario 
        fields = [
            "email",
            "senha",
        ]

        widgets = {
            "email": TextInput(attrs={"pattern" : r'/^[a-zA-Z0-9.!#$%&*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/', "class" : tailwind_input}),
            "senha": PasswordInput(attrs={"class" : tailwind_input}),
        }


