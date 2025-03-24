from django.urls import path
from website import views


urlpatterns = [
    path("", views.Index.as_view(), name="loginpage"),

    path("menu/", views.Menu.as_view(), name="menupage"),
    path("menu/inicio/", views.MenuInicio.as_view(), name="menuiniciopage"),
    path("menu/criar-professor/", views.MenuCriarProfessor.as_view(),
         name="menucriarprofessorpage")



]
