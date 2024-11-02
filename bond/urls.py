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
    
    #home
  
    path('lista_produtos', listaProdutosView, name='lista_produtos'),
    path('lista_produtos/<categoria>', listaCategoriaView, name='lista_categorias'),
    path('lista_servicos', listaServicosView, name='lista_servicos'),
    
    
    path('produto/<id>', produtoView, name='produto'),
    path('servico/<id>', servicosView, name='servico'),
    # path('servicos/<search>', listaProdutosView, name='lista_produtos'),
    path('lista_produtos/<search>', listaProdutosView, name='lista_produtos'),
    path('categoria/<cat>', categoriaView, name='categoria'),
    
    
    
    # dashboard
    path('dashboard', dashboardView, name='dashboard'),
    path('mudarInfo', mudarInfoView, name='mudarInfo'),
    path('minhaConta', minhaContaView, name='minhaConta'),
    path('meuPerfil', meuPerfilView, name='meuPerfil'),
    path('mensagens', mensagensView, name='mensagens'),
    path('pubAnuncio', pubAnuncioView, name='pubAnuncio'),
    path('editarAnuncio/<idObj>/', editAnuncioView, name='editAnuncio'),
    path('gerAnuncio', gerAnuncioView, name='gerAnuncio'),
    path('logout', logoutView, name='logout'),
    path('tipo', tipoView, name='tipo'),
    
    #carrinho 
    path('addCarrinho/<id>/', carrinho_add,  name='addCarrinho'),
    path('carrinho/', carrinho,  name='carrinho'),
    path('limpar_carrinho/', limparCarrinhoView,  name='limparCarrinho'),
    path('delete/<idObj>', deleteView,  name='delete'),
    path('quantidade/<idObj>/<desc>', quantidadeView,  name='quantidade'),
    path('checkout', checkoutView,  name='checkout'),
    path('pagamento', pagamentoView,  name='pagamento'),
    path('creditos', creditoView,  name='creditos'),
    
    
    
    
    
    #comentarios
    path('comentario/<tipo>/', comentarioView,  name='addComentario'),
    
    
    
    

]
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL,
                            document_root= settings.MEDIA_ROOT)

    
    
    