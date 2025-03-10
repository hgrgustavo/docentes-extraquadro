from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from . import models 
from . import forms


class IndexView(CreateView):
    model = models.Usuario
    form_class = forms.LoginForm
    template_name = "login.html"
    success_url = "menu/"

class MenuView(TemplateView):
    template_name = "menu.html"




