from livros.serializers import LivroSerializer
from rest_framework.views import APIView
from livros.models import Livro
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class LivroView(APIView):
    """
    View para gerenciar os livros no sistema. Permite recuperar a lista de livros
    e deletar livros especificados pelos seus IDs.

    **Método GET**:
    **Método DELETE**:

    :param request: Objeto `request` com a lista de IDs dos livros a serem deletados.
    :return: Resposta indicando sucesso ou falha, incluindo IDs não encontrados.
    """
    def get(self, request):
        """
        Método GET que Recupera a lista de todos os livros ordenados por título e 
        retorna os dados dos livros no formato JSON.
        
        :param request: Objeto `request` que contém a requisição HTTP.
        :return: Resposta JSON contendo os dados dos livros.
        """
        queryset = Livro.objects.all().order_by('titulo')
        serializer = LivroSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def delete(self, request):
        """
        Método DELETE para excluir um ou mais livros identificados por seus IDs.
        - Recebe uma lista de IDs no corpo da requisição.
        - Se algum ID não for encontrado, retorna uma resposta com erro detalhando os IDs inválidos.
        - Caso todos os livros sejam deletados com sucesso, retorna uma resposta de sucesso com código 204 (No Content).

        
        :param request: Objeto `request` contendo a lista de IDs dos livros a serem deletados.
        :return: Resposta indicando sucesso ou erro. Caso algum ID não seja encontrado, uma lista de IDs ausentes será retornada.
        """
        id_erro = ""
        erro = False

        for id in request.data:  
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
    """
    View para criar um novo livro no sistema. Permite que um usuário envie dados de um livro 
    através de uma requisição POST, incluindo título, autor, capa (arquivo), categoria e sinopse.

    **Método POST**:

    :param request: Objeto `request` que contém os dados do livro (campo título, autor, capa, categoria e sinopse).
    :return: Resposta JSON com a mensagem de sucesso ou erro, conforme o caso.
    """
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        """
        Método POST para criar um novo livro.
        - Recebe os dados do livro no corpo da requisição (formato multipart).
        - Os campos obrigatórios são: `titulo`, `autor` e `categoria`.
        - Caso os dados estejam completos, cria um novo livro no banco de dados e retorna uma mensagem de sucesso.
        - Se algum dado obrigatório estiver ausente, retorna um erro de validação com código 400 (Bad Request).

        :param request: Objeto `request` contendo os dados do livro a serem criados.
        :return: Resposta com mensagem de sucesso ou erro.
        """
        titulo = request.data.get('titulo')
        autor = request.data.get('autor')
        capa = request.FILES.get('capa') 
        categoria = request.data.get('categoria')
        sinopse = request.data.get('sinopse')

        if titulo and autor and categoria:
    
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
    """
    View para recuperar ou atualizar os dados de um livro específico, baseado no ID fornecido na URL.

    **Método GET**:
    
    **Método PUT**:

    **Função auxiliar `get_book_by_id`**:

    :param request: Objeto `request` contendo os dados da requisição (para PUT) e o ID do livro na URL (para GET e PUT).
    :param id_arg: ID do livro que será recuperado ou atualizado.
    :return: Resposta JSON com os dados do livro ou mensagem de erro, conforme o caso.
    """
   # authentication_classes = [TokenAuthentication]
   # permission_classes = [IsAuthenticated]
    def get(self, request, id_arg):
        """
        Método GET para recuperar um livro baseado no seu ID.
        - Recebe um `id_arg` como parâmetro de URL.
        - Recupera os dados do livro correspondente ao ID fornecido.
        - Retorna os dados do livro serializados, caso o livro exista.
        - Se o livro não for encontrado, retorna uma resposta de erro 404 (Livro não encontrado).


        :param request: Objeto `request` contendo os parâmetros da requisição.
        :param id_arg: ID do livro a ser recuperado.
        :return: Resposta com os dados do livro ou erro 404 se não encontrado.
        """
        livro = self.get_book_by_id(id_arg)
        if livro:
            serializer = LivroSerializer(livro)
            return Response(serializer.data) 
        else:
            return Response({
                'msg': f'Livro com id #{id_arg} não existe'
            }, status=status.HTTP_404_NOT_FOUND)


    def put(self, request, id_arg):
        """
        Método PUT para atualizar os dados de um livro existente.
        - Recebe um `id_arg` como parâmetro de URL e um corpo de requisição com os dados a serem atualizados.
        - Verifica se o livro com o `id_arg` existe.
        - Se o livro existir, atualiza os dados com base nas informações fornecidas no corpo da requisição.
        - Retorna os dados do livro atualizado com status HTTP 200 (OK) caso a atualização seja bem-sucedida.
        - Se houver algum erro na validação dos dados ou o livro não for encontrado, retorna um erro com status HTTP 400 (Bad Request) ou 404 (Not Found).

        :param request: Objeto `request` contendo os dados para atualização (título, autor, etc).
        :param id_arg: ID do livro a ser atualizado.
        :return: Resposta com os dados atualizados ou erro caso os dados sejam inválidos ou o livro não exista.
        """
        livro = self.get_book_by_id(id_arg)
        if livro:
            serializer = LivroSerializer(livro, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()  
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'msg': f'Livro com id #{id_arg} não existe'
            }, status=status.HTTP_404_NOT_FOUND)

    def get_book_by_id(self, id_arg):
        """
        Função auxiliar para buscar um livro no banco de dados usando o ID fornecido.
        - Responsável por buscar um livro no banco de dados utilizando o `id_arg`.
        - Retorna o livro encontrado ou `None` caso o livro não seja encontrado.

        :param id_arg: ID do livro a ser recuperado.
        :return: O objeto `Livro` correspondente ao ID ou `None` se não encontrado.
        """
        try:
            return Livro.objects.get(id=id_arg)
        except Livro.DoesNotExist:
            return None
