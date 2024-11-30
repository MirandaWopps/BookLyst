from rest_framework import serializers
from listLivro.models import Livro
class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro # nome do modelo
        fields = '__all__' # lista de campos