from django.urls import path
from listLivro import views

app_name = 'listLivro'

urlpatterns = [
    path("lista/",views.LivroView.as_view(),name='lista-livro'),
    path('livro/', views.newLivroView.as_view(), name='novo-livro'),
]             