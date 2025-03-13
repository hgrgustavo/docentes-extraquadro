from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from . import models, forms


class IndexView(CreateView):
    model = models.Usuario
    form_class = forms.LoginForm
    template_name = "login.html"
    success_url = "menu/"

class MenuView(TemplateView):
    template_name = "menu.html"

class InicioView(ListView):
    template_name = "menu_inicio.html"
    models = models.Usuario
    context_object_name = "usuario"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context




