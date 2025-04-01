from django.urls import path, include
from website import views


urlpatterns = [
    path("", views.Index.as_view(), name="loginpage"),

    path("menu/", include([
        path("inicio/", views.MenuInicio.as_view(), name="menuiniciopage"),
        path("criar-professor/", views.MenuCriarProfessor.as_view(),
             name="menucriarprofessorpage"),
        path("listar-professor", views.MenuListarProfessor.as_view(),
             name="menulistarprofessorpage"),

        path("contratos/", include([
            path("gerar-contrato/", views.MenuGerarContrato.as_view(),
                 name="menugerarcontratopage"),
            path("gerar-contrato/<int:pk>/",
                 views.GeneratePDF.as_view(), name="gerarcontrato"),
            path("historico/", views.MenuHistorico.as_view(),
                 name="menuhistoricopage"),
        ]))
    ])),
]
