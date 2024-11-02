from django.db import models
from django.contrib.auth.models import User 
import datetime


class Categoria(models.Model):
    nome = models.CharField(max_length=40)    
    def __str__(self):
        return self.nome
    
    
    
    
class Creditos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creditos_usuario')
    quantia = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=False, default=0)
    
    
    def __str__(self):
        return self.user.username    
    
    
    
class Anuncio(models.Model):
        Tipos = {
          (  'produto','Produtp'),
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
        categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE, related_name= 'categoria_produto')
        valor = models.DecimalField(max_digits=5,decimal_places=2)
        visualizacao = models.PositiveIntegerField(default=0) 
        avaliacao = models.PositiveIntegerField(default=0)
        tipo =  models.CharField(max_length=10, choices=Tipos)
        
        
        def __str__(self):
            return self.nome
        
    


    
class Customuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sobre = models.CharField(max_length=200)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    creditos = models.ForeignKey(Creditos,on_delete=models.CASCADE,related_name='creditosCustom')
    # creditos= models.DecimalField(max_digits=10, decimal_places=3)
    data_nas = models.DateTimeField(auto_now_add=False,)
    imagem = models.ImageField( upload_to='users', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    
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
    
    
    def __str__(self):
        return self.user_env.username
    
    
class Mensagem_Manager (models.Model):
    user_env = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_env_manager')
    titulo = models.CharField(max_length=60)
    status = models.CharField(max_length=20, choices=[('Pendente', 'Pendente'), ('Confirmada', 'Confirmada'),], default='Pendente')
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
    
        
class Transacao(models.Model):
    user_remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rementente')
    user_destino = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_destino')
    quantidade = models.DecimalField(max_digits=5,decimal_places=2)
    tipo_transacao = models.CharField(max_length=20, choices=[('UserforUser', 'UserforUser'), ('acr_Credito', 'acr_Credito')])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transação de {self.user_remetente.username} para {self.user_destino.username}'

class Extrato(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_extrato')
    date = models.DateTimeField(auto_now_add=True)
    tipo_transacao = models.CharField(max_length=20, choices=[('UserforUser', 'UserforUser'), ('acr_Credito', 'acr_Credito')]),
    quantidade = models.DecimalField(max_digits=5,decimal_places=2)
    user_destino = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userDestino', blank=True)
    
    def __str__(self):
        return f"Pedido {self.id} de {self.user.user.username}"
    
class CreditTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Quantidade de créditos
    transaction_type = models.CharField(max_length=20, choices=[('Depósito', 'Depósito'), ('Compra', 'Compra')])
    date = models.DateTimeField(auto_now_add=True)

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
