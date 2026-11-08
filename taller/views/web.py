from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.http import Http404
from django.db.models import F

from taller.models import (
    Cliente, Vehiculo, Cita, Diagnostico,
    OrdenServicio, Repuesto, DetalleOrden
)


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        request.session.set_expiry(
            1209600 if request.POST.get("recordarme") else 0
        )
        return redirect("dashboard")

    return render(request, "registration/login.html", {"form": form})


def registro(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        usuario = form.save()
        login(request, usuario)
        return redirect("dashboard")

    return render(request, "registration/register.html", {"form": form})


@login_required
def cerrar_sesion(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return redirect("dashboard")


@login_required
def dashboard(request):
    contexto = {
        "total_clientes": Cliente.objects.count(),
        "total_vehiculos": Vehiculo.objects.count(),
        "total_citas": Cita.objects.count(),
        "total_diagnosticos": Diagnostico.objects.count(),
        "total_ordenes": OrdenServicio.objects.count(),
        "total_repuestos": Repuesto.objects.count(),
        "citas_recientes": Cita.objects.select_related(
            "cliente", "vehiculo"
        ).order_by("-fecha_hora")[:6],
        "ordenes_recientes": OrdenServicio.objects.select_related(
            "cliente", "vehiculo"
        ).order_by("-fecha_ingreso")[:6],
        "repuestos_bajos": Repuesto.objects.filter(
            activo=True, stock__lte=F("stock_minimo")
        )[:6],
    }
    return render(request, "taller/dashboard.html", contexto)


@login_required
def modulo(request, slug):
    modulos = {
        "clientes": ("Clientes", Cliente),
        "vehiculos": ("Vehículos", Vehiculo),
        "citas": ("Citas", Cita),
        "diagnosticos": ("Diagnósticos", Diagnostico),
        "ordenes": ("Órdenes de servicio", OrdenServicio),
        "repuestos": ("Repuestos", Repuesto),
        "reportes": ("Reportes", None),
    }

    if slug not in modulos:
        raise Http404("Módulo no encontrado")

    nombre, modelo = modulos[slug]
    cantidad = modelo.objects.count() if modelo else 0

    return render(request, "taller/module_placeholder.html", {
        "nombre_modulo": nombre,
        "cantidad": cantidad,
        "slug": slug,
    })
