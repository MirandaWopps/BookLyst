from django.contrib import admin

# Register your models here.

from livros.models import Livro
admin.site.register(Livro)