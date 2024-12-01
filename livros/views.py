from livros.serializers import LivroSerializer
from rest_framework.views import APIView
from livros.models import Livro
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import json  # Para manipulação de JSON, se necessário


class LivroView(APIView):
    def get(self, request):
        queryset = Livro.objects.all().order_by('titulo')
        #livro_serializer = LivroSerializer()
        #print(livro_serializer.fields)
        # importante informar que o queryset terá mais
        # de 1 resultado usando many=True
        serializer = LivroSerializer(queryset, many=True)
        return Response(serializer.data)



class newLivroView(APIView):
    def post(self, request, *args, **kwargs):
        image = request.FILES.get('image')  # Obtém a imagem
        metadata = request.data.get('metadata')  # Obtém o metadata

        # Verifica se a imagem e o metadata foram enviados
        if image and metadata:
            # Você pode querer verificar o tipo de imagem, por exemplo, se for um arquivo de imagem válido
            if image.content_type.startswith('image/'):  # Verifica se é uma imagem
                return Response({
                    "message": "Upload successful!",
                    "image_name": image.name,
                    "metadata": metadata,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "message": "The uploaded file is not a valid image."
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "Missing image or metadata."
            }, status=status.HTTP_400_BAD_REQUEST)
