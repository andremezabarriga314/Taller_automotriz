from django.db import models


class Vehiculo(models.Model):
    cliente = models.ForeignKey(
        "taller.Cliente",
        on_delete=models.PROTECT,
        related_name="vehiculos"
    )
    placa = models.CharField(max_length=15, unique=True)
    marca = models.CharField(max_length=60)
    modelo = models.CharField(max_length=60)
    anio = models.PositiveSmallIntegerField(null=True, blank=True)
    color = models.CharField(max_length=40, blank=True)
    vin = models.CharField(max_length=40, unique=True, null=True, blank=True)
    kilometraje = models.PositiveIntegerField(default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["placa"]
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"
