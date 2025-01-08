from django.db import models
from django.contrib.auth.models import User 
import datetime
import uuid
from django.utils import timezone

import os
from datetime import datetime


class Categoria(models.Model):
    nome = models.CharField(max_length=40)    
    def __str__(self):
        return self.nome
    
    
    
    
class Credito(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creditos_usuario')
    valor = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=False, default=0)
    valor_antigo = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=False, default=0)
    
    
    def __str__(self):
        return self.user.username    
    
    
    
class Anuncio(models.Model):
        Tipos = {
          (  'produto','Produto'),
          (  'servico','Servico'),  
        }
        
        usuario = models.ForeignKey(User,on_delete=models.CASCADE)
        nome = models.CharField(max_length=40)
        bv_desc = models.CharField(max_length=60)
        descricao = models.CharField(max_length=300)
        funcao = models.CharField(max_length=60)
        tags = models.CharField(max_length=40)
        imagem = models.ImageField( upload_to='imagens_produtos', height_field=None, width_field=None, max_length=None, blank=True, null=True)
        data_adicionada = models.DateField(auto_now=True)
        data_prazo = models.PositiveBigIntegerField()
        categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE, related_name= 'categoria_produto')
        valor = models.DecimalField(max_digits=5,decimal_places=2)
        visualizacao = models.PositiveIntegerField(default=0) 
        vendas = models.PositiveIntegerField(default=0) 
        avaliacao_anuncio= models.CharField(max_length=2)
        tipo =  models.CharField(max_length=10, choices=Tipos)
        
        
        def __str__(self):
            return self.nome

        
class Confiabilidade (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    data_membro = models.DateField(auto_now=True,blank=True)
    ultimo_acesso = models.DateTimeField(auto_now=False,blank=True,null=True)
    nivel_confiavel = models.IntegerField(default=0,  null=False,blank=True)
    imagemDoc = models.ImageField( upload_to='docs', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    email = models.BooleanField(default=False, null=False, blank=True)
    
    def __str__(self):
        return self.user.username
            

    
class Customuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sobre = models.CharField(max_length=200)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    creditos = models.ForeignKey(Credito,on_delete=models.CASCADE,related_name='creditosCustom')
    data_nas = models.DateTimeField(auto_now_add=False,)
    imagem = models.ImageField( upload_to='users', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    confiabilidade = models.ForeignKey(Confiabilidade, on_delete=models.CASCADE, related_name="confiabilidade" ,null=True  )
    
    def __str__(self):
        return self.user.username

class Banner(models.Model):
    titulo = models.CharField(max_length=10)
    descricao = models.CharField(max_length=50, null=True)
    valor = models.DecimalField(max_digits=5,decimal_places=2, null=True)
    imagem1 = models.ImageField( upload_to='banners/', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    def __str__(self):
        return self.titulo

class Mensagen (models.Model):
    user_env = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_env')
    titulo = models.CharField(max_length=60)
    mensagem  = models.CharField(max_length=400)
    status = models.CharField(max_length=20, choices=[('Pendente', 'Pendente'), ('Enviada', 'Enviada'), ('Recebida', 'Recebida')], default='Pendente')
    user_rec = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rec')
    data = models.DateField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.user_env.username
    
    
class Mensagem_Manager (models.Model):
    user_env = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_env_manager')
    titulo = models.CharField(max_length=60)
    status = models.CharField(max_length=20, choices=[('Recusada', 'Recusada'), ('Pendente', 'Pendente'), ('Confirmada', 'Confirmada'),], default='Pendente')
    mensagem  = models.CharField(max_length=400)
    user_rec = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rec_manager')
    
    def __str__(self):
        return self.user_env.username
    
class Carrinho (models.Model):
    cliente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank = True)
    total = models.PositiveIntegerField(default=0)
    data_criado = models.DateField(auto_now_add=True)
    
    def  __str__(self) :
        
        return "Carrinho"  + str(self.id)

class Produto_Carrinho (models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    produto = models.ForeignKey(Anuncio, on_delete=models.SET_NULL, null=True)
    avaliacao =  models.PositiveIntegerField()
    quantidade = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    
    def  __str__(self) :
        
        return "Carrinho: " + str(self.carrinho.id) + "   Produto: "+ str(self.id)
    

def upload_to(instance, filename):
    # Extrair a extensão do arquivo original
    ext = filename.split('.')[-1]
    # Formatar o nome do arquivo com o ID do objeto e a data atual
    filename = f"{instance.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
    # Retornar o caminho completo onde o arquivo será salvo
    return os.path.join('comprovantes/', filename)



class Pedido(models.Model):
    user_remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rementente')
    valor_carrinho = models.DecimalField(max_digits=5,decimal_places=2)
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name="Carrinho_pedido")
    carrinho_str = models.CharField(max_length=100, blank=True, null=True)
    status_pagamento = models.CharField(max_length=20, blank=True, choices=[('Pendente', 'Pendente'), ('Concluida', 'Concluida'), ('Recusada', 'Recusada')])
    status_pedido= models.CharField(max_length=20, blank=True, choices=[('Pendente', 'Pendente'), ('Concluida', 'Concluida'), ('Recusada', 'Recusada')])
    metodo_pagamento = models.CharField(max_length=100, blank=True, choices=[('Creditos', 'Creditos'), ('Pix', 'Pix')])
    date = models.DateTimeField(auto_now_add=True)
    comprovante = models.ImageField( upload_to=upload_to, height_field=None, width_field=None, max_length=None,  blank=True, null=True)
    confirm_client = models.BooleanField(default=False)
    def __str__(self):
        return f'Pedidos de {self.user_remetente.username} n° {self.id} '

class Transacoes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_extrato')
    date = models.DateTimeField(auto_now_add=True)
    valor  = models.DecimalField(max_digits=5,decimal_places=2)
    tipo_transacao = models.CharField(max_length=20, choices=[('Depósito', 'Depósito'), ('Saque', 'Saque')])

    
    def __str__(self):
        return f" {self.id}  {self.user.username}"
    
class Avaliacao(models.Model):
    anuncio = models.ForeignKey(Anuncio, on_delete=models.CASCADE)
    avaliacao = models.PositiveBigIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.transaction_type} - {self.amount} créditos para {self.user.user.username}'
    
    
class Comentario (models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.CharField(max_length=100, blank=True, null=True)
    produto = models.ForeignKey(Anuncio, on_delete=models.CASCADE, blank=True, null=True)
    avaliacao = models.IntegerField(null=False, blank=False, default=0)
    data_create = models.DateField(auto_now_add=True, null=True, blank=False)
    customUser =  models.ForeignKey(Customuser,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username



class EmailToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)

    def is_valid(self):
        # Você pode configurar a validade do token, por exemplo, 15 minutos
        expiration_time = timezone.now() - timezone.timedelta(minutes=15)
        return self.created_at >= expiration_time
    
                
class Checkout (models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    ultimo_nome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE, blank=True,null=True )
    
    def __str__(self):
            return f'Usuario : {self.user.username}  Pedido: N° {self.pedido.id}'
        
        