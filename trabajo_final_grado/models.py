from django.db import models
from django.utils import timezone
# Create your models here.


class TrabajoFinalGrado(models.Model):

    estados_trabajo = (
        (1, 'Creado' ),
    )
    estados_tareas = (
        (1, 'No gestionado'),
        (2, 'Gestionado')
        )

    nombre_trabajo = models.CharField('Nombre de trabajo de grado', max_length = 2000)
    descripcion = models.TextField('Descripción')
    equipo_de_trabajo = models.TextField('Equipo de trabajo')
    fecha_creacion = models.DateTimeField('Fecha creación', null=True, blank=True)
    planteamiento_del_problema = models.TextField('Planteamiento del problema', blank=True, null=True)
    identificacion_del_problema = models.TextField('Identificación del problema', blank=True, null=True)
    antecedentes_del_problema = models.TextField('Antecedentes', blank=True, null=True)
    estado = models.PositiveSmallIntegerField('Estado', choices=estados_trabajo, default=1)
    estado_tarea_uno = models.PositiveSmallIntegerField('Estado gestión 1', choices=estados_tareas, default=1)
    fecha_gestion_tarea_uno = models.DateTimeField('Fecha gestión tarea 1', null=True, blank=True)
    

    def save(self, *args, **kwargs):
        if self.id:
            #trabajo_existente = TrabajoFinalGrado.objects.get(id=self.id)
            if self.planteamiento_del_problema and self.identificacion_del_problema and self.antecedentes_del_problema and self.estado_tarea_uno == 1:
                self.estado_tarea_uno = 2
                self.fecha_gestion_tarea_uno = timezone.now()
        else:
            self.fecha_creacion = timezone.now()
        return super().save(*args, **kwargs)
                
    class Meta:
        verbose_name = "Trabajo final de grado"
        verbose_name_plural = "Trabajos finales de grado"

    def __str__(self):
        return self.nombre_trabajo