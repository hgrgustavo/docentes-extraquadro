from django.contrib.auth import hashers
from django.db import models
from django.core import validators, exceptions
import os


class Professor(models.Model):
    CHOICES = [
        ("PF", "Pessoa Física"),
        ("PJ", "Pessoa Jurídica"),
    ]

    def remove_mask(string: str) -> str:
        return "".join(filter(str.isdigit, string))

    def check_cpf_digit(cpf: str, position: int):
        product = sum(int(cpf[i]) * (position - i)
                      for i in range(len(cpf)))
        remant = product % 11

        return "0" if remant < 2 else str(11 - remant)

    def check_cnpj_digit(cnpj: str, weights: list[int]):
        product = sum(int(cnpj[i]) * weights[i] for i in range(len(weights)))
        remnant = product % 11

        return "0" if remnant < 2 else str(11 - remnant)

    def verify_cpf(cpf: str) -> bool:
        try:
            new_cpf = Professor.remove_mask(cpf)

            if len(new_cpf) != 11:
                raise exceptions.ValidationError(
                    "O CPF deve conter 11 dígitos!")

            if new_cpf == new_cpf[0] * 11:
                raise exceptions.ValidationError(
                    "CPF inválido: não pode conter todos os dígitos iguais!")

            first_digit = Professor.check_cpf_digit(new_cpf[:9], 10)
            second_digit = Professor.check_cpf_digit(new_cpf[:10], 11)

            return new_cpf[-2:] == first_digit + second_digit

        except exceptions.ValidationError as e:
            raise exceptions.ValidationError("CPF Inválido!") from e

    def verify_cnpj(cnpj: str) -> bool:
        try:
            new_cnpj = Professor.remove_mask(cnpj)
            first_weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            second_weights = [6] + first_weights

            if len(new_cnpj) != 14:
                raise exceptions.ValidationError(
                    "O CNPJ deve conter 14 dígitos!")

            if new_cnpj == new_cnpj[0] * 14:
                raise exceptions.ValidationError(
                    "CNPJ inválido: não pode conter todos os digitos iguais!")

            first_digit = Professor.check_cnpj_digit(
                new_cnpj[:12], first_weights)
            second_digit = Professor.check_cnpj_digit(
                new_cnpj[:12] + first_digit, second_weights)

            return new_cnpj[-2:] == first_digit + second_digit

        except exceptions.ValidationError as e:
            raise exceptions.ValidationError("CPF Inválido!") from e

    nome = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    telefone = models.CharField(max_length=45)
    data_nascimento = models.DateField()
    observacao = models.TextField()
    pf_ou_pj = models.CharField(max_length=15, choices=CHOICES)
    cpf = models.CharField(max_length=14, null=True, blank=True, validators=[validators.RegexValidator(
        regex=r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}$'), verify_cpf])
    cnpj = models.CharField(max_length=18, null=True, blank=True, validators=[
                            validators.RegexValidator(regex=r'^\d{2}\.?(\d{3}\.?){2}/?\d{4}-?\d{2}$'), verify_cnpj])

    class Meta:
        db_table = 'professor'

    def clean(self):
        if self.cpf and self.cnpj:
            raise exceptions.ValidationError("Pessoa Física não pode ter CNPJ")


class Usuario(models.Model):
    nome = models.CharField(max_length=45)
    email = models.EmailField(max_length=255, validators=[
        validators.EmailValidator])
    numero_telefone = models.CharField(max_length=45, validators=[
        validators.RegexValidator(regex=r'^\+?\d{10,15}$')])
    senha = models.CharField(max_length=512, default="")

    def save(self, *args, **kwargs):
        if self.senha:
            self.senha = hashers.make_password(
                self.senha,
                salt=os.urandom(16).hex(),
                hasher=hashers.ScryptPasswordHasher()
            )
        super().save(*args, **kwargs)

    def check_password(self, password):
        return hashers.check_password(password, self.senha)

    class Meta:
        db_table = 'usuario'


class Contratos(models.Model):
    CHOICES_MODALIDADES = [
        ("hora-aula", "Hora-aula"),
    ]

    processo = models.CharField(max_length=255)
    evento = models.DateField()
    prestador = models.CharField(max_length=255)
    servico = models.CharField(max_length=255)
    componentes = models.CharField(max_length=255)
    data_inicio = models.DateField()
    data_termino = models.DateField()
    carga_horaria = models.IntegerField()
    valor_hora_aula = models.FloatField()
    modalidade = models.CharField(
        max_length=50, default="hora-aula", choices=CHOICES_MODALIDADES)

    class Meta:
        db_table = 'contratos'

    def get_pdf_context(self):
        return {
            "id": self.pk,
            "processo": self.processo,
            "evento": self.evento,
            "prestador": self.prestador,
            "servico": self.servico,
            "componentes": self.componentes,
            "data_inicio": self.data_inicio,
            "data_termino": self.data_termino,
            "carga_horaria": self.carga_horaria,
            "valor_hora_aula": self.valor_hora_aula,
            "total_valor": self.valor_hora_aula * self.carga_horaria,
        }
