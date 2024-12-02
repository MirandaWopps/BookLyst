from django.db import models
from django.core.files.storage import FileSystemStorage

# Create your models here.
fs = FileSystemStorage(location="livros/static/img/livros")

class Livro(models.Model):
    """
    Modelo que representa um Livro no sistema.

    Este modelo armazena informações sobre os livros, incluindo título, autor, categoria, capa e sinopse.
    A categoria do livro é um campo com opções predefinidas, permitindo selecionar entre diferentes tipos de livros, 
    como "Autoajuda", "Bibliografia", "Comédia", etc. A capa é um campo de imagem para armazenar a capa do livro,
    e a sinopse é um campo de texto livre para descrever o conteúdo do livro.

    **Parâmetros:**
    - `id`: Identificador único do livro (chave primária). Atribuído automaticamente.
    - `titulo`: Título do livro, com um máximo de 100 caracteres.
    - `autor`: Nome do autor do livro, com um máximo de 100 caracteres.
    - `categoria`: Categoria do livro, definida por uma escolha entre os valores predefinidos em `TIPO_CATEGORIA`.
    - `capa`: Imagem da capa do livro, armazenada no sistema de arquivos.
    - `sinopse`: Descrição do livro, com texto livre, com um valor padrão de "Sinopse...".

    **Funcionamento:**
    - O modelo `Livro` é utilizado para criar, armazenar e gerenciar informações sobre os livros no banco de dados.
    - A categoria do livro é restrita a uma lista predefinida de tipos, fornecendo uma interface de seleção para o usuário.
    - A capa do livro é armazenada como uma imagem, e a sinopse fornece uma descrição textual do conteúdo do livro.

    :param request: Objeto de solicitação que pode ser usado para obter dados de um livro a ser armazenado ou atualizado.
    :return: Instância do livro salva no banco de dados.
    """
    TIPO_CATEGORIA = {
        "A": "Autoajuda",
        "B": "Bibliografia",
        "C": "Comedia",
        "E": "Epico",
        "I": "Infantil",
        "L": "Literatura",
        "M": "Matematica",
        "P": "Poesia",
        "R": "Romance",
        "T": "Terror",
    }

    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, help_text='titulo')
    autor = models.CharField(max_length=100, help_text='autor')
    categoria = models.CharField(max_length=1, choices=TIPO_CATEGORIA, default='SELECIONE')
    capa = models.ImageField(storage=fs)
    sinopse = models.TextField(default='Sinopse..')

    def __str__(self):
        return self.titulo