from django.shortcuts import render
import openpyxl
import os

# Guardar resultados en Excel
def guardar_resultado_excel(nombre, genero, puntaje, porcentaje):
    archivo = "resultados.xlsx"
    if not os.path.exists(archivo):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["Nombre", "Género", "Puntaje", "Porcentaje"])
        wb.save(archivo)

    wb = openpyxl.load_workbook(archivo)
    ws = wb.active
    ws.append([nombre, genero, puntaje, f"{porcentaje}%"])
    wb.save(archivo)

# Vista del test
def test(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "Invitado")
        genero = request.POST.get("genero", "No definido")
        
        # Preguntas del test: 10 preguntas
        preguntas = [int(request.POST.get(f"q{i}", 0)) for i in range(1, 11)]
        
        puntaje = sum(preguntas)
        porcentaje = int((puntaje / 40) * 100)  # 10 preguntas, max 4 cada una

        # Mensaje motivacional según porcentaje
        if porcentaje < 40:
            mensaje = "¡Ánimo! 🌸 Recuerda que cada día es una nueva oportunidad para brillar. Respira profundo y sonríe."
        elif 40 <= porcentaje < 70:
            mensaje = "¡Vas muy bien! 😊 Sigue cuidándote y disfrutando cada momento de tu bienestar."
        else:
            mensaje = "¡Excelente! 🌟 Tu bienestar está en un nivel alto, sigue así y comparte tu alegría."

        # Guardar en Excel
        guardar_resultado_excel(nombre, genero, puntaje, porcentaje)

        # Datos para la gráfica
        datos_grafica = {
            "labels": [f"Q{i}" for i in range(1, 11)],
            "valores": preguntas,
            "colores": []
        }

        # Colores según puntaje individual
        for valor in preguntas:
            if valor <= 1:
                datos_grafica["colores"].append("#f87171")  # rojo bajo
            elif valor <= 3:
                datos_grafica["colores"].append("#facc15")  # amarillo medio
            else:
                datos_grafica["colores"].append("#4ade80")  # verde alto

        return render(request, "resultado.html", {
            "nombre": nombre,
            "genero": genero,
            "puntaje": puntaje,
            "porcentaje": porcentaje,
            "mensaje": mensaje,
            "datos": datos_grafica
        })
    
    return render(request, "test.html")
