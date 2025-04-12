from django.views.generic import base, edit, list
from . import models, forms
from django import http
from django.template import loader
from xhtml2pdf import pisa
import io
from django.core.files.base import ContentFile
from django.contrib import auth


class LoginView(edit.FormView):
    template_name = "login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = auth.authenticate(
            self.request, username=username, password=password)

        if user is not None:
            auth.login(self.request, user)

            return http.HttpResponseRedirect(self.success_url)
        else:
            form.add_error(None, "Usuário ou senha inválidos")
            return super().form_invalid(form)


class MenuInicio(list.ListView):
    template_name = "menu_inicio.html"
    model = models.Usuario
    context_object_name = "usuario"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = models.Usuario.objects.get(pk=1)
            teacher = models.Professor.objects.all()
            contract = models.Contratos.objects.all()

            context["user_name"] = user.nome
            context["user_email"] = user.email
            context["teacher_quantity"] = teacher.count()
            context["contract_quantity"] = contract.count()

        except models.Usuario.DoesNotExist:
            context["user_nome"] = None

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

        return context


class DeleteContratos(edit.DeleteView):
    model = models.Contratos

    def delete(self, request, **kwargs):
        try:
            self.get_object().delete()
            return http.JsonResponse(
                {
                    "status": "success"
                }
            )

        except models.Contratos.DoesNotExist:
            return http.JsonResponse(
                {
                    "status": "error",
                    "cause": "Item not found"
                }
            )
