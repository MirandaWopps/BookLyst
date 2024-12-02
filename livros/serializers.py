from rest_framework import serializers
from livros.models import Livro

class LivroSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Livro.

    Este serializador é responsável por transformar os objetos `Livro` em representações JSON e vice-versa.
    Ele mapeia os campos do modelo `Livro` para o formato JSON e valida os dados de entrada para garantir
    que estão de acordo com as regras definidas no modelo.

    A classe `Meta` define o modelo que será utilizado, que é o modelo `Livro`, e o atributo `fields`
    determina quais campos do modelo serão incluídos no processo de serialização. Neste caso, a opção `__all__`
    inclui todos os campos do modelo `Livro`.

    **Parâmetros:**
    Não há parâmetros adicionais para o funcionamento do serializador, pois ele trabalha diretamente
    com o modelo `Livro` e os dados fornecidos durante a serialização ou desserialização.

    :param request: Objeto `request` contendo os dados a serem validados e serializados.
    :return: Representação serializada do objeto `Livro`, ou erro de validação caso os dados sejam inválidos.
    """
    
    class Meta:
        model = Livro # nome do modelo
        fields = '__all__' # lista de campos