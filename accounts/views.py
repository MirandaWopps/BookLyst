from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
# Autenticação
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import login
# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# 2 funcoes iguais no mesmo slide puta kiu pariu fudeu de vez aaa
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
class accountsClasse(APIView):
    def get(self, request):
        return Response({'msg': 'Resposta do método GET'}, status.HTTP_200_OK)
    
    def post(self, request):
        return Response({'msg': 'Resposta do método POST'}, status.HTTP_200_OK)

@api_view(('GET',))
@renderer_classes((JSONRenderer,))   
def accountsGET(request):
    return Response({'msg': 'Resposta da função GET'}, status.HTTP_200_OK)
    
@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def accountsPOST(request):
    return Response({'msg': 'Resposta da função POST'}, status.HTTP_200_OK)

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
            required=['username', 'password', ],
        ),
        responses={
            status.HTTP_200_OK: 'Token is returned.',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized request.',
        },
    )
    def post(self, request, *args, **kwargs):
        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)