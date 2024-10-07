from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', homeSiteView, name='home'),
    path('colaborador', groupsColaborador, name='colaborador'),
    path('cliente', groupsCliente, name='cliente'),
    path('cadastro', cadastroView, name='cadastro'),
    path('login', loginView, name='login'),
    path('addCarrinho/<id>/', carrinho_add,  name='addCarrinho'),
    path('carrinho/', carrinho,  name='carrinho'),
    path('dashboard', dashboardView, name='dashboard'),
    path('lista_produtos', listaProdutosView, name='lista_produtos'),
    path('servicos', servicosView, name='servicos'),
    path('servicos/<search>', listaProdutosView, name='lista_produtos'),
    path('lista_produtos/<search>', listaProdutosView, name='lista_produtos'),
    path('mudarInfo', mudarInfoView, name='mudarInfo'),
    path('minhaConta', minhaContaView, name='minhaConta'),
    path('meuPerfil', meuPerfilView, name='meuPerfil'),
    path('mensagens', mensagensView, name='mensagens'),
    path('pubAnuncio', pubAnuncioView, name='pubAnuncio'),
    path('gerAnuncio', gerAnuncioView, name='gerAnuncio'),
    path('logout', logoutView, name='logout'),
    path('tipo', tipoView, name='tipo'),
    
    
    

]
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL,
                            document_root= settings.MEDIA_ROOT)

    
    
    