from django.urls import path
from taller.views.web import (
    iniciar_sesion, registro, cerrar_sesion, dashboard, modulo
)

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("login/", iniciar_sesion, name="login"),
    path("registro/", registro, name="registro"),
    path("logout/", cerrar_sesion, name="logout"),
    path("modulo/<slug:slug>/", modulo, name="modulo"),
]
