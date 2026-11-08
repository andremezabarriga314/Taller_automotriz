from django.conf import settings
from django.db import models
from decimal import Decimal


class OrdenServicio(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        EN_PROCESO = "EN_PROCESO", "En proceso"
        FINALIZADA = "FINALIZADA", "Finalizada"
        ENTREGADA = "ENTREGADA", "Entregada"
        CANCELADA = "CANCELADA", "Cancelada"

    numero = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(
        "taller.Cliente",
        on_delete=models.PROTECT,
        related_name="ordenes"
    )
    vehiculo = models.ForeignKey(
        "taller.Vehiculo",
        on_delete=models.PROTECT,
        related_name="ordenes"
    )
    mecanico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ordenes_servicio"
    )
    diagnostico = models.ForeignKey(
        "taller.Diagnostico",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ordenes"
    )
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=15,
        choices=Estado.choices,
        default=Estado.PENDIENTE
    )
    descripcion_trabajo = models.TextField()
    costo_mano_obra = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    descuento = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ["-fecha_ingreso"]
        verbose_name = "Orden de servicio"
        verbose_name_plural = "Órdenes de servicio"

    @property
    def total_repuestos(self):
        return sum(
            (detalle.subtotal for detalle in self.detalles.all()),
            Decimal("0.00")
        )

    @property
    def total(self):
        return self.costo_mano_obra + self.total_repuestos - self.descuento

    def __str__(self):
        return self.numero
