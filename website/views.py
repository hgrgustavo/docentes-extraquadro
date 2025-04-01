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
        try:
            query = models.Solicitacao.objects.order_by("-id").first()
            if not query:
                return http.JsonResponse({"error": "Nenhuma solicitação encontrada"}, status=404)

            context_dict = {
                "id": query.id,
                "processo": query.processo,
                "evento_sige": query.evento_sige,
                "prestador": query.prestador,
                "servico": query.servico,
                "curso_treinamento": query.curso_treinamento,
                "data_inicio": query.data_inicio,
                "data_termino": query.data_termino,
                "horario_inicio": query.horario_inicio,
                "horario_termino": query.horario_termino,
                "carga_horaria": query.carga_horaria,
                "valor_hora": query.valor_hora,
                "parecer_coordenacao": query.parecer_coordenacao,
                "parecer_secretaria": query.parecer_secretaria,
            }

            response = self.render_to_pdf("pdf_template.html", context_dict)
            query.pdf.save(f"contrato_{query.id}.pdf", response)

            if response.status_code == 500:
                return http.JsonResponse({"error": "Erro ao gerar o PDF"}, status=500)

            return http.JsonResponse({
                "message": "PDF gerado com sucesso",
                "pdf_url": query.pdf.url
            })

        except models.Solicitacao.DoesNotExist:
            return http.JsonResponse({"error": "Solicitação não encontrada"}, status=404)

        except Exception as e:
            return http.JsonResponse({"error": f"Erro inesperado: {str(e)}"}, status=500)


class MenuHistorico(list.ListView):
    template_name = "menu_historico.html"
    context_object_name = "contratos"
    model = models.Solicitacao
