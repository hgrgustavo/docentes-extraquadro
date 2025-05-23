from django.urls import path, include
from website import views


urlpatterns = [
    path("", views.MenuInicio.as_view(), name="menuiniciopage"),
    path("login/", views.LoginView.as_view(), name="loginpage"),
    path("menu/", include([
        path("criar-professor/", views.MenuCriarProfessor.as_view(),
             name="menucriarprofessorpage"),

        path("listar-professor/", views.MenuListarProfessor.as_view(),
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
