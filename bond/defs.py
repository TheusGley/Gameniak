from .models import *


    # verficar o model mensagem cada objeto para muda o status

    #validador de pedido vai disponibilizar os creditos para o anunciante  
def validador_pedido(id_pedido):
    pedido = Pedido.objects.get(id=id_pedido)
    extrato = Extrato.objects.all()
    
    if  pedido.comprovante:
        produtos = Produto_Carrinho.objects.filter(carrinho=pedido.carrinho)
        
        for p in produtos:
            user_produto = p.produto.user
            user_creditos = Credito.objects.get(user=user_produto)
            user_creditos += p.produto.valor 
            p.produto.venda += 1
            user_creditos.save()
        extrato.create(
            user= pedido.user_remetente,
            valor_carrinnho= pedido.carrinho.total,
            carrinho = pedido.carrinho
        )
        return True
    else:
        return False
            
                