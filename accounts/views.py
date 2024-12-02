from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
# Autenticação
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
# Swagger
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class CustomAuthToken(ObtainAuthToken):

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
        # Autentica o usuário e gera o token
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
        '''
        Parâmetros: o token de acesso
        Retorna: o username ou 'visitante'
        '''
        try:
            # Obtém o token de autorização da requisição
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]  # "Token <valor>"
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            return Response({'username': user.username}, status=status.HTTP_200_OK)
        except (Token.DoesNotExist, AttributeError):
            # Caso o token seja inválido ou ausente
            return Response({'username': 'visitante'}, status=status.HTTP_404_NOT_FOUND)
        
    
    @swagger_auto_schema(
        operation_description='Realiza logout do usuário, apagando o seu token',
        operation_summary='Realiza logout',
        security=[{'Token': []}],  # Definido corretamente a segurança para o token
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
        try:
            # Extrai o token do cabeçalho Authorization
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]  # "Token <valor>"
            token_obj = Token.objects.get(key=token)
        except (Token.DoesNotExist, IndexError):
            # Caso o token não exista ou o cabeçalho esteja mal formatado
            return Response({'msg': 'Token não encontrado ou inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = token_obj.user
        if user.is_authenticated:
            request.user = user
            logout(request)
            # Deleta o token após logout
            token_obj.delete()
            return Response({'msg': 'Logout bem-sucedido.'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'Usuário não autenticado.'}, status=status.HTTP_403_FORBIDDEN)
