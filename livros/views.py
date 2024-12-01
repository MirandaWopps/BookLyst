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
    def POST(self, request, *args, **kwargs):
        image = request.FILES.get('image')
        metadata = request.data.get('metadata')

        if image and metadata:
            return Response({
                "message": "Upload successful!",
                "image_name": image.name,
                "metadata": metadata,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "message": "Missing image or metadata."
            }, status=status.HTTP_400_BAD_REQUEST)
