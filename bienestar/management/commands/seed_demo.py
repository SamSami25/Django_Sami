from django.core.management.base import BaseCommand
from bienestar.models import Pregunta, Opcion, Categoria, Audiencia, TipBelleza, TipSeguridad, Afirmacion, Genero

class Command(BaseCommand):
    help = "Crea preguntas, opciones y tips de ejemplo"

    def handle(self, *args, **kwargs):
        # Limpieza ligera (no toques Envio)
        Opcion.objects.all().delete()
        Pregunta.objects.all().delete()
        TipBelleza.objects.all().delete()
        TipSeguridad.objects.all().delete()
        Afirmacion.objects.all().delete()

        def add_preg(texto, cat, aud=Audiencia.TODOS):
            p = Pregunta.objects.create(texto=texto, categoria=cat, audiencia=aud, activo=True)
            Opcion.objects.create(pregunta=p, texto="No", peso=0)
            Opcion.objects.create(pregunta=p, texto="A veces", peso=1)
            Opcion.objects.create(pregunta=p, texto="Sí", peso=2)
            return p

        # Preguntas comunes
        add_preg("Me siento segur@ al expresar mis ideas en público.", Categoria.CONFIANZA)
        add_preg("Escucho con atención y entiendo las emociones de otras personas.", Categoria.EMPATIA)
        add_preg("Me recupero rápido después de momentos difíciles.", Categoria.RESILIENCIA)
        add_preg("Mantengo la calma en situaciones de presión.", Categoria.CALMA)

        # Hombres
        add_preg("Me siento segur@ con mi estilo personal (barba, peinado, ropa).", Categoria.CONFIANZA, Audiencia.MASCULINO)
        add_preg("Ofrezco apoyo emocional a mis amigos varones sin prejuicios.", Categoria.EMPATIA, Audiencia.MASCULINO)

        # Mujeres
        add_preg("Me siento comod@ con mi rutina de cuidado personal (piel, cabello, maquillaje).", Categoria.CONFIANZA, Audiencia.FEMENINO)
        add_preg("Pido ayuda sin sentir culpa cuando la necesito.", Categoria.RESILIENCIA, Audiencia.FEMENINO)

        # Tips Belleza (null = ambos)
        TipBelleza.objects.bulk_create([
            TipBelleza(genero=None, texto="Hidrátate: 6–8 vasos de agua al día."),
            TipBelleza(genero=None, texto="Duerme 7–8 horas para una piel más fresca."),
            TipBelleza(genero=Genero.FEMENINO, texto="Protector solar + hidratante con tu tipo de piel."),
            TipBelleza(genero=Genero.MASCULINO, texto="Cuida la barba: lava y peina para un acabado limpio."),
            TipBelleza(genero=None, texto="Sonríe: es el mejor toque de belleza."),
        ])

        # Tips Seguridad
        TipSeguridad.objects.bulk_create([
            TipSeguridad(genero=None, texto="Comparte tu ubicación en tiempo real con alguien de confianza al regresar tarde."),
            TipSeguridad(genero=None, texto="Configura contactos de emergencia en el teléfono."),
            TipSeguridad(genero=Genero.FEMENINO, texto="Acuerda palabras clave con amigas/familia para pedir ayuda."),
            TipSeguridad(genero=Genero.MASCULINO, texto="Evita discusiones en la calle; prioriza tu seguridad."),
            TipSeguridad(genero=None, texto="Verifica rutas y transporte antes de salir."),
        ])

        # Afirmaciones
        Afirmacion.objects.bulk_create([
            Afirmacion(genero=None, texto="Soy suficiente tal como soy."),
            Afirmacion(genero=None, texto="Mi voz merece ser escuchada."),
            Afirmacion(genero=Genero.FEMENINO, texto="Soy fuerte y hermosa."),
            Afirmacion(genero=Genero.MASCULINO, texto="Soy valiente y capaz."),
            Afirmacion(genero=None, texto="Hoy doy mi mejor paso."),
            Afirmacion(genero=None, texto="Mi calma es mi poder."),
        ])

        self.stdout.write(self.style.SUCCESS("Datos de ejemplo creados."))
