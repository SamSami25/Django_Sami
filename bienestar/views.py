from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from .forms import InicioForm, PreguntasForm
from .models import Genero, Pregunta, Opcion, Envio, TipBelleza, TipSeguridad, Afirmacion, Categoria, Audiencia

def home(request):
    return render(request, "home.html")

def iniciar_test(request):
    if request.method == "POST":
        form = InicioForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            genero = form.cleaned_data["genero"]
            # Pasamos por querystring a la vista del test
            return redirect(f"{reverse('test')}?nombre={nombre}&genero={genero}")
    else:
        form = InicioForm()
    return render(request, "iniciar.html", {"form": form})

def test(request):
    nombre = request.GET.get("nombre")
    genero = request.GET.get("genero")
    if not nombre or genero not in dict(Genero.choices):
        return redirect("iniciar")

    if request.method == "POST":
        form = PreguntasForm(genero, data=request.POST)
        if form.is_valid():
            # Calcular puntajes
            puntajes = {
                Categoria.CONFIANZA: 0,
                Categoria.EMPATIA: 0,
                Categoria.RESILIENCIA: 0,
                Categoria.CALMA: 0,
            }
            respuestas = {}
            for key, value in form.cleaned_data.items():
                if key.startswith("q_"):
                    opcion = Opcion.objects.select_related("pregunta").get(id=int(value))
                    cat = opcion.pregunta.categoria
                    puntajes[cat] += opcion.peso
                    respuestas[str(opcion.pregunta.id)] = int(value)

            # Determinar categoría top
            categoria_top = max(puntajes, key=puntajes.get)

            envio = Envio.objects.create(
                nombre=nombre,
                genero=genero,
                punt_confianza=puntajes[Categoria.CONFIANZA],
                punt_empatia=puntajes[Categoria.EMPATIA],
                punt_resiliencia=puntajes[Categoria.RESILIENCIA],
                punt_calma=puntajes[Categoria.CALMA],
                categoria_top=categoria_top,
                respuestas=respuestas,
            )

            # Tips y afirmaciones (genero o para ambos [None])
            tips_b = TipBelleza.objects.filter(Q(genero=genero) | Q(genero__isnull=True))[:5]
            tips_s = TipSeguridad.objects.filter(Q(genero=genero) | Q(genero__isnull=True))[:5]
            afirm = Afirmacion.objects.filter(Q(genero=genero) | Q(genero__isnull=True)).order_by('?')[:5]

            contexto = {
                "envio": envio,
                "nombre": nombre,
                "genero": dict(Genero.choices)[genero],
                "puntajes": puntajes,
                "categoria_top": dict(Categoria.choices)[categoria_top],
                "tips_belleza": tips_b,
                "tips_seguridad": tips_s,
                "afirmaciones": afirm,
            }
            return render(request, "resultado.html", contexto)
    else:
        form = PreguntasForm(genero)

    return render(request, "test.html", {"form": form, "nombre": nombre})
