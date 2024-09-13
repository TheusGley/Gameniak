from django.shortcuts import render
from .models import *
from django.db.utils import IntegrityError 
from django.contrib.auth import authenticate, login ,  logout
import datetime
from django.shortcuts import render,get_object_or_404, redirect
from decimal import Decimal



def loginView (request):
    
    if request.user.is_authenticated:
        
        return redirect('dashboard')                     
            

    if request.method == 'POST':
            username = request.POST.get('email')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                    login(request,user)
                    return redirect('dashboard')
            else :
                    error_messagem = "Email ou Senha não conferem" 
                    return render (request, 'index/login.html', {'error_messagem':error_messagem})
                
    else:
        return render(request, 'index/login.html')
            
            
    return render(request, 'index/login.html')


# Index 

def homeSiteView (request):
    
    carro_id = request.session.get("carro_id", None)
            
    if carro_id:
        carro_id = Carrinho.objects.get(id=carro_id)
    else:
        carro_id = None
        
    produto_destaque = Produto.objects.filter(visualizacao = 10) 
    contagem = Produto_Carrinho.objects.filter(carrinho= carro_id).count()
    produto_carrinho = Produto_Carrinho.objects.filter(carrinho = carro_id)
    today = datetime.datetime.today().month
    imagens_banner = Banner.objects.all()
    
    # Colocar os produtos mais Vendidos, 
    produtos = Produto.objects.all()
    produto_recentes = Produto.objects.filter(data_adicionada__month=today)
    servicos_recentes = Servico.objects.filter(data_adicionada__month=today)
    
    
    context = {
        'produto_carrinho': produto_carrinho,
        'imagens_banner': imagens_banner,
        'produto_destaque':produto_destaque,
        'Produtos':produtos,
        'produto_recentes':  produto_recentes,
        'contagem':contagem,
        'servicos_recentes':servicos_recentes,
        
    }
    
    
    return render(request, 'index/index.html',context )


def carrinho_add (request, id):    
    produto = get_object_or_404(Produto, id=id)
    carro_id = request.session.get("carro_id", None)
    
    if carro_id :
        carro_obj = Carrinho.objects.get(id=carro_id)
        # carroProduto = Produto_Carrinho.objects.get(produto=produto)
        produto_no_carrinho = carro_obj.produto_carrinho_set.filter(produto=produto)        
        if produto_no_carrinho.exists():    
            carroProduto= produto_no_carrinho.last()
            carroProduto.quantidade += 1
            carroProduto.subtotal = produto.valor
            carroProduto.save()
            carro_obj.total += produto.valor
            carro_obj.save()
            
        else:
            carroProduto = Produto_Carrinho.objects.create(carrinho = carro_obj,produto = produto, avaliacao   = produto.valor,  quantidade  = 1, subtotal=produto.valor)
            carro_obj.total += produto.valor
            carro_obj.save()
        
            
    else:
        carro_obj = Carrinho.objects.create(total= 0)
        request.session["carro_id"]=carro_obj.id
        carroProduto = Produto_Carrinho.objects.create(carrinho    = carro_obj,produto     = produto, avaliacao   = produto.valor,  quantidade  = 1,           subtotal=produto.valor)
        carro_obj.total += produto.valor
        carro_obj.save()
        
    active  = "disabled"
       
    context ={ 'active' : active, 
              }
    
    return redirect('home' )


def carrinho (request): 
    
    carro_id = request.session.get("carro_id", None)
            
    if carro_id:
        carro_id = Carrinho.objects.get(id=carro_id)
    else:
        carro_id = None
        
   
           
    context = { 
        'carro':carro_id,
    }
       
    return render (request, 'index/carrinho.html', context)   



def listaProdutosView (request):
    
    produtos = Produto.objects.all()
    categorias = Categoria.objects.all()
    # produtosD = Produto.objects.filter()
    context = { 
            'categorias':categorias,
            'produtos' :produtos,
            }
    
    return render(request, 'index/lista-produtos.html', context)


def servicosView (request):
    
    servicos = Servico.objects.all()
    categorias = Categoria.objects.all()
    # produtosD = Produto.objects.filter()
    context = { 
            'categorias':categorias,
            'servicos' :servicos,
            }
    
    return render(request, 'index/lista-servicos.html', context)




def homeView (request):
    
    return render(request, 'dashboard/index.html')


def meuPerfilView(request):
    
    return render(request, 'dashboard/meu-servico.html')



def dashboardView (request):
    
    now=  datetime.datetime.now()
    user = Customuser.objects.get(user=request.user)     
    creditos = user.creditos
    transacoes = Transaction.objects.filter(seller=request.user.id)
    produtos_vendidos = Transaction.objects.filter(seller=request.user.id).count()
    produtos = Produto.objects.filter(usuario=request.user).count()
    servicos = Servico.objects.filter(usuario=request.user).count()

    produtos_servicos = produtos + servicos

    valorTotal = Transaction.objects.filter(seller=request.user.id)
    ultimas_vendas = Transaction.objects.filter(seller=request.user.id, date__month=now.month)
    if valorTotal:
        
        for i in valorTotal:
            total =+ i.valor
    total = 0
            
                
    context = {
        'transacoes': transacoes,
        'ultimas_vendas':ultimas_vendas,
        'valorTotal': total,
        'creditos' : creditos, 
        'produtos_vendidos':produtos_vendidos,
        'produtos_servicos':produtos_servicos,
    }
    return render(request, 'dashboard/index.html',context)



def minhaContaView(request):
    user = User.objects.get(id=request.user.id)
    userInfo = Customuser.objects.get(user=user)
    error_messages = " "
    
    
    if request.method == 'POST':
        username = request.POST.get('username')
        telefone = request.POST.get('telefone')
        sobre = request.POST.get('sobre')
        imagem = request.POST.get('imagem')
        
        try:
            User.objects.get(username=username)
            error_messages = "Ja existe um Usario com esse username"
            
            context = {
            'userInfo':userInfo,
            'error_message': error_messages,
            }
    
            return render(request, 'dashboard/minha-conta.html',context)
        except :
            try :
                user.username=username
                user.save()
                userInfo.telefone=telefone,
                userInfo.sobre=sobre,
                userInfo.imagem=imagem
                
                userInfo.save()
                
                context = {
                    'userInfo':userInfo,
                    'error_message': error_messages,
                    
                    }
            
                
                return render(request, 'dashboard/minha-conta.html',context)
            except IntegrityError as e :
                
                context = {
                    'userInfo':userInfo,
                    'error_message': e,
                    
                    }
                return render(request, 'dashboard/minha-conta.html',context)
            
        
    
    context = {
        'userInfo':userInfo,
        'error_message': error_messages,
        
        }
    
    return render(request, 'dashboard/minha-conta.html',context)



def mensagensView(request):
    user = User.objects.get(id=request.user.id)
    mensagemInstance = Mensagen.objects.all()
    mensagens_envi = Mensagen.objects.filter(user_env=user)
    mensagens_rec = Mensagem_Manager.objects.filter(user_rec=user, status= "Confirmada")
    error_message = " "
    
    if request.method == 'POST':
        user_rec = request.POST.get('user_rec')
        mensagem =  request.POST.get('mensagem')
        titulo =  request.POST.get('titulo')
        
        try:
            
            user_get =  User.objects.get(username=user_rec)
            mensagemManager = Mensagem_Manager.objects.all()
            mensagemInstance.create(
                user_env = user,
                titulo = titulo,
                mensagem = mensagem,
                status = 'Pendente',
                user_rec = user_get
                
            )
            mensagemManager.create(
                user_env = user,
                titulo = titulo,
                mensagem = mensagem,
                status = 'Pendente',
                user_rec = user_get
                
            )

            
            
            error_message = " "
            context = {
                'mensagens_envi': mensagens_envi,
                'mensagens_rec':mensagens_rec,
                'error_message': error_message,
            }
            return render(request, 'dashboard/mensagens.html', context)
            
        except Exception as e:
            error_message = "Destinatario não encontrado"
            context = {
                'mensagens_envi': mensagens_envi,
                'mensagens_rec':mensagens_rec,
                'error_message': e,
            }
            return render(request, 'dashboard/mensagens.html', context)
    context = {
        'mensagens_envi': mensagens_envi,
        'mensagens_rec':mensagens_rec,
        'error_message': error_message,
        
    }
    return render(request, 'dashboard/mensagens.html', context)



def mudarInfoView(request):
    user = request.user.id
    userInfo = Customuser.objects.get(user=user)
    
    
    context = {
        'userInfo':userInfo,
        }
    
    return render(request, 'dashboard/mudar-informacao.html',context)


def pubAnuncioView(request):
    
    
    categorias = Categoria.objects.all()
    
    if request.method == 'POST':
        tipo_servico = request.POST.get('tipo')
        nome_servico = request.POST.get('nome_servico')
        resume_servico = request.POST.get('resume_servico')
        descricao = request.POST.get('descricao_servico')
        funcao = request.POST.get('funcao_servico')
        categoria =  request.POST.get('categoria_servico')
        tags_servico = request.POST.get('tags_servico')
        imagem_servico = request.FILES.get('fileInput')
        valor_servico = request.POST.get('valorServico')
        valor_decimal = float(valor_servico.replace(',', '.'))
        
        categoria_servico = Categoria.objects.get(nome=categoria)
        if tipo_servico == "servico":
            
            try:
                servicos =  Servico.objects.all()
                servicos.create(
                    usuario = request.user,
                    nome = nome_servico,
                    bv_desc = resume_servico,
                    descricao = descricao,
                    tags = tags_servico,
                    funcao = funcao,
                    imagens_produto = imagem_servico,
                    categoria = categoria_servico,
                    valor = valor_decimal
                )
                                
                return redirect('gerAnuncio')
                
                
            except IntegrityError as e :
            
                error_message = "verifique o campo de " +  str(e)
                context = {"error_message":error_message,
                            'categorias' : categorias, 
                           }    
                return render(request,  'dashboard/publicar-anuncio.html', context)
            
        elif tipo_servico == 'produto':
            
             
            try:
                produto =  Produto.objects.all()
                produto.create(
                    usuario = request.user,
                   nome = nome_servico,
                    bv_desc = resume_servico,
                    descricao = descricao,
                    tags = tags_servico,
                    funcao = funcao,
                    imagem = imagem_servico,
                    categoria = categoria_servico,
                    valor = valor_decimal   
                )
                
                return redirect('gerAnuncio')
                
                
            except IntegrityError as e :
                error_message = "verifique o campo de " + str(e)
                
                context = {"error_message":error_message,
                             'categorias' : categorias, 

                           }    

                return render(request,  'dashboard/publicar-anuncio.html', context)
        
        
    context = {
        'categorias' : categorias, 
        }
        
    
    return render(request, 'dashboard/publicar-anuncio.html', context)


def gerAnuncioView(request):
    
    produtos = Produto.objects.filter(usuario=request.user)
    servicos = Servico.objects.filter(usuario=request.user)

    produtos_servicos = list(produtos) + list(servicos)
    
    
    context = {
        'produtos_servicos' : produtos_servicos,
    }
    return render(request, 'dashboard/gerenciar-anuncios.html', context)

def logoutView (request):
    
    logout(request)
    
    
    return redirect('home')
