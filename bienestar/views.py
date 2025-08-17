from django.shortcuts import render, redirect
from django.http import HttpResponse
import xlsxwriter
import io
import random

# Datos de ejemplo para preguntas
preguntas = [
    "¿Te sientes seguro/a de ti mismo/a?",
    "¿Disfrutas de tu apariencia física?",
    "¿Sueles sonreír durante el día?",
    "¿Te sientes feliz con tu estilo personal?",
    "¿Te gusta aprender cosas nuevas?",
    "¿Te sientes relajado/a la mayor parte del tiempo?",
    "¿Te importa tu bienestar físico?",
    "¿Tienes confianza en tus decisiones?",
    "¿Sueles ayudar a los demás?",
    "¿Te sientes motivado/a para mejorar cada día?"
]

# Colores para el gráfico
colores_preguntas = ['#f472b6','#7c3aed','#3b82f6','#22c55e','#facc15','#f97316','#ef4444','#10b981','#8b5cf6','#f9a8d4']

# Lista para guardar resultados
resultados = []

def home(request):
    return render(request, 'home.html')

def iniciar_test(request):
    return render(request, 'iniciar.html', {'preguntas': preguntas})

def test(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        genero = request.POST.get('genero')
        puntaje_total = 0
        valores = []

        for i in range(10):
            resp = int(request.POST.get(f'pregunta{i+1}', 0))
            valores.append(resp)
            puntaje_total += resp

        porcentaje = round(puntaje_total / 40 * 100, 2)

        # Definir mensaje según porcentaje
        if porcentaje >= 75:
            mensaje = "¡Excelente! 😊 Estás muy bien."
        elif porcentaje >= 40:
            mensaje = "¡Bien! Mantén la calma y sigue adelante."
        else:
            mensaje = "¡Ánimo! 💪 Puedes mejorar, sigue intentándolo."

        # Guardar resultado
        resultados.append({
            'nombre': nombre,
            'genero': genero,
            'puntaje': puntaje_total,
            'porcentaje': porcentaje,
            'valores': valores
        })

        datos = {
            'labels': preguntas,
            'valores': valores,
            'colores': colores_preguntas
        }

        context = {
            'nombre': nombre,
            'genero': genero,
            'puntaje': puntaje_total,
            'porcentaje': porcentaje,
            'mensaje': mensaje,
            'datos': datos
        }

        return render(request, 'resultado.html', context)

    return redirect('home')


def exportar_excel(request):
    # Crear archivo Excel en memoria
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Resultados")

    # Formato de cabecera
    header_format = workbook.add_format({'bold': True, 'bg_color': '#fce7f3', 'border':1})

    headers = ['Nombre', 'Género', 'Puntaje', 'Porcentaje'] + preguntas
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header, header_format)

    # Escribir datos
    for row_num, r in enumerate(resultados, 1):
        worksheet.write(row_num, 0, r['nombre'])
        worksheet.write(row_num, 1, r['genero'])
        worksheet.write(row_num, 2, r['puntaje'])
        worksheet.write(row_num, 3, r['porcentaje'])
        for col_num, val in enumerate(r['valores']):
            worksheet.write(row_num, col_num + 4, val)

    workbook.close()
    output.seek(0)

    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename=resultados.xlsx'
    return response
