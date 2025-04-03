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
    success_url = "#"


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

    def post(self, request, **kwargs):
        try:
            query = models.Contratos.objects.order_by("-id").first()
            if not query:
                return http.JsonResponse(
                    {"error": "Nenhum contrato encontrado"}, status=404
                )

            context_dict = {
                "id": query.id,
                "processo": query.processo,
                "evento": query.evento_sige,
                "prestador": query.prestador,
                "servico": query.servico,
                "componentes": query.curso_treinamento,
                "data_inicio": query.data_inicio,
                "data_termino": query.data_termino,
                "carga_horaria": query.carga_horaria,
                "valor_hora_aula": query.valor_hora,
            }

            response_buffer = self.render_to_pdf(
                "pdf_template.html", context_dict)

            if not response_buffer:
                return http.JsonResponse(
                    {"error": "Erro ao gerar o PDF"}, status=500
                )

            query.pdf.save(
                f"contrato_{query.id}.pdf", ContentFile(response_buffer.read())
            )

            response_buffer.close()

            return http.JsonResponse(
                {
                    "message": "PDF gerado com sucesso",
                    "pdf_url": query.pdf.url,
                }
            )

        except models.Contratos.DoesNotExist:
            return http.JsonResponse({"error": "Contrato não encontrado"}, status=404)

        except Exception as e:
            return http.JsonResponse(
                {"error": f"Erro inesperado: {str(e)}"}, status=500
            )


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
