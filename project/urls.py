from django.urls import path
from website import views


urlpatterns = [
    path("", views.Index.as_view(), name="loginpage"),

    path("menu/inicio/", views.MenuInicio.as_view(), name="menuiniciopage"),

    path("menu/criar-professor/", views.MenuCriarProfessor.as_view(),
         name="menucriarprofessorpage"),

    path("menu/listar-professor/", views.MenuListarProfessor.as_view(),
         name="menulistarprofessor"),

    path("menu/contratos/gerar-contrato/",
         views.MenuGerarContrato.as_view(), name="menugerarcontratopage"),





]
