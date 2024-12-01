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
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        titulo = request.data.get('titulo')
        autor = request.data.get('autor')
        capa = request.FILES.get('capa')  # Para arquivos
        categoria = request.data.get('categoria')
        sinopse = request.data.get('sinopse')

        # Verifique se os dados estão presentes
        if titulo and autor and categoria:
            # Salvar no banco de dados (ajuste para seu modelo)
            livro = Livro.objects.create(
                titulo=titulo,
                autor=autor,
                categoria=categoria,
                sinopse=sinopse,
                capa=capa,
            )
            return Response({'message': 'Livro criado com sucesso!'}, status=201)
        else:
            return Response({'error': 'Dados incompletos.'}, status=400)

