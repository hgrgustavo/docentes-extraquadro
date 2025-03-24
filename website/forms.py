from django import forms
from . import models


class LoginForm(forms.ModelForm):
    class Meta:
        model = models.Usuario
        fields = [
            "email",
            "senha",
        ]


class CriarProfessorForm(forms.ModelForm):
    class Meta:
        model = models.Professor
        fields = [
            "nome",
            "email",
            "telefone",
            "data_nascimento",
            "observacao",
            "pf_ou_pj",
            "cpf",
            "cnpj",
        ]
        pf_ou_pj = forms.ChoiceField(
            choices=[(""), ("Selecionar")] + models.Professor.CHOICES,
            error_messages={"required": "Por favor, escolha entre PF ou PJ."})

        widgets = {

        }
