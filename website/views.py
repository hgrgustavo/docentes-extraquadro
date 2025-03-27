from django.views.generic import base, edit, list
from . import models, forms
from django import http
from django.template import loader
from xhtml2pdf import pisa


class Index(edit.CreateView):
    model = models.Usuario
    form_class = forms.LoginForm
    template_name = "login.html"
    success_url = "menu/inicio/"


class MenuInicio(list.ListView):
    template_name = "menu_inicio.html"
    model = models.Usuario
    context_object_name = "usuario"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            usuario = models.Usuario.objects.get(pk=1)
            context["get_nome"] = usuario.nome

        except models.Usuario.DoesNotExist:
            context["get_nome"] = None

        return context


class MenuCriarProfessor(edit.CreateView):
    template_name = "menu_criarprofessor.html"
    model = models.Professor
    form_class = forms.CriarProfessorForm
    success_url = "#"


class MenuListarProfessor(list.ListView):
    template_name = "menu_listarprofessor.html"
    model = models.Professor
    context_object_name = "professor"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class MenuGerarContrato(edit.CreateView):
    template_name = "menu_gerarcontrato.html"
    model = models.Solicitacao
    form_class = forms.GerarContratoForm
    success_url = "#"


class GeneratePDF(base.View):
    def render_to_pdf(html_src, context_dict):

        template = loader.get_template(html_src)
        html = template.render(context_dict)
        response = http.HttpResponse(content_type="application/pdf")
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return http.HttpResponse("Erro ao gerar PDF", status=500)

        return response

    def post(self, request, **kwargs):
        doc_data = models.Solicitacao.objects.order_by("id").desc()[0]
        context_dict = {
            "id": doc_data.id,
            "processo": doc_data.processo,
        }
