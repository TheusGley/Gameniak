from .models import *
import re 

from .models import * 
from datetime import datetime, timedelta
import pytz
import decimal
from django.utils.timezone import now 
from django.db.utils import IntegrityError




    # verficar o model mensagem cada objeto para muda o status
def veri_mensagem(mensagem):

    telefone_regex = r'\b\d{7,15}\b'  # Números com 7 a 15 dígitos
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    mensagem_manager = Mensagem_Manager.objects.get(id= mensagem.id)
    mensagem_model = Mensagen.objects.all()
    mensagem = mensagem_manager.mensagem
       
    if re.search(telefone_regex, mensagem):
        print(mensagem_manager)
        mensagem_manager.status = "Recusado"
        
        mensagem_manager.save()
        print("contem telefone")
        
        return None
    elif re.search(email_regex, mensagem):
        mensagem_manager.status = "Recusado"
        mensagem_manager.save()
        print("contem email")
        
        return None
    else:
        mensagem_manager.status = "Confirmada"
        print("Criado")
        mensagem_model.create(
            user_env = mensagem_manager.user_env,
            titulo = mensagem_manager.titulo,
            mensagem= mensagem_manager.mensagem,
            status = "Recebida",
            user_rec= mensagem_manager.user_rec
        )
        mensagem_manager.save()
        return None
    
    
    #validador de pedido vai disponibilizar os creditos para o anunciante  
def validador_pedido(id_pedido):
    pedido = Pedido.objects.get(id=id_pedido)
    user_admin= Credito.objects.get(user__username="admin")
    
    if  pedido.comprovante:
        produtos = Produto_Carrinho.objects.filter(carrinho=pedido.carrinho)
        try :
            for p in produtos:
                user_produto = p.produto.usuario
                user_creditos = Credito.objects.get(user=user_produto)
                valor_credito = float(p.produto.valor) * 0.10 
                user_creditos.valor += p.produto.valor - decimal.Decimal(valor_credito)
                user_admin.valor+=  decimal.Decimal(valor_credito)
                print(user_admin.valor)
                user_admin.save()
                p.produto.vendas += 1
                user_creditos.save()
                print("creditos Adicionados a:" + str(user_creditos)) 
            return True
        except IntegrityError as e :
            print("Creditos nao adicionados")
    return False
            
def saque_credito(id_user):
    
    try:
        credito = Credito.objects.get(user=id_user)
        
    except:
        return False
        

def contador_prazo():        
    pedidos = Pedido.objects.filter(status_pedido='Pendente').select_related('carrinho')
    for pedido in pedidos:
    # Obter todos os produtos do carrinho em uma única consulta
        produtos_carrinho = Produto_Carrinho.objects.filter(carrinho=pedido.carrinho)

        for produto_carrinho in produtos_carrinho:
            anuncio = produto_carrinho.produto
            if anuncio.data_prazo:  # Verificar se o prazo existe
                    data_limite = pedido.date + timedelta(days=anuncio.data_prazo)
                    data_limite_aware = data_limite.replace(tzinfo=pytz.utc)

                    agora = datetime.now(pytz.utc)  # Obtendo a data e hora atual em UTC

                    if agora >= data_limite_aware:
                        recusar_pedido(pedido)
                    elif agora == data_limite_aware:
                        enviar_mensagem(anuncio.usuario)

def recusar_pedido(pedido):
    # Lógica para recusar o pedid
    print("Pedido recusado")
    pass 

def enviar_mensagem(usuario):
    # Lógica para enviar mensagem ao usuário
    print("Enviando Mentiras..")
    
    pass

def media_avaliacao (produto, avaliacao):
    produto_get = Anuncio.objects.get(id=produto.id)
    coments = Comentario.objects.filter(produto=produto)
    
    avaliacoes = 0
    for obj in coments:
        avaliacoes += obj.avaliacao
        
    media_final = avaliacoes / coments.count()
    produto_get.avaliacao_anuncio = round(media_final)
    produto_get.save()
    return print(round(media_final))
    
    
def contador_prazo():
    # Filtra pedidos pendentes
    pedidos = Pedido.objects.filter(status_pedido="Pendente")
    
    # Itera sobre os pedidos
    for p in pedidos:
        try:
            # Obtém o anúncio relacionado ao carrinho do pedido
            anuncio = Anuncio.objects.get(nome__icontains=p.carrinho_str)
            
            # Calcula a data final do prazo
            data_final = p.date + timedelta(days=anuncio.data_prazo)
            
            # Verifica se o prazo expirou
            if data_final < now():
                p.status_pedido = "Recusado"
                p.save()  # Salva a alteração no banco de dados
                print(f"Pedido {p.id}: Recusado")
            else:
                print(f"Pedido {p.id}: Dentro do prazo")
        except Anuncio.DoesNotExist:
            print(f"Anúncio relacionado ao pedido {p.id} não encontrado.")
            
            
def validador_doc (documento, user):
    
    
    if documento:
        
        conf_user = Confiabilidade.objects.get(user=user)
        conf_user.nivel_confiavel +=1
        conf_user.save() 
        
        print(f"aumentamos o nivel de confiabilidade para {conf_user.user.username} ")
    
    return True
    