from . import models, forms, storages

from xhtml2pdf import pisa

import io

from django.core.files.base import ContentFile
from django.contrib import auth
from django.db.models import Sum
from django import http, shortcuts
from django.template import loader
from django.views.generic import base, edit, list


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = models.Usuario.objects.get(pk=1)
            teacher = models.Professor.objects.all()

            context["user_name"] = user.nome
            context["user_email"] = user.email

            context["last_record"] = teacher.order_by("-id").first().id
            context["teacher_cpf_percentage"] = round((teacher.filter(
                pf_ou_pj="PF").count() / teacher.count()) * 100)

            context["teacher_cnpj_percentage"] = round((teacher.filter(
                pf_ou_pj="PJ").count() / teacher.count()) * 100)

        except models.Usuario.DoesNotExist:
            context["user_nome"] = None

        return context


class MenuListarProfessor(list.ListView):
    template_name = "menu_listarprofessor.html"
    model = models.Professor
    context_object_name = "professor"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = models.Usuario.objects.get(pk=1)
            teacher = models.Professor.objects.all()

            context["user_name"] = user.nome
            context["user_email"] = user.email

            context["last_record"] = teacher.order_by("-id").first().id
            context["teacher_cpf_percentage"] = round((teacher.filter(
                pf_ou_pj="PF").count() / teacher.count()) * 100)

            context["teacher_cnpj_percentage"] = round((teacher.filter(
                pf_ou_pj="PJ").count() / teacher.count()) * 100)

        except models.Usuario.DoesNotExist:
            context["user_nome"] = None

        return context


class MenuGenContract(edit.CreateView):
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
                file_content = ContentFile(pdf_buffer.read())
                file_name = f"contrato_{contrato.id}.pdf"

                """
                (Uncomment this and pdf field on models if you wanna save
                .pdfs in the server.)

                contrato.pdf.save(
                    file_content,
                    file_name
                )
                """

                storages.GoogleDriveStorage().save(file_content, file_name)

            pdf_buffer.close()

            return http.JsonResponse(  # async
                {
                    "message": "PDF gerado com sucesso",
                    "contrato_id": contrato.id,
                    "public_url": storages.GoogleDriveStorage.url(self, file_name)
                }
            )

        except Exception as e:
            return http.JsonResponse(
                {"message": f"Erro inesperado: {str(e)}"},
                status=500
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            user = models.Usuario.objects.get(pk=1)
            contract = models.Contratos.objects.all()

            aggregate_data = contract.aggregate(
                sum_carga_horaria=Sum("carga_horaria"),
                sum_valor_hora_aula=Sum("valor_hora_aula")
            )

            sum_carga_horaria = aggregate_data["sum_carga_horaria"] or 0
            sum_valor_hora_aula = aggregate_data["sum_valor_hora_aula"] or 0

            context["user_name"] = user.nome
            context["user_email"] = user.email
            context["total_cost"] = sum_carga_horaria * sum_valor_hora_aula

        except models.Usuario.DoesNotExist:
            context["user_nome"] = None

        return context


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


class MenuHistory(list.ListView):
    template_name = "menu_historico.html"
    context_object_name = "contratos"
    model = models.Contratos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = models.Usuario.objects.get(pk=1)
            contract = models.Contratos.objects.all()

            aggregate_data = contract.aggregate(
                sum_carga_horaria=Sum("carga_horaria"),
                sum_valor_hora_aula=Sum("valor_hora_aula")
            )

            sum_carga_horaria = aggregate_data["sum_carga_horaria"] or 0
            sum_valor_hora_aula = aggregate_data["sum_valor_hora_aula"] or 0

            context["user_name"] = user.nome
            context["user_email"] = user.email
            context["total_cost"] = sum_carga_horaria * sum_valor_hora_aula

        except models.Usuario.DoesNotExist:
            context["user_nome"] = None

        return context


class DeleteContract(edit.DeleteView):
    model = models.Contratos

    def delete(self, request, **kwargs):
        try:
            self.get_object().delete()
            return http.JsonResponse(
                {
                    "message": "success"
                },
                status=200
            )

        except models.Contratos.DoesNotExist:
            return http.JsonResponse(
                {
                    "message": "error",
                    "cause": "Item not found"
                },
                status=404
            )


class DownloadContract(base.View):
    def post(self, request, **kwargs):
        contract_id = kwargs.get("pk")

        try:
            shortcuts.get_object_or_404(
                models.Contratos,
                id=contract_id
            )

            download_link = storages.GoogleDriveStorage().get_download_link(
                contract_id
            )

            if not download_link:
                return http.JsonResponse(
                    {
                        "message": "error",
                        "cause": "Link not found"

                    },
                    status=400
                )

            return http.JsonResponse(
                {
                    "message": "success",
                    "link": download_link,
                },
                status=200
            )

        except http.Http404:
            return http.JsonResponse(
                {
                    "message": "error",
                    "cause": "Item not found",
                },
                status=404
            )
