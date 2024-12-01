from django.urls import path
from livros import views


app_name = 'livros'

urlpatterns = [
    path("lista/", views.LivroView.as_view(), name='lista-livros'),
    path('livro/', views.newLivroView.as_view(), name='um-livro'),
]