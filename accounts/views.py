from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
# Autenticação
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import AuthenticationFailed
# Swagger
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class CustomAuthToken(ObtainAuthToken):
    """
    Customiza o processo de autenticação de usuários e manipulação de tokens.

    Esta classe sobrescreve o comportamento padrão da API de autenticação do Django Rest Framework,
    permitindo a autenticação do usuário com username e password, a obtenção de informações do usuário
    a partir do token, logout e a alteração de senha do usuário com atualização do token.

    **Métodos:**
    - `post`: Recebe o `username` e `password` no corpo da requisição e, se as credenciais forem válidas,
      retorna um token de autenticação para o usuário. Caso contrário, retorna um erro 401 de credenciais inválidas.
      
    - `get`: Recupera o `username` do usuário autenticado através do token de autenticação fornecido na requisição.
      Retorna o nome de usuário ou 'visitante' caso o token seja inválido.
      
    - `delete`: Realiza o logout do usuário e remove o token de autenticação associado a ele.
    
    - `put`: Permite ao usuário alterar sua senha. A senha é verificada e, em caso de sucesso, o token é atualizado.

    **Parâmetros:**
    - `request`: Objeto request com os dados fornecidos pelo usuário, como username, senha e token de autenticação.
    - `*args`: Argumentos adicionais passados para o método.
    - `**kwargs`: Argumentos de palavra-chave adicionais passados para o método.

    **Funcionamento:**
    - O método `post` autentica o usuário com `username` e `password`, e retorna um token válido para o usuário autenticado.
    - O método `get` retorna o nome do usuário autenticado, ou 'visitante' se o token for inválido.
    - O método `delete` remove o token do usuário, efetivando o logout.
    - O método `put` permite que o usuário altere sua senha, atualizando o token após a mudança.

    :param request: Objeto request contendo as informações necessárias para autenticação, alteração de senha ou logout.
    :return: Resposta contendo o token, nome do usuário ou status de erro, dependendo do método executado.
    """


    @swagger_auto_schema(
        operation_summary='Obter o token de autenticação',
        operation_description='Retorna o token em caso de sucesso na autenticação ou HTTP 401',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password'],
        ),
        responses={
            status.HTTP_200_OK: 'Token retornado com sucesso.',
            status.HTTP_401_UNAUTHORIZED: 'Solicitação não autorizada. Credenciais inválidas.',
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Realiza a autenticação do usuário e gera um token de autenticação caso as credenciais sejam válidas.

        Este método recebe as credenciais de autenticação (`username` e `password`), valida as informações 
        fornecidas e, se o usuário for autenticado com sucesso, cria e retorna um token de autenticação. 
        Caso as credenciais sejam inválidas, retorna um erro 401.

        **Funcionamento:**
        1. Recebe o `username` e `password` no corpo da requisição.
        2. Verifica se os dados são válidos usando o serializer.
        3. Tenta autenticar o usuário com as credenciais fornecidas.
        4. Se a autenticação for bem-sucedida, cria um token e o retorna.
        5. Se as credenciais forem inválidas, retorna uma resposta com erro 401.

        **Parâmetros:**
        - `request`: O objeto request contendo as credenciais `username` e `password` no corpo da requisição.
        - `*args`: Argumentos adicionais passados para o método.
        - `**kwargs`: Argumentos de palavra-chave adicionais passados para o método.

        **Retorno:**
        - Se a autenticação for bem-sucedida, retorna um token de autenticação.
        - Se as credenciais forem inválidas, retorna um erro 401 com uma mensagem de credenciais inválidas.

        :param request: objeto request contendo `username` e `password` para autenticação.
        :return: Resposta contendo o token de autenticação ou erro de credenciais inválidas.
        """

        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token': token.key})
        return Response({'detail': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        operation_summary='Obtém o username do usuário',
        operation_description="Retorna o username do usuário ou 'visitante' se o token for inválido",
        manual_parameters=[ 
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Token de autenticação no formato "Token <valor do token>"',
            ),
        ],
        responses={
            200: openapi.Response(
                description='Nome do usuário',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'username': openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
            404: 'Token não encontrado ou inválido. Usuário não autenticado.',
        }
    )
    def get(self, request):
        """
        Verifica o token de autenticação presente no cabeçalho da requisição e retorna o nome de usuário do usuário autenticado.

        Este método busca o token de autenticação no cabeçalho da requisição, valida o token e, caso seja válido, 
        retorna o `username` do usuário associado. Se o token não for encontrado ou for inválido, retorna 
        "visitante" como nome de usuário.

        **Funcionamento:**
        1. Recupera o token de autenticação do cabeçalho da requisição.
        2. Verifica a validade do token.
        3. Se o token for válido, retorna o `username` do usuário associado.
        4. Se o token não for encontrado ou for inválido, retorna "visitante".

        **Parâmetros:**
        - `request`: O objeto request contendo o cabeçalho `Authorization` com o token de autenticação.

        **Retorno:**
        - Retorna o `username` do usuário autenticado caso o token seja válido.
        - Retorna "visitante" se o token for inválido ou não fornecido.

        :param request: objeto request contendo o cabeçalho `Authorization` com o token de autenticação.
        :return: Resposta com o `username` do usuário ou "visitante" se o token for inválido.
        """

        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1] 
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            return Response({'username': user.username}, status=status.HTTP_200_OK)
        except (Token.DoesNotExist, AttributeError):
            return Response({'username': 'visitante'}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        operation_description='Realiza logout do usuário, apagando o seu token',
        operation_summary='Realiza logout',
        security=[{'Token': []}], 
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING, default='Token ',
                description='Token de autenticação no formato "Token <valor do token>"',
            ),
        ],
        request_body=None,
        responses={
            status.HTTP_200_OK: 'Usuário deslogado com sucesso',
            status.HTTP_400_BAD_REQUEST: 'Requisição inválida. Token não encontrado.',
            status.HTTP_401_UNAUTHORIZED: 'Usuário não autenticado. Token inválido.',
            status.HTTP_403_FORBIDDEN: 'Usuário não autorizado a realizar logout.',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'Erro no servidor ao realizar o logout.',
        },
    )
    def delete(self, request):
        """
        Realiza o logout do usuário, apagando o token de autenticação.

        Este método extrai o token de autenticação da requisição, valida o token, e se o token for válido, 
        realiza o logout do usuário, exclui o token e retorna uma resposta confirmando a operação. 
        Se o token não for válido ou não for fornecido, retorna uma mensagem de erro. Caso o usuário não 
        esteja autenticado, retorna uma mensagem de erro informando que o logout não pode ser realizado.

        **Funcionamento:**
        1. O método recupera o token de autenticação do cabeçalho `Authorization` da requisição.
        2. Valida o token. Se o token for válido, o usuário é autenticado.
        3. Realiza o logout do usuário e exclui o token de autenticação.
        4. Se o token não for válido ou não for encontrado, retorna um erro de requisição.
        5. Se o usuário não estiver autenticado, retorna um erro de autorização.

        **Parâmetros:**
        - `request`: O objeto `request` contendo o cabeçalho `Authorization` com o token de autenticação.

        **Retorno:**
        - Retorna uma resposta confirmando o sucesso do logout e a exclusão do token.
        - Retorna erro em caso de token inválido ou ausente, ou se o usuário não estiver autenticado.

        :param request: objeto request contendo o cabeçalho `Authorization` com o token de autenticação.
        :return: Resposta confirmando o sucesso do logout ou erro, dependendo da situação.
        """
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]  
            token_obj = Token.objects.get(key=token)
        except (Token.DoesNotExist, IndexError):
            return Response({'msg': 'Token não encontrado ou inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = token_obj.user
        if user.is_authenticated:
            request.user = user
            logout(request)
            token_obj.delete()
            return Response({'msg': 'Logout bem-sucedido.'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'Usuário não autenticado.'}, status=status.HTTP_403_FORBIDDEN)
        
    @swagger_auto_schema(
        operation_description='Troca a senha do usuário e atualiza o token em caso de sucesso.',
        operation_summary='Troca a senha do usuário.',
        manual_parameters=[ 
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Token de autenticação no formato "Token <valor do token>"',
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING, description='Senha atual do usuário.'),
                'new_password1': openapi.Schema(type=openapi.TYPE_STRING, description='Nova senha que o usuário deseja definir.'),
                'new_password2': openapi.Schema(type=openapi.TYPE_STRING, description='Confirmação da nova senha.'),
            },
            required=['old_password', 'new_password1', 'new_password2'],
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Senha alterada com sucesso.",
                examples={
                    "application/json": {
                        "message": "Senha alterada com sucesso."
                    }
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Erro na solicitação.",
                examples={
                    "application/json": {
                        "old_password": ["Senha atual incorreta."],
                        "new_password1": ["A nova senha não atende aos requisitos de segurança."]
                    }
                }
            ),
        },
    )
    def put(self, request):
        """
        Permite a alteração da senha do usuário, realizando a validação da senha atual e garantindo que a nova senha seja confirmada.

        **Funcionamento:**
        1. O método recupera o token de autenticação do cabeçalho `Authorization` da requisição.
        2. Valida o token. Se o token for válido, o usuário é autenticado.
        3. Verifica se a senha atual fornecida está correta.
        4. Se a senha atual for válida, o método altera a senha do usuário e atualiza o token de autenticação.
        5. Se a nova senha não coincidir com a confirmação ou se a senha atual estiver incorreta, retorna um erro.

        **Parâmetros:**
        - `request`: O objeto `request` contendo o cabeçalho `Authorization` com o token de autenticação, bem como os dados com a senha atual, nova senha e confirmação da nova senha.

        **Retorno:**
        - Retorna uma resposta com a chave do novo token em caso de sucesso e mensagem indicando que a senha foi alterada.
        - Retorna erro se as senhas não coincidirem, ou se a senha atual estiver incorreta.

        :param request: objeto request contendo o cabeçalho `Authorization` com o token de autenticação e os dados de senha.
        :return: Resposta com o token atualizado e mensagem de sucesso ou erro, dependendo da situação.
        """

        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
        except (Token.DoesNotExist, IndexError):
            return Response({'msg': 'Token inválido ou não fornecido.'}, status=status.HTTP_400_BAD_REQUEST)

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password1')
        confirm_password = request.data.get('new_password2')

        if new_password != confirm_password:
            return Response({'error': 'As novas senhas não coincidem.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
                
            try:
                token = Token.objects.get(user=user)
                token.delete()
                token, _ = Token.objects.get_or_create(user=user)
            except Token.DoesNotExist:
                pass
            return Response({'token': token.key, "message": "Senha alterada com sucesso."}, status=status.HTTP_200_OK)
        else:
            return Response({"old_password": ["Senha atual incorreta."]}, status=status.HTTP_400_BAD_REQUEST)
