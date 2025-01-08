from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', homeSiteView, name='home'),
    path('cadastro', cadastroView, name='cadastro'),
    path('login', loginView, name='login'),
    
    #home
    path('lista_produtos', listaProdutosView, name='lista_produtos'),
    path('lista_produtos/<categoria>', listaCategoriaView, name='lista_categorias'),
    path('lista_servicos', listaServicosView, name='lista_servicos'),
    
    path('pesquisa', pesquisarView, name='pesquisa'),
    
    
    path('produto/<id>', produtoView, name='produto'),
    path('servico/<id>', servicosView, name='servico'),
    # path('servicos/<search>', listaProdutosView, name='lista_produtos'),
    path('lista_produtos/<search>', listaProdutosView, name='lista_produtos'),
    path('categoria/<cat>', categoriaView, name='categoria'),
    
    
    
    # dashboard
    path('dashboard', dashboardView, name='dashboard'),
    path('pedido/<id>', pedidoIdView, name='pedidos'),
    path('entregue/<id>', confirmarEntregaView, name='confirmarEntrega'),
    path('mudarInfo', mudarInfoView, name='mudarInfo'),
    path('confirmarEmail',confirmaEmailView, name='confirmarEmail'),
    path('email/<uidb64>/<token>/', authenticate_via_email, name='auth_email'),
    path('minhaConta', minhaContaView, name='minhaConta'),
    path('gerAnuncio', gerAnuncioView, name='gerAnuncio'),
    path('minhasVendas', minhaVendasView, name='minhasVendas'),
    path('comprovante/<id_pedido>', comprovanteView, name='comprovante'),
    path('minhasCompras', comprasView, name='minhasCompras'),
    path('meuPerfil', meuPerfilView, name='meuPerfil'),
    path('mensagens', mensagensView, name='mensagens'),
    path('mensagem/<id>', mensagemView, name='mensagem'),
    path('deleteMensagens<idObj>', deleteMsgView, name='deleteMensagens'),
    path('deleteAnuncio<idObj>', deleteAnuncioView, name='deleteAnuncio'),

    path('pubAnuncio', pubAnuncioView, name='pubAnuncio'),
    path('editarAnuncio/<idObj>/', editAnuncioView, name='editAnuncio'),
    path('gerAnuncio', gerAnuncioView, name='gerAnuncio'),
    path('logout', logoutView, name='logout'),
    
    #carrinho 
    path('addCarrinho/<id>/', carrinho_add,  name='addCarrinho'),
    path('carrinho/', carrinho,  name='carrinho'),
    path('limpar_carrinho/', limparCarrinhoView,  name='limparCarrinho'),
    path('delete/<idObj>', deleteView,  name='delete'),
    path('quantidade/<idObj>/<desc>', quantidadeView,  name='quantidade'),
    path('checkout', checkoutView,  name='checkout'),
    path('pagamento', pagamentoView,  name='pagamento'),
    path('pedidos', pedidosView,  name='pedidos'),
    path('creditos', creditosView,  name='creditos'),
    path('msg_senha',msg_senhaView,  name='msg_senha'),
    path('rec_senha', rec_senhaView,  name='rec_senha'),
    path('reset_senha/<str:uidb64>/<str:token>/', reset_senha, name='reset_senha'),   
    

    
    
    path('teste', teste,  name='teste'),
    
    
    
    
    
    
    #comentarios
    path('comentario/<id_produto>/', comentarioView,  name='addComentario'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    
    