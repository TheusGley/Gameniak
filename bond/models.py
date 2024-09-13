from django.db import models
from django.contrib.auth.models import User 


class Categoria(models.Model):
    nome = models.CharField(max_length=40)

    
    
    def __str__(self):
        return self.nome
    
class Produto(models.Model):
    usuario = models.OneToOneField(User,on_delete=models.CASCADE)
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

    
    
    
    def __str__(self):
        return self.nome
    
    
    
class Servico(models.Model):
    usuario = models.OneToOneField(User,on_delete=models.CASCADE)
    nome = models.CharField(max_length=40)
    bv_desc = models.CharField(max_length=60)
    descricao = models.CharField(max_length=300)
    funcao = models.CharField(max_length=60)
    tags = models.CharField(max_length=40)  
    imagens_produto = models.ImageField( upload_to='imagens_produtos', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    data_adicionada = models.DateField(auto_now=True)
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE, related_name= 'categoria_servico')
    valor = models.DecimalField(max_digits=5,decimal_places=2)
    visualizacao = models.PositiveIntegerField(default=0) 
    
    
    
    def __str__(self):
        return self.nome
    


    
class Customuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sobre = models.CharField(max_length=200)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    creditos = models.DecimalField(max_digits=5,decimal_places=2)
    data_nas = models.DateTimeField(auto_now_add=False,)
    imagem = models.ImageField( upload_to='users/', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    
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
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    avaliacao =  models.PositiveIntegerField()
    quantidade = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    
    def  __str__(self) :
        
        return "Carrinho: " + str(self.carrinho.id) + "   Produto: "+ str(self.id)
    
        
class Transaction(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    product = models.ForeignKey(Produto, on_delete=models.CASCADE)
    credits_exchanged = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transação de {self.buyer.user.username} para {self.seller.user.username}'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Produto)
    total_credits = models.DecimalField(max_digits=10, decimal_places=2)  # Total em créditos
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pendente', 'Pendente'), ('Pago', 'Pago')], default='Pendente')

    def __str__(self):
        return f"Pedido {self.id} de {self.user.user.username}"
class CreditTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Quantidade de créditos
    transaction_type = models.CharField(max_length=20, choices=[('Depósito', 'Depósito'), ('Compra', 'Compra')])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.transaction_type} - {self.amount} créditos para {self.user.user.username}'
