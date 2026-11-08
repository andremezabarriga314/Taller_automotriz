from django.contrib import admin
from django.urls import path, include

from taller.views.crud import (
    crud_list, crud_create, crud_edit, crud_delete
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("taller.urls")),
    path("<slug:slug>/", crud_list, name="crud_list"),
    path("<slug:slug>/nuevo/", crud_create, name="crud_create"),
    path("<slug:slug>/<int:pk>/editar/", crud_edit, name="crud_edit"),
    path("<slug:slug>/<int:pk>/eliminar/", crud_delete, name="crud_delete"),
]
