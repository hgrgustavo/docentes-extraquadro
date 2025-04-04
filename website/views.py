from django.views.generic import base, edit, list
from . import models, forms
from django import http
from django.template import loader
from xhtml2pdf import pisa
import io
from django.core.files.base import ContentFile


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
    model = models.Contratos
    form_class = forms.GerarContratoForm

    def form_valid(self, form):
        try:
            contrato = form.save()

            pdf_buffer = GeneratePDF().render_to_pdf(
                "pdf_template.html",
                contrato.get_pdf_context()
            )

            if pdf_buffer:
                contrato.pdf.save(
                    f"contrato_{contrato.id}.pdf",
                    ContentFile(pdf_buffer.read()))

            pdf_buffer.close()

            return http.JsonResponse(  # melhorar retorno !
                {
                    "message": "PDF gerado com sucesso",
                    "contrato_id": contrato.id
                }
            )

        except Exception as e:
            return http.JsonResponse(
                {"error": f"Erro inesperado: {str(e)}"},
                status=500
            )


class GeneratePDF(base.View):
    def render_to_pdf(self, html_src, context_dict):
        try:
            template = loader.get_template(html_src)
            html = template.render(context_dict)
            buffer = io.BytesIO()

            pisa_status = pisa.CreatePDF(html, dest=buffer)

            if pisa_status.err:
                print("Erro na geração do PDF")
                return None

            buffer.seek(0)
            return buffer

        except Exception as e:
            print(f"Erro ao renderizar o PDF: {str(e)}")
            return None


class MenuHistorico(list.ListView):
    template_name = "menu_historico.html"
    context_object_name = "contratos"
    model = models.Contratos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["modalidade"] = models.ControlePagamento.objects.values(
            "modalidade"
        )

        return context
