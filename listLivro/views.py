from django.shortcuts import render
# Create your views here.

from listLivro.serializer import LivroSerializer
from rest_framework.views import APIView
from listLivro.models import Livro
from rest_framework.response import Response
from rest_framework import status

class LivroView(APIView):
    def get(self, request):
        queryset = Livro.objects.all().order_by('id')
        # importante informar que o queryset terá mais
        # de 1 resultado usando many=True
        serializer = LivroSerializer(queryset, many=True)
        return Response(serializer.data)
    
class newLivroView(APIView):
    def post(self, request):
        serializer = LivroSerializer(data=request.data)
        print('Serializer=',serializer)
        if serializer.is_valid():
            serializer.save()
            # uma boa prática é retornar o próprio objeto armazenado
            return Response(serializer.data,
            status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
            status.HTTP_400_BAD_REQUEST)