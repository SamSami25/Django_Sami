from django.shortcuts import render
from django.http import HttpResponse
import xlsxwriter
from io import BytesIO

def test(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        genero = request.POST.get("genero")
        # Recoger respuestas de las 10 preguntas
        respuestas = []
        for i in range(1, 11):
            valor = int(request.POST.get(f"pregunta{i}", 0))
            respuestas.append(valor)
        
        promedio = sum(respuestas) / len(respuestas)

        # Mensajes motivacionales según el porcentaje
        if promedio <= 1.5:
            mensaje = "¡Ánimo! Puedes mejorar, respira y sigue adelante 💪"
        elif promedio <= 3:
            mensaje = "¡Muy bien! Continúa así y respira con tranquilidad 🙂"
        else:
            mensaje = "¡Excelente! Estás muy bien 👏"

        # Datos para gráfica
        datos = {
            "labels": [f"Pregunta {i}" for i in range(1, 11)],
            "valores": respuestas,
            "colores": ['#f99','#9f9','#99f','#ff9','#f9f','#9ff','#fc9','#c9f','#9fc','#ffc']
        }

        request.session['resultado'] = {
            "nombre": nombre,
            "genero": genero,
            "respuestas": respuestas,
            "promedio": promedio,
            "mensaje": mensaje
        }

        return render(request, "resultado.html", {"datos": datos, "mensaje": mensaje, "promedio": promedio})

    return render(request, "test.html")


def exportar_excel(request):
    resultado = request.session.get('resultado')
    if not resultado:
        return HttpResponse("No hay resultados para exportar.")

    # Crear archivo Excel en memoria
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Resultados")

    # Formatos
    bold = workbook.add_format({'bold': True})
    center = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

    # Cabecera
    worksheet.write('A1', 'Nombre', bold)
    worksheet.write('B1', 'Género', bold)
    worksheet.write('C1', 'Pregunta', bold)
    worksheet.write('D1', 'Respuesta', bold)

    # Escribir datos
    fila = 1
    nombre = resultado['nombre']
    genero = resultado['genero']
    for i, resp in enumerate(resultado['respuestas'], start=1):
        worksheet.write(fila, 0, nombre)
        worksheet.write(fila, 1, genero)
        worksheet.write(fila, 2, f"Pregunta {i}")
        worksheet.write(fila, 3, resp, center)
        fila += 1

    # Promedio
    worksheet.write(fila, 2, "Promedio", bold)
    worksheet.write_formula(fila, 3, f"=AVERAGE(D2:D{fila})")

    workbook.close()
    output.seek(0)

    response = HttpResponse(
        output.read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename=resultado.xlsx'
    return response
