from django.views.generic import base, edit, list
from . import models, forms


class Index(edit.CreateView):
    model = models.Usuario
    form_class = forms.LoginForm
    template_name = "login.html"
    success_url = "menu/"


class Menu(base.TemplateView):
    template_name = "menu.html"


class MenuInicio(list.ListView):
    template_name = "menu_inicio.html"
    model = models.Usuario
    context_object_name = "usuario"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Busca o usuário diretamente pelo ID
            usuario = models.Usuario.objects.get(pk=1)
            context["get_nome"] = usuario.nome  # Pega apenas o nome do usuário

        except models.Usuario.DoesNotExist:
            # Se o usuário não for encontrado, retorna None
            context["get_nome"] = None

        return context


class MenuCriarProfessor(edit.CreateView):
    template_name = "menu_criarprofessor.html"
    model = models.Professor
    form_class = forms.CriarProfessorForm
