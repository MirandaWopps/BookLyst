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
    
    def delete(self, request):
        id_erro = ""
        erro = False

        for id in request.data:  # Espera-se que request.data seja uma lista de IDs
            try:
                livro = Livro.objects.get(id=id)
                livro.delete()
            except Livro.DoesNotExist:  # Captura caso o ID não exista
                id_erro += f"{id} "
                erro = True

        if erro:
            return Response(
                {'error': f'Os seguintes itens não foram encontrados: [{id_erro.strip()}]'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(status=status.HTTP_204_NO_CONTENT)



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




class upLivroView(APIView):
    # Método GET para recuperar o livro baseado no ID
    def get(self, request, id_arg):
        livro = self.get_book_by_id(id_arg)
        if livro:
            serializer = LivroSerializer(livro)
            return Response(serializer.data)  # Retorna os dados do livro serializados
        else:
            # Caso o livro não seja encontrado, retorna erro 404
            return Response({
                'msg': f'Livro com id #{id_arg} não existe'
            }, status=status.HTTP_404_NOT_FOUND)

    # Método PUT para atualizar os dados de um livro
    def put(self, request, id_arg):
        livro = self.get_book_by_id(id_arg)
        if livro:
            serializer = LivroSerializer(livro, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()  # Salva os dados atualizados no banco
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Caso o livro não seja encontrado, retorna erro 404
            print(serializer.errors)
            return Response({
                'msg': f'Livro com id #{id_arg} não existe'
            }, status=status.HTTP_404_NOT_FOUND)

    # Função para buscar o livro pelo ID
    def get_book_by_id(self, id_arg):
        try:
            return Livro.objects.get(id=id_arg)
        except Livro.DoesNotExist:
            return None
