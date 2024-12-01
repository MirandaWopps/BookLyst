from rest_framework import serializers
from livros.models import Livro

class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro # nome do modelo
        fields = '__all__' # lista de campos