from django.shortcuts import render
from .models import *
from django.db.utils import IntegrityError 
from django.contrib.auth import authenticate, login ,  logout
import datetime
from django.shortcuts import render,get_object_or_404, redirect
from .defs import validador_pedido
from django.contrib.auth.models import  Group

# Login Cadastro
def loginView (request):
    
    if request.user.is_authenticated:
        
        if request.user.groups.filter(name='Cliente').exists():
        
            return redirect('home')          
        elif request.user.groups.filter(name='Colaborador').exists():
            
            return redirect('dashboard')           
            

    if request.method == 'POST':
            username = request.POST.get('email')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                    login(request,user)
                    if request.user.groups.filter(name='Cliente').exists():
        
                            return redirect('home')          
                    elif request.user.groups.filter(name='Colaborador').exists():
                            
                        return redirect('dashboard')           
            else :
                    error_messagem = "Email ou Senha não conferem" 
                    return render (request, 'index/login.html', {'error_messagem':error_messagem})
                
    else:
        return render(request, 'index/login.html')
            
            
    return render(request, 'index/login.html')

def cadastroView (request):
    nome  = request.POST.get('nome')
    email = request.POST.get('email') 
    username = request.POST.get('username')
    senha = request.POST.get('senha')
    dataNasc = request.POST.get('dataNasc')
    dataFormat = datetime.datetime.strptime(dataNasc, "%Y-%m-%d")


    if request.method == 'POST':
        user  = User.objects.all()
        customuser = Customuser.objects.all()
        creditos = Credito.objects.all()
        
        try:
            user.create(email=email, password=senha, first_name=nome, username=username)
            user_request = User.objects.get(username=username)
            creditos.create(user= user_request)
            creditos_user = Credito.objects.get(user=user_request)
            
            customuser.create(sobre="", telefone="", creditos=creditos_user, data_nas = dataFormat , user=user_request)
            login(request, user_request)
            
            return redirect('tipo')
            
        except IntegrityError as e :
            print (e)
            context = {'error':str(e)}
            return redirect('dashboard',context)
            
    return redirect('dashboard',context)



# Index


def homeSiteView(request):
    carro_id = request.session.get("carro_id", None)
    
    # Gerenciamento do carrinho de compras
    if carro_id:
        try: 
            carrinho = Carrinho.objects.get(id=carro_id)
        except Carrinho.DoesNotExist:  # Se o carrinho não for encontrado, cria um novo
            carrinho = Carrinho.objects.create()
            request.session['carro_id'] = carrinho.id  # Atualiza o carro_id na sessão
    else:
        # Se não houver carrinho na sessão, cria um novo
        carrinho = Carrinho.objects.create()
        request.session['carro_id'] = carrinho.id
    
    # Contagem de produtos no carrinho
    contagem = Produto_Carrinho.objects.filter(carrinho=carrinho).count()
    produto_carrinho = Produto_Carrinho.objects.filter(carrinho=carrinho)
    
    total_valor = produto_carrinho.aggregate(total=models.Sum('produto__valor'))['total'] 
    # Data atual para filtrar produtos e serviços
    today = datetime.datetime.today().month
    
    # Banner e verificações de grupo de usuários
    imagens_banner = Banner.objects.all()
    
    if request.user.groups.filter(name='Colaborador').exists():
        group = "colaborador"
    elif request.user.groups.filter(name='Cliente').exists():
        group = "clientes"
    else:
        group = 'None'
    
    # Produtos e serviços recentes
    produtos = Anuncio.objects.all()
    produto_recentes = Anuncio.objects.filter(data_adicionada__month=today, tipo="Produto")
    servicos_recentes = Anuncio.objects.filter(data_adicionada__month=today,tipo="Servico")
    creditos = Credito.objects.get(user=request.user)
 
    # Produtos mais visualizados (destaques)
    produto_destaque = Anuncio.objects.filter(visualizacao__gte=100)
    
    context = {
        'group': group,
        'produto_carrinho': produto_carrinho,
        'imagens_banner': imagens_banner,
        'produto_destaque': produto_destaque,
        'Produtos': produtos,
        'produto_recentes': produto_recentes,
        'contagem': contagem,
        'servicos_recentes': servicos_recentes,
        'carro_id': carro_id,
        'creditos':creditos,
        'total_valor':  total_valor, 
    }
    
    return render(request, 'index/index.html', context)



def listaProdutosView (request):
    if request.user.groups.filter(name='Colaborador').exists():
        
        group = "colaborador"
        
    elif request.user.groups.filter(name='Cliente').exists():
        group= 'clientes'
    else: 
        group = 'None'
    
     
    carro_id = request.session.get("carro_id", None)
            
    if carro_id:
        carro_id = Carrinho.objects.get(id=carro_id)
    else:
        carro_id = None
        
    contagem = Produto_Carrinho.objects.filter(carrinho= carro_id).count()
    produtos = Anuncio.objects.all()
    categorias = Categoria.objects.all()
    # produtosD = Anuncio.objects.filter()
    produto_carrinho = Produto_Carrinho.objects.filter(carrinho=carro_id)
    total_valor = produto_carrinho.aggregate(total=models.Sum('produto__valor'))['total'] 
    
    
    context = { 
            'categorias':categorias,
            'produtos' :produtos,
            'group' :group,
            'contagem':contagem,
            'produto_carrinho':produto_carrinho,
            'total_valor' : total_valor,
            }
    
    return render(request, 'index/lista-produtos.html', context)



def produtoView(request, id):
    
    produto = Anuncio.objects.get(id=id)
    produto.visualizacao += 1 
    produto.save()
    comentarios = Comentario.objects.filter(produto=produto) # adicionar imagem do usuario no comentraio 
      
    carro_id = request.session.get("carro_id", None)
            
    if carro_id:
        carro_id = Carrinho.objects.get(id=carro_id)
    else:
        carro_id = None
        
    contagem = Produto_Carrinho.objects.filter(carrinho= carro_id).count()
     
    produtosRelacionados = Anuncio.objects.filter(categoria = produto.categoria)
    produto_carrinho = Produto_Carrinho.objects.filter(carrinho=carro_id)
    total_valor = produto_carrinho.aggregate(total=models.Sum('produto__valor'))['total'] 
    try:
        credito = Credito.objects.filter(user=request.user)
        
   
        context = {
        'produto': produto,
        'comentarios': comentarios,
        'produtosRelacionados': produtosRelacionados,
        'contagem':contagem,
        'produto_carrinho':produto_carrinho,
        'total_valor':total_valor,
        'creditos':credito,
        
        }
        return render(request, 'index/produto.html', context)
    except :
        context = {
            'produto': produto,
            'comentarios': comentarios,
            'produtosRelacionados': produtosRelacionados,
            'contagem':contagem,
            'produto_carrinho':produto_carrinho,
            'total_valor':total_valor,
            
            }
        return render(request, 'index/produto.html', context)



def listaCategoriaView (request, categoria):
    produtos = Anuncio.objects.filter(categoria=categoria)
  
    carro_id = request.session.get("carro_id", None)
            
    if carro_id:
        carro_id = Carrinho.objects.get(id=carro_id)
    else:
        carro_id = None
        
    contagem = Produto_Carrinho.objects.filter(carrinho= carro_id).count()

    context = {
        'produtos': produtos,
        'contagem':contagem,
    }

    return render(request, 'index/lista_produtos.html', context)

def servicosView (request,id):
     
    produto = Anuncio.objects.get(id=id)
    produto.visualizacao += 1 
    produto.save()
    comentarios = Comentario.objects.filter(servico=produto) # adicionar imagem do usuario no comentraio 
      
    carro_id = request.session.get("carro_id", None)
            
    if carro_id:
        carro_id = Carrinho.objects.get(id=carro_id)
    else:
        carro_id = None
        
    contagem = Produto_Carrinho.objects.filter(carrinho= carro_id).count()
     
    produtosRelacionados = Anuncio.objects.filter(categoria = produto.categoria)
   
   
    if request.user.groups.filter(name='Colaborador').exists():
        
        group = "colaborador"
        
    elif request.user.groups.filter(name='Cliente').exists():
        group= 'clientes'
    else: 
        group = 'None'
        
    carro_id = request.session.get('carro_id', None)
    
    if carro_id:
        carro_id = Carrinho.objects.get(id=carro_id)
    else:
        carro_id = None
        
    contagem = Produto_Carrinho.objects.filter(carrinho= carro_id).count()
    categorias = Categoria.objects.all()
    # produtosD = Anuncio.objects.filter()
    
    try:
        
        credito = Credito.objects.filter(user=request.user)
        context = { 
                'categorias':categorias,
                'produto' :produto,
                'group' :group,
                'comentarios': comentarios,
                'produtosRelacionados': produtosRelacionados,
                'contagem':contagem,
                'credito':credito,
                
                }
        
        return render(request, 'index/produto.html', context)
    except:
        context = { 
                'categorias':categorias,
                'produto' :produto,
                'group' :group,
                'comentarios': comentarios,
                'produtosRelacionados': produtosRelacionados,
                'contagem':contagem,
                
                }
        
        return render(request, 'index/produto.html', context)
    


def listaServicosView (request):
    
    if request.user.groups.filter(name='Colaborador').exists():
        
        group = "colaborador"
        
    elif request.user.groups.filter(name='Cliente').exists():
        group= 'clientes'
    else: 
        group = 'None'
     
    carro_id = request.session.get("carro_id", None)
            
    if carro_id:
        carro_id = Carrinho.objects.get(id=carro_id)
    else:
        carro_id = None
        
    contagem = Produto_Carrinho.objects.filter(carrinho= carro_id).count()
    servicos = Anuncio.objects.filter(tipo='servico')
    categorias = Categoria.objects.all()
    # produtosD = Anuncio.objects.filter()
    context = { 
            'categorias':categorias,
            'servicos' :servicos,
            'group' :group,
            'contagem':contagem
            }
    
    return render(request, 'index/lista-servicos.html', context)



def categoriaView (request, cat):
    
    if request.user.groups.filter(name='Colaborador').exists():
        
        group = "colaborador"
        
    elif request.user.groups.filter(name='Cliente').exists():
        group= 'clientes'
    else: 
        group = 'None'
     
    carro_id = request.session.get("carro_id", None)
            
    if carro_id:
        carro_id = Carrinho.objects.get(id=carro_id)
    else:
        carro_id = None
        
    contagem = Produto_Carrinho.objects.filter(carrinho= carro_id).count()
    servicos = Anuncio.objects.filter(categoria__nome= cat, tipo="Servico")
    produtos = Anuncio.objects.filter(categoria__nome= cat)
    categorias = Categoria.objects.all()
    # produtosD = Anuncio.objects.filter()
    context = { 
            'categorias':categorias,
            'servicos' :servicos,
            'produtos' :produtos,
            'group' :group,
            'contagem':contagem
            }
    
    return render(request, 'index/categorias.html', context)

def comentarioView(request, tipo):
    
    if request.method == 'POST':
        user = request.user
        comentario = request.POST.get('comentario')
        objeto = request.POST.get('objeto')
        usuario = request.POST.get('usuario')
        avaliacao = request.POST.get('inputStar')
        customuser = Customuser.objects.get(user=user)
        
        coments = Comentario.objects.all()
        
        if  Anuncio.objects.get(usuario=usuario.username, tipo= tipo):
            
            try:
            
                coments = Comentario.objects.create(
                    user = user,
                    comentario = comentario,
                    produto = objeto,
                    avaliacao = avaliacao,
                    customuser = customuser
                )
                
                coments.save()
                print("produto")
                return redirect('produto',)
            except IntegrityError as e:
                print(str(e))
                
                return redirect('home')
        
        elif Anuncio.objects.get(usuario=usuario.username, tipo= tipo):
            try:
            
                coments = Comentario.objects.create(
                user = user,
                comentario = comentario,
                servico = objeto,
                avaliacao = avaliacao,
                customuser = customuser
            )
                
                coments.save() 
                print("servico")
                
                return redirect('servicos', id_obj)
            
            except IntegrityError as e:
                print(str(e))
                return redirect('home')
        print("algo")
    return redirect('lista-servicos')

    
def homeView (request):
    
    if  request.user.groups.filter(name='Colaborador').exists():
        
        group = "colaborador"
        
    elif request.user.groups.filter(name='Cliente').exists():
        group= 'clientes'
    else: 
        group = 'None'
    context = {'group':group}
    
    return render(request, 'dashboard/index.html',context)

def tipoView (request):
    
    return render(request, 'index/tipoConta.html')

def groupsCliente (request):

    user = User.objects.get(username=request.user.username)
    grupo = Group.objects.get(name="Cliente")
    user.groups.add(grupo)
    
    return redirect('home')

def groupsColaborador (request):
    
    
    user = User.objects.get(username=request.user.username)
    grupo = Group.objects.get(name="Colaborador")
    user.groups.add(grupo)
    
    return redirect('dashboard')



def meuPerfilView(request):
    
    if  request.user.groups.filter(name='Colaborador').exists():
        
        group = "colaborador"
        
    elif request.user.groups.filter(name='Cliente').exists():
        group= 'clientes'
    else: 
        group = 'None'
    context = {'group':group}
    
    return render(request, 'dashboard/meu-servico.html', context)



def dashboardView (request):
    
    now=  datetime.datetime.now()

    try:
        user = Customuser.objects.get(user=request.user)    
        
    except :
        return redirect('mudarInfo') 
    creditos = user.creditos
    produtos_vendidos = Anuncio.objects.filter(usuario=request.user.id, vendas=1).count()
    produtos = Anuncio.objects.filter(usuario=request.user).count()

    produtos_servicos = produtos 

    valorTotal = Anuncio.objects.filter(usuario=request.user.id)
    # ultimas_vendas = Anuncio.objects.filter(usuario=request.user.id, date__month=now.month)
    
    if valorTotal:
        
        for i in valorTotal:
            total =+ i.valor
    total = 0
            
    if  request.user.groups.filter(name='Colaborador').exists():
        
        group = "colaborador"
        
    elif request.user.groups.filter(name='Cliente').exists():
        group= 'clientes'
    else: 
        group = 'None'
    
    
                
    context = {
        # 'ultimas_vendas':ultimas_vendas,
        'valorTotal': total,
        'creditos' : creditos, 
        'produtos_vendidos':produtos_vendidos,
        'produtos_servicos':produtos_servicos,
        'customuser': user,
        'group':group,
    }    
    return render(request, 'dashboard/index.html',context)



def minhaContaView(request):
    user = User.objects.get(id=request.user.id)
    userInfo = Customuser.objects.get(user=user)
    creditos = Credito.objects.get(user=user)
    error_messages = " "
    if  request.user.groups.filter(name='Colaborador').exists():
        
        group = "colaborador"
        
    elif request.user.groups.filter(name='Cliente').exists():
        group= 'clientes'
    else: 
        group = 'None'
    
    
    
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
            'group':group,
            'creditos':creditos,
            
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
                    'creditos':creditos,
                    'error_message': error_messages,
                    'group':group
                    
                    }
            
                
                return render(request, 'dashboard/minha-conta.html',context)
            except IntegrityError as e :
                
                context = {
                    'userInfo':userInfo,
                    'error_message': e,
                    'group':group,
                    'creditos':creditos,
                    
                    }
                return render(request, 'dashboard/minha-conta.html',context)
            
        
    
    context = {
        'userInfo':userInfo,
        'error_message': error_messages,
        'group':group,
        'creditos':creditos,
         
        }
    
    return render(request, 'dashboard/minha-conta.html',context)



def mensagensView(request):
    user = User.objects.get(id=request.user.id)
    mensagemInstance = Mensagen.objects.all()
    mensagens_envi = Mensagen.objects.filter(user_env=user)
    mensagens_rec = Mensagem_Manager.objects.filter(user_rec=user, status= "Confirmada")
    error_message = " "
    if  request.user.groups.filter(name='Colaborador').exists():
        
        group = "colaborador"
        
    elif request.user.groups.filter(name='Cliente').exists():
        group= 'clientes'
    
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
                'group':group
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
        'group':group
        
        
    }
    return render(request, 'dashboard/mensagens.html', context)



def mudarInfoView(request):
    user = request.user.id
    userInfo = Customuser.objects.get(user=user)
    if  request.user.groups.filter(name='Colaborador').exists():
        
        group = "colaborador"
        
    elif request.user.groups.filter(name='Cliente').exists():
        group= 'clientes'

    
    
    context = {
        'userInfo':userInfo,
        'group':group,
        }
    
    return render(request, 'dashboard/mudar-informacao.html',context)


def editAnuncioView (request,idObj):
    user = request.user
    if request.method == "POST":
       
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
        valor_comissao =  valor_decimal * 0.10
        valor_final = valor_decimal + valor_comissao
        categoria_servico = Categoria.objects.get(nome=categoria)
        
        anuncio = Anuncio.objects.get(id=idObj)
        anuncio.nome = nome_servico
        anuncio.bv_desc = resume_servico
        anuncio.descricao = descricao
        anuncio.funcao = funcao
        anuncio.tags = tags_servico
        anuncio.imagem = imagem_servico
        anuncio.categoria  = categoria_servico
        anuncio.valor = valor_final
        anuncio.tipo = tipo_servico
        anuncio.save
        
        return redirect ('gerAnuncio')
    try:
        produto = Anuncio.objects.get(id=idObj)
        categorias = Categoria.objects.all()
        context = {
            'produto':produto,
            'categorias':categorias,
            
        }
        return render(request,"dashboard/editar-anuncio.html", context)
    except IntegrityError as e:
        print(str(e))
        return redirect('gerAnuncio')
        

def pubAnuncioView(request):
    
    
    categorias = Categoria.objects.all()
    if  request.user.groups.filter(name='Colaborador').exists():
        
        group = "colaborador"
        
    elif request.user.groups.filter(name='Cliente').exists():
        group= 'clientes'

    
    
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
        valor_comissao =  valor_decimal * 0.10
        valor_final = valor_decimal + valor_comissao
        print (valor_final)
        
        categoria_servico = Categoria.objects.get(nome=categoria)
        if tipo_servico == "servico":
            
            try:
                servicos =  Anuncio.objects.all()
                servicos.create(
                    usuario = request.user,
                    nome = nome_servico,
                    bv_desc = resume_servico,
                    descricao = descricao,
                    tags = tags_servico,
                    funcao = funcao,
                    imagem = imagem_servico,
                    categoria = categoria_servico,
                    valor = valor_final,
                    tipo = "Servico"
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
                produto =  Anuncio.objects.all()
                produto.create(
                    usuario = request.user,
                   nome = nome_servico,
                    bv_desc = resume_servico,
                    descricao = descricao,
                    tags = tags_servico,
                    funcao = funcao,
                    imagem = imagem_servico,
                    categoria = categoria_servico,
                    valor = valor_final,
                    tipo = "Produto"
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
    
    produtos = Anuncio.objects.filter(usuario=request.user, tipo="Produto")
    servicos = Anuncio.objects.filter(usuario=request.user, tipo="Servico")

    produtos_servicos = list(produtos) + list(servicos)
    
    if  request.user.groups.filter(name='Colaborador').exists():
        
        group = "colaborador"
        
    elif request.user.groups.filter(name='Cliente').exists():
        group= 'clientes'

    
    
    
    context = {
        'group':group,
        'produtos_servicos' : produtos_servicos,
    }
    return render(request, 'dashboard/gerenciar-anuncios.html', context)

def logoutView (request):
    
    logout(request)
    
    
    return redirect('home')


#################### FINALIZAÇÃO DE COMPRA ###########################


def carrinho_add (request, id):    
    produto = get_object_or_404(Anuncio, id=id)
    carro_id = request.session.get("carro_id", None)
 
    
    if carro_id :
        carro_obj = Carrinho.objects.get(id=carro_id)
        produto_no_carrinho = carro_obj.produto_carrinho_set.filter(produto=produto)        
        if produto_no_carrinho.exists():    
            carroProduto= produto_no_carrinho.last()
            carroProduto.quantidade += 1
            carroProduto.subtotal = produto.valor
            carroProduto.save()
            carro_obj.total += produto.valor
            carro_obj.save()
            
        else:
            carroProduto = Produto_Carrinho.objects.create(carrinho = carro_obj,produto = produto, avaliacao   = produto.avaliacao,  quantidade  = 1, subtotal=produto.valor)
            carro_obj.total += produto.valor
            carro_obj.save()
        
            
    else:
        carro_obj = Carrinho.objects.create(total= 0)
        request.session["carro_id"]=carro_obj.id
        carroProduto = Produto_Carrinho.objects.create(carrinho    = carro_obj,produto     = produto, avaliacao   = produto.valor,  quantidade  = 1,           subtotal=produto.valor)
        carro_obj.total += produto.valor
        carro_obj.save()
        
   
    return redirect('produto',id)


def carrinho (request): 
    carro_id = request.session.get('carro_id',None)

    # Gerenciamento do carrinho de compras
    if carro_id:
        try: 
            carrinho = Carrinho.objects.get(id=carro_id)
        except Carrinho.DoesNotExist:  # Se o carrinho não for encontrado, cria um novo
            carrinho = Carrinho.objects.create()
            request.session['carro_id'] = carrinho.id  # Atualiza o carro_id na sessão
    else:
        # Se não houver carrinho na sessão, cria um novo
        carrinho = Carrinho.objects.create()
        request.session['carro_id'] = carrinho.id

        
    produtos = Produto_Carrinho.objects.filter(carrinho=carro_id)
    valorTotal = produtos.aggregate(total=models.Sum('produto__valor'))['total'] 
    contagem = Produto_Carrinho.objects.filter(carrinho= carro_id).count()
    creditos = Credito.objects.get(user=request.user)
   
           
    context = { 
        'carro':carro_id,
        'produtos': produtos, 
        'valorTotal': valorTotal, 
        'contagem': contagem,
        'creditos' :creditos,
    }
       
    return render (request, 'index/carrinho.html', context)   

def limparCarrinhoView (request,):

    carro_id = request.session.get("carro_id", None)
            
    if carro_id:
        carro_id = Carrinho.objects.get(id=carro_id)
    else:
        carro_id = None
    
    carro_id.delete()
    return redirect('carrinho')


def quantidadeView (request,idObj, desc):
    
    carro_id = request.session.get("carro_id", None)
    produto =  Produto_Carrinho.objects.get(carrinho= carro_id, id=idObj)
    
    if desc == "inc" : #increment
        produto.quantidade += 1
        produto.save()
        return redirect ("carrinho")
    elif desc == "dec" : # decrement
        produto.quantidade -=1
        produto.save()
        
        if produto.quantidade < 1:
            print("entrou")
            produto.delete()
            return redirect('carrinho')
        produto.save()
        return redirect('carrinho') 
    
    return redirect('carrinho')
    
        
def deleteView (request,idObj):

    carro_id = request.session.get("carro_id", None)
            
    if carro_id:
        carrinho = Produto_Carrinho.objects.get(carrinho= carro_id, id = idObj)
        carrinho.delete()
    else:
        carro_id = None
    

    
    return redirect('carrinho')


def checkoutView (request):
    
    user = request.user
    user_custom = Customuser.objects.get(user=user.id)
    carro_id = request.session.get("carro_id", None)
    carrinho =  Produto_Carrinho.objects.filter(carrinho=carro_id)
    contagem = Produto_Carrinho.objects.filter(carrinho=carro_id).count()
    
    context = {
        'user' :user,
        'customUser':user_custom,
        'carrinho': carrinho,   
        'contagem' : contagem,
        
    }
    
    return render(request, 'index/checkout.html', context)

def pagamentoView (request):
    
    user = request.user
    user_custom = Customuser.objects.get(user=user.id)
    carro_id = request.session.get("carro_id", None)
    carrinho =  Produto_Carrinho.objects.filter(carrinho=carro_id)
    contagem = Produto_Carrinho.objects.filter(carrinho=carro_id).count()
    carrinho_total = Carrinho.objects.get(id=carro_id)
    creditos = Credito.objects.get(user=user)
    
    context = {
        'user' :user,
        'customUser':user_custom,
        'carrinho': carrinho,   
        'contagem' : contagem,
        'carrinho_total':carrinho_total,
        'creditos':creditos
        
    }
    
    return render(request, 'index/pagamento.html', context)


def pedidosView (request):
    
    user = request.user
    pedido = Pedido.objects.all()
    carro_id = request.session.get("carro_id", None)
    creditos_usuario = Credito.objects.get(user=user)
    carrinho_total = Carrinho.objects.get(id=carro_id)
    produtos_carrinho = Produto_Carrinho.objects.filter(carrinho=carro_id)
    
    if request.method =="POST":
        
        if  creditos_usuario.valor < carrinho_total.total:
            
            
            error = "Creditos Insuficientes"
            
            context = {
                'error' : error,
            }
            return render(request, 'index/pagamento2.html', context )
            
        
        try :
            
            creditos_usuario.valor_antigo = creditos_usuario.valor
            creditos_usuario.valor = creditos_usuario.valor - carrinho_total.total
            creditos_usuario.save()

            pedido.create(
                user_remetente = user,
                valor_carrinho = carrinho_total.total,
                carrinho = carrinho_total,
                status = "Pendente"
            
            ) 
            ultimo_pedido = Pedido.objects.get(user_remetente =user, carrinho__id=carrinho_total.id)   
            validador_pedido(ultimo_pedido.id)
                
            
            produtos_carrinho.delete()
            carrinho_total.delete()
            
        except IntegrityError as e:
            print(str(e))
            error = str(e)
            context = {
                'error' : error,
            }
            return render(request, 'index/pedidos.html', context )
            
        pedidos = Pedido.objects.filter(user_remetente= user)
        context = {
            'carrinho_total':carrinho_total,
            'pedidos' : pedidos,
            'creditos': creditos_usuario,
        }
        
        return render(request, 'index/pedidos.html', context )
    else :
        pedidos = Pedido.objects.filter(user_remetente= user)
        context = {
            'carrinho_total':carrinho_total,
            'pedidos' : pedidos,
            
        }
        
        return render(request, 'index/pedidos.html', context )