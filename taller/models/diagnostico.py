from django.conf import settings
from django.db import models


class Diagnostico(models.Model):
    cliente = models.ForeignKey(
        "taller.Cliente",
        on_delete=models.PROTECT,
        related_name="diagnosticos"
    )
    vehiculo = models.ForeignKey(
        "taller.Vehiculo",
        on_delete=models.PROTECT,
        related_name="diagnosticos"
    )
    mecanico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="diagnosticos"
    )
    fecha = models.DateTimeField(auto_now_add=True)
    sintomas = models.TextField()
    hallazgos = models.TextField(blank=True)
    resultado = models.TextField()
    recomendaciones = models.TextField(blank=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Diagnóstico"
        verbose_name_plural = "Diagnósticos"

    def __str__(self):
        return f"Diagnóstico #{self.id} - {self.vehiculo.placa}"
