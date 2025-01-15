from django.shortcuts import render

# Create your views here.


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime

from firebase_admin import db

class LandingAPI(APIView):
    
    name = 'Landing API'

    # Coloque el nombre de su colección en el Realtime Database
    collection_name = 'coleccion'

    def get(self, request):

    # Referencia a la colección
        ref = db.reference(f'{self.collection_name}')
        
        # get: Obtiene todos los elementos de la colección
        data = ref.get()

        # Devuelve un arreglo JSON
        return Response(data, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        
        # Referencia a la colección
        ref = db.reference(f'{self.collection_name}')

        current_time  = datetime.now()
        custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
        request.data.update({"saved": custom_format })
        
        # push: Guarda el objeto en la colección
        new_resource = ref.push(request.data)
        
        # Devuelve el id del objeto guardado
        return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)
    



#Actividad en clase
class LandingAPIDetail(APIView):
    name = 'Landing Detail API'
    collection_name = 'coleccion'
    def get(self, request, pk):
        reference = db.reference(f'{self.collection_name}/{pk}')
        data = reference.get()

        #En caso de éxito, retornar el documento con el código de estado 200 OK.
        #Si no se encuentra el documento, retornar un mensaje de error con el código 404 Not Found.

        if data:
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)


    def put(self, request, pk):
        reference = db.reference(f'{self.collection_name}/{pk}')
        
        #Si el documento no se encuentra, retornar un mensaje de error con el código 404 Not Found.
        if not reference.get():
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
        data = request.data

        #Validar que el cuerpo de la solicitud (request.data) contenga los campos necesarios para la actualización.        
        if not isinstance(data, dict) or not data:
            return Response({"error": "Body has not the correct fields to be updated"}, status=status.HTTP_400_BAD_REQUEST)

        reference.update(data)
        #En caso de éxito, retornar un mensaje confirmando la actualización con el código de estado 200 OK.
        return Response({"message": "Document Updated"}, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        reference = db.reference(f'{self.collection_name}/{pk}')

        #En caso de éxito, retornar un mensaje confirmando la eliminación con el código de estado 204 No Content.
        #Si no se encuentra el documento, retornar un mensaje de error con el código 404 Not Found.

        if not reference.get():
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
        reference.delete()

        return Response({"message": "Document eliminated succesfully!"}, status=status.HTTP_200_OK)