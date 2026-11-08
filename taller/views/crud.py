from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.forms import ModelForm
from django.forms.models import modelform_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from taller.models import (
    Cliente, Vehiculo, Cita, Diagnostico,
    OrdenServicio, Repuesto, DetalleOrden
)


MODULOS = {
    "clientes": {
        "titulo": "Clientes",
        "modelo": Cliente,
        "descripcion": "Administra los clientes del taller."
    },
    "vehiculos": {
        "titulo": "Vehículos",
        "modelo": Vehiculo,
        "descripcion": "Registra y administra los vehículos."
    },
    "citas": {
        "titulo": "Citas",
        "modelo": Cita,
        "descripcion": "Programa y administra las citas."
    },
    "diagnosticos": {
        "titulo": "Diagnósticos",
        "modelo": Diagnostico,
        "descripcion": "Registra los diagnósticos mecánicos."
    },
    "ordenes": {
        "titulo": "Órdenes de servicio",
        "modelo": OrdenServicio,
        "descripcion": "Administra las órdenes de trabajo."
    },
    "repuestos": {
        "titulo": "Repuestos",
        "modelo": Repuesto,
        "descripcion": "Controla el inventario de repuestos."
    },
    "detalles": {
        "titulo": "Detalles de órdenes",
        "modelo": DetalleOrden,
        "descripcion": "Administra los repuestos utilizados en cada orden."
    },
}


class TallerModelForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        cliente = cleaned_data.get("cliente")
        vehiculo = cleaned_data.get("vehiculo")

        if cliente and vehiculo:
            if vehiculo.cliente_id != cliente.pk:
                self.add_error(
                    "vehiculo",
                    "El vehículo seleccionado no pertenece al cliente."
                )

        return cleaned_data


def obtener_modulo(slug):
    modulo = MODULOS.get(slug)
    if not modulo:
        from django.http import Http404
        raise Http404("El módulo solicitado no existe.")
    return modulo


@login_required
def crud_list(request, slug):
    config = obtener_modulo(slug)
    modelo = config["modelo"]

    objetos = modelo.objects.all().order_by("-pk")

    campos = [
        campo for campo in modelo._meta.fields
        if campo.concrete
        and not campo.many_to_many
        and not campo.primary_key
    ]

    consulta = request.GET.get("q", "").strip()
    if consulta:
        from django.db.models import Q

        busqueda = Q()
        for campo in campos:
            if campo.get_internal_type() in (
                "CharField", "TextField", "EmailField"
            ):
                busqueda |= Q(**{f"{campo.name}__icontains": consulta})

        if busqueda:
            objetos = objetos.filter(busqueda)

    filas = []
    for objeto in objetos[:200]:
        valores = []
        for campo in campos:
            valor = getattr(objeto, campo.name, "")
            valores.append(str(valor) if valor is not None else "—")
        filas.append({
            "objeto": objeto,
            "valores": valores,
        })

    return render(request, "taller/crud/list.html", {
        "config": config,
        "slug": slug,
        "campos": campos,
        "filas": filas,
        "consulta": consulta,
        "cantidad": objetos.count(),
    })


@login_required
def crud_create(request, slug):
    config = obtener_modulo(slug)
    modelo = config["modelo"]

    Formulario = modelform_factory(
        modelo,
        form=TallerModelForm,
        fields="__all__"
    )

    form = Formulario(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            f'{config["titulo"]}: registro creado correctamente.'
        )
        return redirect("crud_list", slug=slug)

    return render(request, "taller/crud/form.html", {
        "config": config,
        "slug": slug,
        "form": form,
        "accion": "Registrar",
    })


@login_required
def crud_edit(request, slug, pk):
    config = obtener_modulo(slug)
    objeto = get_object_or_404(config["modelo"], pk=pk)

    Formulario = modelform_factory(
        config["modelo"],
        form=TallerModelForm,
        fields="__all__"
    )

    form = Formulario(request.POST or None, instance=objeto)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            f'{config["titulo"]}: registro actualizado correctamente.'
        )
        return redirect("crud_list", slug=slug)

    return render(request, "taller/crud/form.html", {
        "config": config,
        "slug": slug,
        "form": form,
        "accion": "Guardar cambios",
    })


@login_required
def crud_delete(request, slug, pk):
    config = obtener_modulo(slug)
    objeto = get_object_or_404(config["modelo"], pk=pk)

    if request.method == "POST":
        try:
            objeto.delete()
            messages.success(request, "Registro eliminado correctamente.")
        except ProtectedError:
            messages.error(
                request,
                "No se puede eliminar porque este registro está relacionado "
                "con otros datos del sistema."
            )

        return redirect("crud_list", slug=slug)

    return render(request, "taller/crud/delete.html", {
        "config": config,
        "slug": slug,
        "objeto": objeto,
    })
