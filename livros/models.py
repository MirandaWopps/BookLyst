from django.db import models
from django.core.files.storage import FileSystemStorage

# Create your models here.
fs = FileSystemStorage(location="VersoLivro/static/img/VersoLivro")

class Livro(models.Model):
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