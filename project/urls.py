from django.urls import path, include, resolvers
from website import views
from website import models, time_sync

urlpatterns: list[resolvers.URLPattern | resolvers.URLResolver] = [
    path("", views.Index.as_view(), name="indexpage"),
    path("login/", views.Login.as_view(), name="loginpage"),
    path("menu/", include([
        path("home/", views.MenuHome.as_view(), name="menuhomepage"),

        path("criar-professor/", views.MenuCriarProfessor.as_view(),
             name="menucriarprofessorpage"),

        path("listar-professor/", views.MenuListarProfessor.as_view(extra_context={"contract_expiration_date": models.Contratos.objects.all().values(
                "prestador_id", "data_termino", "servico", "componentes", "modalidade", "id"), "today": time_sync.get_synced_date()}),
             name="menulistarprofessorpage"),

        path("listar-professor/upload/teacher_photo/<int:pk>/",
             views.UploadTeacherPhoto.as_view(), name="uploadteacherphoto"),

        path("listar-professor/download/<int:pk>/",
             views.DownloadContract.as_view()),

        path("contratos/", include([
            path("gerar-contrato/", views.MenuGenContract.as_view(),
                 name="menugerarcontratopage"),

            path("historico/", views.MenuHistory.as_view(),
                 name="menuhistoricopage"),

            path("historico/excluir/<int:pk>/",
                 views.DeleteContract.as_view(), name="deletecontract"),

            path("historico/download/<int:pk>/",
                 views.DownloadContract.as_view(), name="downloadcontract")
        ]))
    ])),
]
