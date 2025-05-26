from typing import Any
from django import forms
from . import models


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"id": "login_email", "class": "bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500", "placeholder": "name@company.com", "required": ""}))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"id": "login_password", "class": "bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500", "placeholder": "••••••••", "required": ""}))


class CriarProfessorForm(forms.ModelForm):
    class Meta:
        model = models.Professor
        fields: list[str] = [
            "nome",
            "email",
            "telefone",
            "data_nascimento",
            "observacao",
            "pf_ou_pj",
            "cpf",
            "cnpj",
        ]

        widgets: dict[str, Any] = {
            "pf_ou_pj": forms.Select(attrs={"id": "pf_ou_pj", "class": "col-start-1 row-start-1 w-full appearance-none rounded-md bg-white py-1.5 pr-8 pl-3 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "data_nascimento": forms.DateInput(attrs={"id": "data_nascimento", "type": "date", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "nome": forms.TextInput(attrs={"id": "nome", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "email": forms.EmailInput(attrs={"id": "email", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "telefone": forms.TextInput(attrs={"type": "tel", "id": "telefone", "class": "resize-none !block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "cpf": forms.TextInput(attrs={"type": "text", "id": "cpf", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "cnpj": forms.TextInput(attrs={"type": "text", "id": "cnpj", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "observacao": forms.Textarea(attrs={"id": "obs", "rows": "3", "class": "resize-none block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
        }


class GerarContratoForm(forms.ModelForm):
    class Meta:
        model = models.Contratos
        fields: list[str] = [
            "processo",
            "evento",
            "prestador",
            "servico",
            "componentes",
            "data_inicio",
            "data_termino",
            "carga_horaria",
            "valor_hora_aula",
        ]

        widgets: dict[str, Any] = {
            "processo": forms.TextInput(attrs={"id": "pf_ou_pj", "class": "col-start-1 row-start-1 w-full appearance-none rounded-md bg-white py-1.5 pr-8 pl-3 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "evento": forms.DateInput(attrs={"id": "data_nascimento", "type": "date", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "prestador": forms.Select(attrs={"id": "nome", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "servico": forms.Textarea(attrs={"id": "obs", "rows": "3", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "componentes": forms.Textarea(attrs={"id": "obs", "rows": "3", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "data_inicio": forms.DateInput(attrs={"id": "data_nascimento", "type": "date", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "data_termino": forms.DateInput(attrs={"id": "data_nascimento", "type": "date", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "carga_horaria": forms.TextInput(attrs={"id": "nome", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "valor_hora_aula": forms.TextInput(attrs={"id": "nome", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
        }
