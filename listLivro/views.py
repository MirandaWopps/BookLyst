from django.shortcuts import render
# Create your views here.

from listLivro.serializer import LivroSerializer
from rest_framework.views import APIView
from listLivro.models import Livro
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

class LivroView(APIView):
    def get(self, request):
        queryset = Livro.objects.all().order_by('id')
        # importante informar que o queryset terá mais
        # de 1 resultado usando many=True
        serializer = LivroSerializer(queryset, many=True)
        return Response(serializer.data)
    
class newLivroView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(postself, request, *args, **kwargs):
        image = request.FILES.get('image')
        metadata = request.data.get('metadata') #Metadata in JSON format as string
        if image and metadata:
            return Response({
                "message" : "Upload sucessful !",
                "image_name" : image.name,
                "metadata": metadata,
                }, 
                status=status.HTTP_201_CREATED)
        else:
            return Response({
                "message": "Missing image or metadata."},
                status=status.HTTP_400_BAD_REQUEST)