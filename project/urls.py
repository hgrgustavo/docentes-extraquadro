from django.urls import path, include
from website import views


urlpatterns = [
    path("", views.MenuInicio.as_view(), name="menuiniciopage"),
    path("login/", views.LoginView.as_view(), name="loginpage"),

    path("menu/", include([
        path("criar-professor/", views.MenuCriarProfessor.as_view(),
             name="menucriarprofessorpage"),
        path("listar-professor", views.MenuListarProfessor.as_view(),
             name="menulistarprofessorpage"),

        path("contratos/", include([
            path("gerar-contrato/", views.MenuGerarContrato.as_view(),
                 name="menugerarcontratopage"),

            path("gerar-contrato/pdf/",
                 views.GeneratePDF.as_view(), name="gerarpdf"),

            path("historico/", views.MenuHistorico.as_view(),
                 name="menuhistoricopage"),
            path("historico/excluir/<int:pk>/",
                 views.DeleteContratos.as_view(), name="deletecontrato")
        ]))
    ])),
]
