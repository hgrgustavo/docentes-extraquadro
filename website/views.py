import io
from typing import Any, override
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from . import models, forms, storages
from weasyprint import HTML
from django.core.files.base import ContentFile
from django import http
from django.template import loader
from django.views.generic.base import TemplateView, View, ContextMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from .backends import CustomAuthentication
from abc import ABC, abstractmethod
from django.forms import BaseModelForm


class UserDataStrategy(ABC):
    @abstractmethod
    def get_user_data(self, request: http.HttpRequest) -> Any:
        pass

class SessionUserDataStrategy(UserDataStrategy):
    @override
    def get_user_data(self, request: http.HttpRequest) -> models.Usuario | None:
        email = request.session.get("email")        
        return models.Usuario.objects.filter(email=email).first() if email else None

class QueryUserDataStrategy(UserDataStrategy):
    @override
    def get_user_data(self, request: http.HttpRequest) -> models.Usuario | None: # type: ignore
        email = getattr(request.user, "email", None)
        return models.Usuario.objects.filter(email=email).first()

class UserDataMixin(ContextMixin):
    strategy: UserDataStrategy

    def set_strategy(self, request: http.HttpRequest, strategy: UserDataStrategy):
        self.request = request
        self.strategy = strategy

    @override
    def get_context_data(self, **kwargs: Any) -> Any:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        
        current_user = self.strategy.get_user_data(self.request)

        if current_user:
            context["user_name"] = current_user.nome
            context["user_email"] = current_user.email
   
        return context

class Index(TemplateView):
    template_name = "index.html"

class Login(TemplateView):
    template_name = "login.html"
    form_class = forms.LoginForm

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.LoginForm
        
        return context

    def post(self, request: http.HttpRequest) -> http.HttpResponse:
        email: str = str(request.POST.get("email"))
        password: str = str(request.POST.get("password"))
        
        user_query: models.Usuario | None = CustomAuthentication.authenticate(request=request, email=email, password=password)

        if user_query is not None:
            login(request=request, user=user_query)
            request.session["email"] = email
            return redirect("menuhomepage")
            
        return http.JsonResponse({"message": "forbidden"}, status=403)

@method_decorator(login_required(login_url=settings.LOGIN_URL), name='dispatch')
class MenuHome(UserDataMixin, ListView):
    template_name = "menu_home.html"
    model = models.Usuario
    context_object_name = "usuario"

    def get(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> http.HttpResponse:
        self.set_strategy(self.request, SessionUserDataStrategy())
        return super().get(request, *args, **kwargs)

@method_decorator(login_required(login_url=settings.LOGIN_URL), name='dispatch')
class MenuCriarProfessor(UserDataMixin, CreateView):
    template_name = "menu_criarprofessor.html"
    model = models.Professor
    form_class = forms.CriarProfessorForm
    success_url = "#"

    def get(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> http.HttpResponse:
        self.set_strategy(self.request, SessionUserDataStrategy())
        return super().get(request, *args, **kwargs)

@method_decorator(login_required(login_url=settings.LOGIN_URL), name='dispatch')
class MenuListarProfessor(UserDataMixin, ListView):
    template_name = "menu_listarprofessor.html"
    model = models.Professor
    context_object_name = "professor"

    def get(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> http.HttpResponse:
        self.set_strategy(self.request, SessionUserDataStrategy())
        return super().get(request, *args, **kwargs)


@method_decorator(login_required(login_url=settings.LOGIN_URL), name='dispatch')
class MenuGenContract(UserDataMixin, CreateView):
    template_name = "menu_gerarcontrato.html"
    model = models.Contratos
    form_class = forms.GerarContratoForm

    def get(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> http.HttpResponse:
        self.set_strategy(self.request, SessionUserDataStrategy())
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm):
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

        


@method_decorator(login_required(login_url=settings.LOGIN_URL), name='dispatch')
class GeneratePDF(View):
    def render_to_pdf(self, html_src: str, context_dict: dict[str, Any]) -> io.BytesIO:
        template = loader.get_template(html_src)
        html = template.render(context_dict)
        buffer = io.BytesIO()

        HTML(string=html).write_pdf(buffer) # type: ignore

        buffer.seek(0)

        return buffer


@method_decorator(login_required(login_url=settings.LOGIN_URL), name='dispatch')
class MenuHistory(UserDataMixin, ListView):
    template_name = "menu_historico.html"
    context_object_name = "contratos"
    model = models.Contratos

    def get(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> http.HttpResponse:
        self.set_strategy(self.request, SessionUserDataStrategy())
        return super().get(request, *args, **kwargs)


@method_decorator(login_required(login_url=settings.LOGIN_URL), name='dispatch')
class DeleteContract(DeleteView):
    model = models.Contratos

    def delete(self, request: http.HttpRequest, *args: Any, **kwargs: Any):
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


@method_decorator(login_required(login_url=settings.LOGIN_URL), name='dispatch')
class DownloadContract(View):
    def post(self, request: http.HttpRequest, **kwargs: Any):
        contract_id = kwargs.get("pk")

        try:
            get_object_or_404 (
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


@method_decorator(login_required(login_url=settings.LOGIN_URL), name='dispatch')
class UploadTeacherPhoto(View):
    model = models.Professor

    def post(self, request: http.HttpRequest, pk: int):
        try:
            models.Professor.objects.get(
                pk=pk)

            buffer = io.BytesIO()

            for _, file in request.FILES.items():
                buffer.write(b"".join(file.chunks(chunk_size=1024**2)))

            buffer.seek(0)

            file_name: str = f"teacher_{pk}_photo.{
                request.FILES["file"].name.split('.')[-1]}"  # type: ignore

            storages.GoogleDriveStorage().upload(ContentFile(buffer.read()), file_name)

            buffer.close()

            file_url = storages.GoogleDriveStorage().get_drivefile_url(file_name)

            return http.JsonResponse({"status": "success", "photo_url": file_url})

        except models.Professor.DoesNotExist:
            return http.JsonResponse({"status": "error", "message": "Teacher not found!"}, status=404)
