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
            choices=models.Professor.CHOICES,
            error_messages={"required": "Por favor, escolha entre PF ou PJ."})

        widgets = {
            "pf_ou_pj": forms.Select(attrs={"id": "pf_ou_pj", "class": "col-start-1 row-start-1 w-full appearance-none rounded-md bg-white py-1.5 pr-8 pl-3 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "data_nascimento": forms.DateInput(attrs={"id": "data_nascimento", "type": "date", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "nome": forms.TextInput(attrs={"id": "nome", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "email": forms.EmailInput(attrs={"id": "email", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "telefone": forms.TextInput(attrs={"type": "tel", "id": "telefone", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "cpf": forms.TextInput(attrs={"type": "text", "id": "cpf", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "cnpj": forms.TextInput(attrs={"type": "text", "id": "cnpj", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "observacao": forms.Textarea(attrs={"id": "obs", "rows": "3", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
        }


class GerarContratoForm(forms.ModelForm):
    class Meta:
        model = models.Contratos
        fields = [
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

        widgets = {
            "processo": forms.TextInput(attrs={"id": "pf_ou_pj", "class": "col-start-1 row-start-1 w-full appearance-none rounded-md bg-white py-1.5 pr-8 pl-3 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "evento": forms.DateInput(attrs={"id": "data_nascimento", "type": "date", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "prestador": forms.TextInput(attrs={"id": "nome", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "servico": forms.Textarea(attrs={"id": "obs", "rows": "3", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "componentes": forms.Textarea(attrs={"id": "obs", "rows": "3", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "data_inicio": forms.DateInput(attrs={"id": "data_nascimento", "type": "date", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "data_termino": forms.DateInput(attrs={"id": "data_nascimento", "type": "date", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "carga_horaria": forms.TextInput(attrs={"id": "nome", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
            "valor_hora_aula": forms.TextInput(attrs={"id": "nome", "class": "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"}),
        }
