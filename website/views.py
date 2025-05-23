import io
import ntplib
from datetime import datetime
from . import models, forms, storages
from weasyprint import HTML
from django.core.files.base import ContentFile
from django.contrib import auth
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

            context["user_name"] = user.nome
            context["user_email"] = user.email

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

            context["user_name"] = user.nome
            context["user_email"] = user.email

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
            contract = models.Contratos.objects.all()

            # data de hoje
            try:
                ntp_client = ntplib.NTPClient()
                ntp_response = ntp_client.request(
                    host="pool.ntp.org", version=3)
                today = datetime.utcfromtimestamp(ntp_response.tx_time).date()

            except Exception as e:
                print("Error obtaining ntp data, because ", e)
                today = datetime.now().strftime("%Y-%m-%d")

            context["user_name"] = user.nome
            context["user_email"] = user.email
            context["contract_expiration_date"] = contract.values(
                "prestador_id", "data_termino", "servico", "componentes", "modalidade", "id")
            context["today"] = today

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
                file_name = f"contract_{contrato.id}.pdf"

                storages.GoogleDriveStorage().upload(file_content, file_name)

                pdf_buffer.close()

            return http.HttpResponseRedirect(self.request.path)

        except Exception as e:
            return http.JsonResponse(
                {
                    "message": f"Erro inesperado: {str(e)}"
                },
                status=500
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            user = models.Usuario.objects.get(pk=1)

            context["user_name"] = user.nome
            context["user_email"] = user.email

        except models.Usuario.DoesNotExist:
            context["user_nome"] = None

        return context


class GeneratePDF(base.View):
    def render_to_pdf(self, html_src, context_dict):
        try:
            template = loader.get_template(html_src)
            html = template.render(context_dict)
            buffer = io.BytesIO()

            HTML(
                string=html).write_pdf(buffer)

            buffer.seek(0)

            return buffer

        except Exception as e:
            print(f"Error rendering PDF: {str(e)}")

            if buffer:
                buffer.close()

            return None


class MenuHistory(list.ListView):
    template_name = "menu_historico.html"
    context_object_name = "contratos"
    model = models.Contratos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = models.Usuario.objects.get(pk=1)

        # data de hoje
        try:
            ntp_client = ntplib.NTPClient()
            ntp_response = ntp_client.request(
                host="pool.ntp.org", version=3)
            today = datetime.utcfromtimestamp(ntp_response.tx_time).date()

        except Exception as e:
            print("Error obtaining ntp data, because ", e)
            today = datetime.now().strftime("%Y-%m-%d")

        context["user_name"] = user.nome
        context["user_email"] = user.email

        context["today"] = today

        return context


class DeleteContract(edit.DeleteView):
    model = models.Contratos

    def delete(self, request, **kwargs):
        try:
            contract_id = kwargs.get("pk")

            if contract_id:
                self.get_object().delete()
                storages.GoogleDriveStorage().delete(contract_id)

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

        except Exception:
            return http.JsonResponse(
                {
                    "message": "error",
                    "cause": "Failed to delete file on Google Drive"
                },
                status=500
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
                f"contract_{contract_id}.pdf"
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


class UploadTeacherPhoto(base.View):
    model = models.Professor

    def post(self, request, pk):
        try:
            models.Professor.objects.get(
                pk=pk)

            buffer = io.BytesIO()

            for _, file in request.FILES.items():
                buffer.write(b"".join(file.chunks(chunk_size=1024**2)))

            buffer.seek(0)

            file_name = f"teacher_{pk}_photo.{
                request.FILES["file"].name.split('.')[-1]}"

            storages.GoogleDriveStorage().upload(ContentFile(buffer.read()), file_name)

            buffer.close()

            file_url = storages.GoogleDriveStorage().get_drivefile_url(file_name)

            return http.JsonResponse({"status": "success", "photo_url": file_url})

        except models.Professor.DoesNotExist:
            return http.JsonResponse({"status": "error", "message": "Teacher not found!"}, status=404)
