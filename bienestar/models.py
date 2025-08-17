from django.db import models
from django.utils import timezone

class Genero(models.TextChoices):
    MASCULINO = 'M', 'Hombre'
    FEMENINO = 'F', 'Mujer'

class Categoria(models.TextChoices):
    CONFIANZA = 'CONF', 'Confianza'
    EMPATIA = 'EMPA', 'Empatía'
    RESILIENCIA = 'RESI', 'Resiliencia'
    CALMA = 'CALM', 'Calma'

class Audiencia(models.TextChoices):
    TODOS = 'ALL', 'Todos'
    MASCULINO = 'M', 'Solo hombres'
    FEMENINO = 'F', 'Solo mujeres'

class Pregunta(models.Model):
    texto = models.CharField(max_length=255)
    categoria = models.CharField(max_length=4, choices=Categoria.choices)
    audiencia = models.CharField(max_length=3, choices=Audiencia.choices, default=Audiencia.TODOS)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.texto

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='opciones')
    texto = models.CharField(max_length=255)
    peso = models.IntegerField(default=0)  # 0=No, 1=Tal vez, 2=Sí

    def __str__(self):
        return f"{self.pregunta.texto[:20]}... -> {self.texto} ({self.peso})"

class TipBelleza(models.Model):
    genero = models.CharField(max_length=1, choices=Genero.choices, null=True, blank=True)  # null=aplica a ambos
    texto = models.CharField(max_length=255)

    def __str__(self):
        g = dict(Genero.choices).get(self.genero, 'Ambos')
        return f"[{g}] {self.texto}"

class TipSeguridad(models.Model):
    genero = models.CharField(max_length=1, choices=Genero.choices, null=True, blank=True)
    texto = models.CharField(max_length=255)

    def __str__(self):
        g = dict(Genero.choices).get(self.genero, 'Ambos')
        return f"[{g}] {self.texto}"

class Afirmacion(models.Model):
    genero = models.CharField(max_length=1, choices=Genero.choices, null=True, blank=True)
    texto = models.CharField(max_length=255)

    def __str__(self):
        g = dict(Genero.choices).get(self.genero, 'Ambos')
        return f"[{g}] {self.texto}"

class Envio(models.Model):
    nombre = models.CharField(max_length=80)
    genero = models.CharField(max_length=1, choices=Genero.choices)
    creado = models.DateTimeField(default=timezone.now)
    punt_confianza = models.IntegerField(default=0)
    punt_empatia = models.IntegerField(default=0)
    punt_resiliencia = models.IntegerField(default=0)
    punt_calma = models.IntegerField(default=0)
    categoria_top = models.CharField(max_length=4, choices=Categoria.choices, blank=True)
    respuestas = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.get_categoria_top_display()} ({self.creado:%Y-%m-%d %H:%M})"
