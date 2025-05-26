from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core import validators, exceptions
from django.utils.translation import gettext_lazy as _
from typing import Any



class Professor(models.Model):
    CHOICES: list[tuple[str, str]] = [
        ("PF", "Pessoa Física"),
        ("PJ", "Pessoa Jurídica"),
    ]

    def __str__(self) -> str:
        return self.nome

    @staticmethod
    def remove_mask(string: str) -> str:
        return "".join(filter(str.isdigit, string))

    @staticmethod
    def check_cpf_digit(cpf: str, position: int) -> str:
        product = sum(int(cpf[i]) * (position - i)
                      for i in range(len(cpf)))
        remnant = product % 11

        return str(0 if remnant < 2 else str(11 - remnant))

    @staticmethod
    def check_cnpj_digit(cnpj: str, weights: list[int]) -> str:
        product = sum(int(cnpj[i]) * weights[i] for i in range(len(weights)))
        remnant = product % 11

        return str(0 if remnant < 2 else str(11 - remnant))

    def verify_cpf(self, cpf: str) -> None:
        new_cpf: str = Professor.remove_mask(cpf)

        if len(new_cpf) != 11:
            raise exceptions.ValidationError(
                _("CPF com tamanho inválido."), code="invalid")

        if new_cpf == new_cpf[0] * 11:
            raise exceptions.ValidationError(
                _("CPF com digitos repetidos."), code="invalid")

        first_digit: str = Professor.check_cpf_digit(new_cpf[:9], 10)
        second_digit: str = Professor.check_cpf_digit(new_cpf[:9] + first_digit, 11)

        if new_cpf[-2:] != f"{first_digit + second_digit}":
            raise exceptions.ValidationError(
                _("CPF com digitos verificadores inválidos."), code="invalid")

    def verify_cnpj(self, cnpj: str) -> None:
        new_cnpj: str = Professor.remove_mask(cnpj)
        first_weights: list[int] = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        second_weights: list[int] = [6] + first_weights

        if len(new_cnpj) != 14:
            raise exceptions.ValidationError(
                _("O CNPJ deve conter 14 dígitos!"), code="invalid")

        if new_cnpj == new_cnpj[0] * 14:
            raise exceptions.ValidationError(
                _("CNPJ inválido: não pode conter todos os digitos iguais!"), code="invalid")

        first_digit: str = Professor.check_cnpj_digit(
            new_cnpj[:12], first_weights)
        second_digit: str = Professor.check_cnpj_digit(
            new_cnpj[:12] + first_digit, second_weights)

        if new_cnpj[-2:] != f"{first_digit + second_digit}":
            raise exceptions.ValidationError(
                ("CNPJ com digitos verificadores inválidos!"), code="invalid")

    nome = models.CharField(max_length=45)
    email = models.EmailField(max_length=255, validators=[validators.EmailValidator()])
    telefone = models.CharField(max_length=45)
    data_nascimento = models.DateField()
    observacao = models.TextField()
    pf_ou_pj = models.CharField(max_length=15, choices=CHOICES)
    cpf = models.CharField(max_length=14, null=True, blank=True, validators=[
        validators.RegexValidator(
            regex=r"\d{3}\.?\d{3}\.?\d{3}-?\d{2}$"),
        verify_cpf
    ])
    cnpj = models.CharField(max_length=18, null=True, blank=True, validators=[
                            validators.RegexValidator(
                                regex=r"^\d{2}\.?(\d{3}\.?){2}/?\d{4}-?\d{2}$"),
                            verify_cnpj])

    class Meta:
        db_table: str = "professor"

    def clean(self) -> None:
        if self.cpf and self.cnpj:
            raise exceptions.ValidationError(
                "Escolha entre Pessoa Física ou Jurídica.")


class UsuarioManager(BaseUserManager["Usuario"]):
    def create_user(self, nome: str, email: str, numero_telefone: str, data_nascimento: str, password: str):
        if not nome:
            raise ValueError("O name é obrigatório.")
        
        if not email:
            raise ValueError("O name é obrigatório.")
        
        if not numero_telefone:
            raise ValueError("O número de telefone é obrigatório")
        
        if not data_nascimento:
            raise ValueError("A data de nascimento é obrigatória")
        
        if not password:
            raise ValueError("A senha deve ser obrigatória")
        
        usuario = self.model (
            nome = nome,
            email = self.normalize_email(email),
            data_nascimento = data_nascimento,
        )
        usuario.set_password(password)
        usuario.save(using=self._db)


class Usuario(AbstractBaseUser):
    nome = models.CharField(max_length=45)
    email = models.EmailField(max_length=255, validators=[validators.EmailValidator()], unique=True)
    numero_telefone = models.CharField(max_length=45, validators=[
        validators.RegexValidator(regex=r"^\+?\d{10,15}$")])
    data_nascimento = models.DateField()
    password = models.CharField(max_length=512)

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["__all__"]

    def __str__(self) -> str:
        return self.nome

    class Meta:
        db_table: str = "usuario"


class Contratos(models.Model):
    CHOICES_MODALIDADES: list[tuple[str, str]] = [
        ("hora-aula", "Hora-aula"),
    ]

    processo = models.CharField(max_length=255)
    evento = models.DateField()
    prestador = models.ForeignKey(Professor, on_delete=models.CASCADE)
    servico = models.CharField(max_length=255)
    componentes = models.CharField(max_length=255)
    data_inicio = models.DateField()
    data_termino = models.DateField()
    carga_horaria = models.IntegerField()
    valor_hora_aula = models.FloatField()
    modalidade = models.CharField(
        max_length=50, default="hora-aula", choices=CHOICES_MODALIDADES
    )

    class Meta:
        db_table: str = "contratos"

    def get_pdf_context(self) -> dict[str, Any]:
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
