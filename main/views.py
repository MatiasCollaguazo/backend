from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
import requests
import json
from datetime import datetime
from collections import defaultdict


@login_required
@permission_required('main.index_viewer', raise_exception=True)
def index(request):
    # Arme el endpoint del REST API
    current_url = request.build_absolute_uri()
    url = current_url + '/api/v1/landing'

    # Petición al REST API
    response_http = requests.get(url)
    response_dict = json.loads(response_http.content)

    print("Endpoint ", url)
    print("Response ", response_dict)

    # Respuestas totales
    total_responses = len(response_dict.keys())

    # Variables para primera, última y día con más respuestas
    first_responses = None
    last_response = None
    high_rate_responses = None

    # Diccionario para contar respuestas por día
    responses_by_day = defaultdict(int)

    # Procesar cada respuesta
    for key, record in response_dict.items():
        saved_time = record.get('saved')
        if not saved_time:
            continue

        # Convertir la fecha a un objeto datetime con manejo de errores
        dt = None
        try:
            # Normalizar el formato de la fecha
            normalized_time = saved_time.replace('a. m.', 'AM').replace('p. m.', 'PM')
            dt = datetime.strptime(normalized_time, '%d/%m/%Y, %I:%M:%S %p')
        except ValueError:
            print(f"Formato de fecha inválido: {saved_time}")
            continue


        # Actualizar primera respuesta
        if first_responses is None or dt < first_responses:
            first_responses = dt

        # Actualizar última respuesta
        if last_response is None or dt > last_response:
            last_response = dt

        # Contar respuestas por día
        day_key = dt.strftime('%d/%m/%Y')  # Formato: día/mes/año
        responses_by_day[day_key] += 1

    # Encontrar el día con más respuestas
    if responses_by_day:
        high_rate_responses = max(responses_by_day, key=responses_by_day.get)

    # Formatear fechas para mostrar en la plantilla
    first_responses_str = first_responses.strftime('%d/%m/%Y, %I:%M:%S %p') if first_responses else 'N/A'
    last_response_str = last_response.strftime('%d/%m/%Y, %I:%M:%S %p') if last_response else 'N/A'

    # Objeto con los datos a renderizar
    data = {
        'title': 'Landing - Dashboard',
        'total_responses': total_responses,
        'first_responses': first_responses_str,
        'last_responses': last_response_str,  # Cambiado a 'last_responses' para coincidir con la plantilla
        'high_rate_responses': high_rate_responses if high_rate_responses else 'N/A',
        'responses': list(response_dict.values()),
    }

    # Renderización en la plantilla
    return render(request, 'main/index.html', data)
