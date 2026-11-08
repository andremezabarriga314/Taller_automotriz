from django.db import models


class Cita(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        CONFIRMADA = "CONFIRMADA", "Confirmada"
        ATENDIDA = "ATENDIDA", "Atendida"
        CANCELADA = "CANCELADA", "Cancelada"

    cliente = models.ForeignKey(
        "taller.Cliente",
        on_delete=models.PROTECT,
        related_name="citas"
    )
    vehiculo = models.ForeignKey(
        "taller.Vehiculo",
        on_delete=models.PROTECT,
        related_name="citas"
    )
    fecha_hora = models.DateTimeField()
    motivo = models.CharField(max_length=255)
    estado = models.CharField(
        max_length=15,
        choices=Estado.choices,
        default=Estado.PENDIENTE
    )
    observaciones = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_hora"]
        verbose_name = "Cita"
        verbose_name_plural = "Citas"

    def __str__(self):
        return f"Cita {self.id} - {self.vehiculo.placa}"
