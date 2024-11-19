from django.urls import path
from accounts import views
from django.urls import include

app_name = 'accounts'

urlpatterns = [
    path('accountsClasse/', views.accountsClasse.as_view(), name='accountsClasse'),
    path('accountsGET/', views.accountsGET, name='accountsGET'),
    path('accountsPOST/', views.accountsPOST, name='accountsPOST'),
]