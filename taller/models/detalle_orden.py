from django.db import models
from decimal import Decimal


class DetalleOrden(models.Model):
    orden = models.ForeignKey(
        "taller.OrdenServicio",
        on_delete=models.CASCADE,
        related_name="detalles"
    )
    repuesto = models.ForeignKey(
        "taller.Repuesto",
        on_delete=models.PROTECT,
        related_name="detalles_orden"
    )
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Detalle de orden"
        verbose_name_plural = "Detalles de orden"
        constraints = [
            models.UniqueConstraint(
                fields=["orden", "repuesto"],
                name="unique_repuesto_por_orden"
            )
        ]

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.repuesto.nombre} x {self.cantidad}"
