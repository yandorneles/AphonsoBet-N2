from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.pagina_inicial, name="pagina_inicio"),
    path('login/', views.pagina_login, name="pagina_login"),
    path('logout/', views.pagina_inicial, name="pagina_logout"),
    path('cadastro/', views.pagina_cadastro, name="pagina_cadastro"),
    path('apostas/', views.pagina_apostas, name="pagina_apostas"),
    path('apostar/<int:jogo_id>', views.pagina_apostar, name="pagina_apostar"),
    # arquivos
    path('aphonso_bet/static/upload/<str:filename>', views.obter_upload, name="uploads"),
]
