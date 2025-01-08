from django.shortcuts import render
from .models import *
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login ,  logout
import datetime
from django.shortcuts import render,get_object_or_404, redirect
from .defs import *
from django.contrib.auth.models import  Group
import datetime
import uuid
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode,  urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str

# Login Cadastro
def loginView (request):
    
    if request.user.is_authenticated:        
            return redirect('dashboard')           
            

    if request.method == 'POST':
        username_or_email = request.POST.get('email')
        password = request.POST.get('password')

        # Primeira tentativa de autenticação direta
        user = authenticate(username=username_or_email, password=password)

        if user is None:  
            try:
                user_model = User.objects.get(email=username_or_email)
                user = authenticate(username=user_model.username, password=password)
                print(user)     
                if user:
                    pass
                else:
                    return render(request, 'index/login.html', {'error_messagem': "Credenciais inválidas"})

                try:
                    user_last = Confiabilidade.objects.get(user=user_model)
                    user_last.ultimo_acesso = user_model.last_login
                    user_last.save()
                except Confiabilidade.DoesNotExist:
                    pass

            except User.DoesNotExist:
                return render(request, 'index/login.html', {'error_messagem': "Usuário não encontrado"})
            except User.MultipleObjectsReturned:
                return render(request, 'index/login.html', {'error_messagem': "Vários usuários encontrados com este email"})
            except IntegrityError as e:
                return render(request, 'index/login.html', {'error_messagem': "Erro de integridade: " + str(e)})

        
        login(request, user)
        return redirect('dashboard')

    
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
        confi = Confiabilidade.objects.all()
        
        try:
            user.create(email=email, password=senha, first_name=nome, username=username)
            user_request = User.objects.get(username=username)
            creditos.create(user= user_request)
            creditos_user = Credito.objects.get(user=user_request)
            confi.create(user=user_request,) 
            customuser.create(sobre="", telefone="", creditos=creditos_user, data_nas = dataFormat , user=user_request)
            login(request, user_request)
            
            return redirect('dashboard')
            
        except IntegrityError as e :
            error_message = str(e)
            if "UNIQUE constraint failed: user_username" in error_message:
                context = {'error': 'Esse USERNAME já existe.Por favor escolha outro.'}
            else:
                context = {'error': 'Ocorreu algum errou. Por favor, Tente mais tarde.'}
            return redirect('dashboard', context)
                            
    return redirect('dashboard',context)



# Index


def homeSiteView(request):
    carro_id = request.session.get("carro_id", None)
    contador_prazo()
    
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
    
   
    
    # Produtos e serviços recentes
    produtos = Anuncio.objects.all()
    produto_recentes = Anuncio.objects.filter(data_adicionada__month=today, tipo="Produto")
    servicos_recentes = Anuncio.objects.filter(data_adicionada__month=today,tipo="Servico")
    produto_destaque = Anuncio.objects.filter(visualizacao__gte=100)
    user = request.user

    if user.is_authenticated:
        
        creditos = Credito.objects.get(user=request.user)
 
        # Produtos mais visualizados (destaques)
        
        context = {
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
    else:
        context = {
            'produto_carrinho': produto_carrinho,
            'imagens_banner': imagens_banner,
            'produto_destaque': produto_destaque,
            'Produtos': produtos,
            'produto_recentes': produto_recentes,
            'contagem': contagem,
            'servicos_recentes': servicos_recentes,
            'carro_id': carro_id,
            'total_valor':  total_valor, 
        }
        
        return render(request, 'index/index.html', context)
    
def pesquisarView(request):
    produto_pesquisa = request.POST.get('procurar')
    
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


    contagem = Produto_Carrinho.objects.filter(carrinho=carrinho).count()
    produto_carrinho = Produto_Carrinho.objects.filter(carrinho=carrinho)
    total_valor = produto_carrinho.aggregate(total=models.Sum('produto__valor'))['total'] 
    credito = Credito.objects.get(user=request.user)
    
    
    if request.method == "POST":
        anuncios = Anuncio.objects.filter(nome__icontains=produto_pesquisa)
        categorias = Categoria.objects.filter(nome__icontains=produto_pesquisa)
        
    
    if anuncios.exists():
        context = {
            'anuncios': anuncios,
            'error_messages': None,
            'produto_carrinho':produto_carrinho,
            'contagem':contagem,
            'total_valor':total_valor, 
            'creditos':credito,
        }
    elif categorias.exists():
        anuncios_por_categoria = Anuncio.objects.filter(categoria__in=categorias)
        contagem = Produto_Carrinho.objects.filter(carrinho=carrinho).count()
        produto_carrinho = Produto_Carrinho.objects.filter(carrinho=carrinho)
        context = {
            'anuncios': anuncios_por_categoria,
            'error_messages': None,
            'produto_carrinho':produto_carrinho,
            'total_valor':total_valor,
            'creditos':credito,
            'contagem':contagem,
        }
    else:
        context = {
            'anuncios': None,
            'error_messages': "Nenhum produto encontrado",
            'produto_carrinho':produto_carrinho,
            'total_valor':total_valor,
            'creditos':credito,
            'contagem':contagem, 
        }

    # Renderizar o template com o contexto
    return render(request, 'index/pesquisa.html', context)

    


def listaProdutosView (request):

    
     
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
    creditos = Credito.objects.get(user=request.user)
    
    context = { 
            'categorias':categorias,
            'produtos' :produtos,
            'contagem':contagem,
            'produto_carrinho':produto_carrinho,
            'total_valor' : total_valor,
            'creditos':creditos,
            }
    
    return render(request, 'index/lista-produtos.html', context)



def produtoView(request, id):
    
    produto = Anuncio.objects.get(id=id)
    produto.visualizacao += 1 
    produto.save()
    comentarios = Comentario.objects.filter(produto=produto) # adicionar imagem do usuario no comentraio 
    user_produto = Customuser.objects.get(user=produto.usuario)  
      
    carro_id = request.session.get("carro_id", None)
            
    if carro_id:
        carro_id = Carrinho.objects.get(id=carro_id)
    else:
        carro_id = None


    avaliacao_permissao = Pedido.objects.filter(user_remetente=request.user.id, carrinho_str__icontains=produto.nome)
    
    if  avaliacao_permissao:
        avaliacao = "habilitado"
    else:
        avaliacao = "desabilitado"
    contagem = Produto_Carrinho.objects.filter(carrinho= carro_id).count()
     
    produtosRelacionados = Anuncio.objects.filter(categoria = produto.categoria)
    produto_carrinho = Produto_Carrinho.objects.filter(carrinho=carro_id)
 
    total_valor = carro_id.total
    try:
        credito = Credito.objects.get(user=request.user)
        
        context = {
        'produto': produto,
        'comentarios': comentarios,
        'produtosRelacionados': produtosRelacionados,
        'contagem':contagem,
        'produto_carrinho':produto_carrinho,
        'total_valor':total_valor,
        'creditos':credito,
        'user_produto':user_produto,
        'avaliacao':avaliacao,
        
    
        
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
             'user_produto':user_produto,
                'avaliacao':avaliacao,
             
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
   
   

        
    carro_id = request.session.get('carro_id', None)
    
    if carro_id:
        carro_id = Carrinho.objects.get(id=carro_id)
    else:
        carro_id = None
        
    contagem = Produto_Carrinho.objects.filter(carrinho= carro_id).count()
    categorias = Categoria.objects.all()

    
    try:
        
        credito = Credito.objects.filter(user=request.user)
        context = { 
                'categorias':categorias,
                'produto' :produto,
                'comentarios': comentarios,
                'produtosRelacionados': produtosRelacionados,
                'contagem':contagem,
                'creditos':credito,
                
                }
        
        return render(request, 'index/produto.html', context)
    except:
        context = { 
                'categorias':categorias,
                'produto' :produto,
                'comentarios': comentarios,
                'produtosRelacionados': produtosRelacionados,
                'contagem':contagem,
                
                }
        
        return render(request, 'index/produto.html', context)
    


def listaServicosView (request):
    

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
            'contagem':contagem
            }
    
    return render(request, 'index/lista-servicos.html', context)



def categoriaView (request, cat):

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
            'contagem':contagem
            }
    
    return render(request, 'index/categorias.html', context)

def comentarioView(request, id_produto):
    
    if request.method == 'POST':
        usercustom = Customuser.objects.get(user= request.user)
        comentario = request.POST.get('comentario')
        avaliacao = request.POST.get('inputStar')
        produto = Anuncio.objects.get(id=id_produto)
        coments = Comentario.objects.all()
        
       
            
        try:
            
                coments.create(
                    user = request.user,
                    comentario = comentario,
                    produto = produto,
                    avaliacao = int(avaliacao),
                    customUser = usercustom 
                )
                
                media_avaliacao(produto, int(avaliacao))
                return redirect('produto',id_produto)
        except IntegrityError as e:
                print(str(e))
                
                return redirect('home')
        
        
    return redirect('produto',id_produto)


    
def homeView (request):
    
 
    
    return render(request, 'dashboard/index.html',)



def meuPerfilView(request):
    

    
    return render(request, 'dashboard/meu-servico.html',)

# Dashboard 

def dashboardView (request):
    
    
    try:
        user = Customuser.objects.get(user=request.user)    
        
    except :
        return redirect('mudarInfo') 
    
    try: 
        extrato = Transacoes.objects.filter(user=request.user)
        
    except:
        extrato = None
        
        pass
    creditos = user.creditos
    produtos_vendidos = Anuncio.objects.filter(usuario=request.user.id, vendas=1).count()
    meus_anuncios = Anuncio.objects.filter(usuario=request.user) 
    ultimas_vendas = []
    month = datetime.datetime.now()
    for i in meus_anuncios:
        vendas = Pedido.objects.filter(carrinho_str__icontains=i.nome, date__month=month.month, status_pedido= "Concluida" )
        ultimas_vendas.append(vendas)
    total_vendas = len(ultimas_vendas)
    valorTotal = Anuncio.objects.filter(usuario=request.user.id)
    
    if valorTotal:
        
        for i in valorTotal:
            total =+ i.valor
    total = 0
    pedidos = Pedido.objects.filter(user_remetente=request.user)  # Filtrar anúncios do usuário

    context = {
        'total_vendas':total_vendas,
        'valorTotal': total,
        'creditos' : creditos, 
        'produtos_vendidos':produtos_vendidos,
        'pedidos':pedidos,
        'customuser': user,
        'anuncios':meus_anuncios,
        'extrato':extrato,
    }    
    return render(request, 'dashboard/index.html',context)

def pedidoIdView (request, id):
    pedidos =  Pedido.objects.get(id=id)
    carrinho_str = pedidos.carrinho_str
    caracteres_remover = '{}[]""'
    texto_limpo = carrinho_str
    context = {
        'pedidos':pedidos,
        'texto_limpo':texto_limpo
        
    }
    return render(request, 'dashboard/pedido.html', context)
    

def minhaContaView(request):
    user = User.objects.get(id=request.user.id)
    userInfo = Customuser.objects.get(user=user)
    creditos = Credito.objects.get(user=user)
    user_confiabilidade = Confiabilidade.objects.get(user=user)
    error_messages = " " 
    email_confirm = user_confiabilidade.email
    doc_confirm = user_confiabilidade.imagemDoc

    if request.method == 'POST':
      
        username = request.POST.get('username')
        telefone = request.POST.get('telefone')
        sobre = request.POST.get('sobre')
        imagem = request.FILES.get('fileInput')
        documento = request.FILES.get('DocInput')
      
        error_messages = None

        if username and username != request.user.username:
            try:
            
                if User.objects.filter(username=username).exists():
                    error_messages = "Já existe um usuário com esse username"
                else:
                    user.username = username
                    user.save()
            except IntegrityError:
                error_messages = "Erro ao salvar o username"

    
            if telefone:
                userInfo.telefone = telefone

            if sobre:
                userInfo.sobre = sobre

            if imagem:
                userInfo.imagem = imagem

            if documento:
                try:
                    user_confiabilidade.imagemDoc = documento
                    validador_doc(documento, user)  
                    user_confiabilidade.save()
                except Exception as e:
                    error_messages = f"Erro ao salvar documento: {e}"

        
            if not error_messages:
                userInfo.save()

    
            context = {
                'userInfo': userInfo,
                'creditos': creditos,
                'error_message': error_messages,
            }

            return render(request, 'dashboard/minha-conta.html', context)

        else:
                try :
                        userInfo.telefone=telefone,
                        userInfo.sobre=sobre,
                        userInfo.imagem=imagem
                        user_confiabilidade.imagemDoc = documento
                        validador_doc(documento, user)
                        user_confiabilidade.save()
                        userInfo.save()
                        context = {
                            'userInfo':userInfo,
                            'creditos':creditos,
                            'error_message': error_messages,
                            }
                    
                        
                        return render(request, 'dashboard/minha-conta.html',context)
                except IntegrityError as e :
                        
                        context = {
                            'userInfo':userInfo,
                            'error_message': e,
                
                            'creditos':creditos,
                            
                            }
                        return render(request, 'dashboard/minha-conta.html',context)
                    
    
    context = {
            'userInfo':userInfo,
            'error_message': error_messages,
            'creditos':creditos,
            'email_confrim': email_confirm,
            'doc_confirm': doc_confirm,
            
            }
        
    return render(request, 'dashboard/minha-conta.html',context)


def confirmaEmailView (request):

    try:
            user = User.objects.get(email=request.user.email)
            token, created = EmailToken.objects.get_or_create(user=user)
            if not created:
                token.token = uuid.uuid4()
                token.created_at = timezone.now()
                token.save()

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token_url = reverse('auth_email', kwargs={'uidb64': uidb64, 'token': str(token.token)})
            link = request.build_absolute_uri(token_url)

            send_mail(
                'Seu link de autenticação',
                f'Clique no link para Verificar seu email e fazer login: {link}',
                'gleydevelopment@gleydevelopment.com',
                [request.user.email],
                fail_silently=False,
            )
            
            message = "Uma mensagem foi enviada para o seu email, Clique no link para concluir a verificação de email."
            context = {
                'user': user,
                'message': message,
            }
            
            return render(request, 'email/send_email.html',context)
        
    except User.DoesNotExist:
        
            message = "E-mail não registrado"
            context = {
                'user': user,
                'message': message,
        
            }
        
            return render(request, 'email/send_email.html', context)

def authenticate_via_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        email_token = EmailToken.objects.get(user=user, token=token)
        confiabilidade = Confiabilidade.objects.get(user=user) 

        if email_token.is_valid():
            confiabilidade.nivel_confiavel += 1
            login(request, user)
            email_token.delete()
            return redirect('home') 
        else:
            return render(request, 'index/reset_token_invalido.html', {'error_message': 'O token nao e valido, por favor tente novamente'})
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, EmailToken.DoesNotExist):
        return render(request, 'index/reset_token_invalido.html')



def comprasView (request):
    
    user = request.user
    
    compras = Pedido.objects.filter(user_remetente=user,status_pedido="Concluida")
    
    
    context = {
        'pedido' : compras, 
        
    }
    
    return render(request, 'dashboard/compras.html', context)




def mensagensView(request):
    user = User.objects.get(id=request.user.id)
    mensagemManager = Mensagem_Manager.objects.all()
    mensagens_envi = Mensagem_Manager.objects.filter(user_env=user)
    mensagens_rec = Mensagen.objects.filter(user_rec=user, status="Recebida")

    mensagens= [] 
    
    for i in mensagens_envi:
            try:
                message = Mensagem_Manager.objects.filter(user_env=user)
                mensagens.extend(message)  
            except :
                pass
    for i in mensagens_rec:
            try:
                message =  Mensagen.objects.filter(user_rec=user, status="Recebida")
                mensagens.extend(message)  
            except :
                pass
          
          
        
    
    error_message = " "
  
    if request.method == 'POST':
        user_rec = request.POST.get('user_rec')
        mensagem =  request.POST.get('mensagem')
        titulo =  request.POST.get('titulo')
        
        try:
            user_receber = User.objects.get(username=user_rec)
            print(user_receber)
            mensagemManager.create(
                user_env = user,
                titulo = titulo,
                mensagem = mensagem,
                status = 'Pendente',
                user_rec = user_receber
                
            )
            
            ultima_mensagem = Mensagem_Manager.objects.all().last()
            veri_mensagem(ultima_mensagem)
            
            error_message = " "
            context = {
                'mensagens':mensagens,
                'error_message': error_message,
           
           
            }
            return render(request, 'dashboard/mensagens.html', context)
            
        except Exception as e:
            error_message = "Destinatario não encontrado"
            context = {
                'mensagens':mensagens,
                'error_message': e,
                
            }
            return render(request, 'dashboard/mensagens.html', context)
    context = {
        'mensagens':mensagens,
        'error_message': error_message,

        
        
    }
    return render(request, 'dashboard/mensagens.html', context)

def mensagemView (request, id):
    
    try :
        mensagem = Mensagem_Manager.objects.get(id=id)  
    except: 
        mensagem = mensagem.objects.get(id=id)    
        
    
     
    context= {
        'mensagem':mensagem,
        
    }
    return render(request, 'dashboard/mensagem.html', context)


def mudarInfoView(request):

    try :
        user = request.user.id
        userInfo = Customuser.objects.get(user=user)

        
        context = {
            'userInfo':userInfo,
            'user':user,
            }
        
        return render(request, 'dashboard/mudar-informacao.html',context)
    except :
        return redirect('login')
    
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
        
        if imagem_servico is None:
            
            try:
                anuncio = Anuncio.objects.get(id=idObj)
                anuncio.nome = nome_servico
                anuncio.bv_desc = resume_servico
                anuncio.descricao = descricao
                anuncio.funcao = funcao
                anuncio.tags = tags_servico
                anuncio.categoria  = categoria_servico
                anuncio.valor = valor_final
                anuncio.tipo = tipo_servico
                anuncio.save()
                return redirect ('gerAnuncio')
                
            except IntegrityError as e :
                produto = Anuncio.objects.get(id=idObj)
                categorias = Categoria.objects.all()
                context = {
                    'produto':produto,
                    'categorias':categorias,
                    'error_message' : str(e),
                    
                }
                return render(request,"dashboard/editar_anuncio.html", context)
        else:
            try:
                anuncio = Anuncio.objects.get(id=idObj)
                anuncio.nome = nome_servico
                anuncio.bv_desc = resume_servico
                anuncio.descricao = descricao
                anuncio.funcao = funcao
                anuncio.tags = tags_servico
                anuncio.categoria  = categoria_servico
                anuncio.valor = valor_final
                anuncio.tipo = tipo_servico
                anuncio.save()
                return redirect ('gerAnuncio')
                
            except IntegrityError as e :
                produto = Anuncio.objects.get(id=idObj)
                categorias = Categoria.objects.all()
                context = {
                    'produto':produto,
                    'categorias':categorias,
                    'error_message' : str(e),
                    
                }
                return render(request,"dashboard/editar_anuncio.html", context)
                
    try:
        produto = Anuncio.objects.get(id=idObj)
        categorias = Categoria.objects.all()
        context = {
            'produto':produto,
            'categorias':categorias,
            
        }
        return render(request,"dashboard/editar_anuncio.html", context)
    except IntegrityError as e:
        print(str(e))
        return redirect('gerAnuncio')
        

def pubAnuncioView(request):
    print(request.user)
    confiabilidade = Confiabilidade.objects.get(user=request.user)
    print(confiabilidade)
    userInfo = Customuser.objects.get(user=request.user)
    creditos = Credito.objects.get(user=request.user)
    if confiabilidade.nivel_confiavel == 0 :
        print ('entrei')
        error_messages = "Aumente seu nivel de confiabilidade, confirmando o email ou enviando foto do documento."
       
        context = {
            'error_messages':error_messages,
            'userInfo':userInfo,
            'creditos':creditos,
        }
        return  render(request, 'dashboard/minha-conta.html', context)
    
        
    categorias = Categoria.objects.all()
    
    if request.method == 'POST':
        tipo_servico = request.POST.get('tipo')
        nome_servico = request.POST.get('nome_servico')
        resume_servico = request.POST.get('resume_servico')
        data_prazo = request.POST.get('data_prazo')
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
                    data_prazo = data_prazo,
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
                    data_prazo = data_prazo,
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
    
    anuncios = Anuncio.objects.filter(usuario=request.user)
    context = {
  
        'anuncios' : anuncios,
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
            carroProduto = Produto_Carrinho.objects.create(carrinho = carro_obj,produto = produto, avaliacao   = produto.avaliacao_anuncio,  quantidade  = 1, subtotal=produto.valor)
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
    valorTotal = carrinho.total
    contagem = Produto_Carrinho.objects.filter(carrinho= carro_id).count()
    
    if request.user.is_authenticated:
        creditos = Credito.objects.get(user=request.user)
    else:
        creditos = 0 
           
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
    produto =  Produto_Carrinho.objects.get(carrinho=carro_id, id=idObj)
    carrinho  = Carrinho.objects.get(id=carro_id)
    if desc == "inc" : #increment
        produto.quantidade += 1
        carrinho.total += produto.produto.valor
        carrinho.save()
        produto.save()
        return redirect ("carrinho")
    elif desc == "dec" : # decrement
        produto.quantidade -=1
        carrinho.total -= produto.produto.valor
        carrinho.save()
        produto.save()
        
        if produto.quantidade < 1:
            print("entrou")
            produto.delete()
            return redirect('carrinho')
        produto.save()
        return redirect('carrinho') 
    
    return redirect('carrinho')
    
        
def deleteView (request,idObj):

    try:
      carro_id = request.session.get("carro_id", None)
    except:         
        if carro_id.exists():
            carrinho = Produto_Carrinho.objects.get(carrinho= carro_id, id = idObj)
            carrinho.delete()
        else:
            carro_id = None
        

    
    return redirect('carrinho')

def deleteMsgView (request,idObj):

    mensagem = Mensagen.objects.get(id=idObj)
    mensagem.delete()

    
    return redirect('mensagens')


def deleteAnuncioView (request,idObj):

    anuncio = Anuncio.objects.get(id=idObj)
    anuncio.delete()

    
    return redirect('gerAnuncio')



def checkoutView (request):
    
    
   
        user = request.user
        try:
           
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
            
        except : 
            context= {'error_message':"Algo deu errado"}
            return render(request, 'index/login.html', context)
            
        

def pagamentoView (request):
    
    
    if request.method == 'POST':
        nome_post = request.POST.get('nome')
        sobrenome_post =request.POST.get('sobrenome')
        telefone_post =request.POST.get('telefone')
        email_post  =request.POST.get('email')
    
            
        try :
            checkout = Checkout.objects.all()
            checkout.create(
                    user = request.user,
                    nome = nome_post,
                    ultimo_nome = sobrenome_post,
                    telefone = telefone_post,
                    email = email_post
                            )       
        except IntegrityError as e: 
            print(str(e))
            
            redirect( 'checkout')
            
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

def minhaVendasView (request):

    
    anuncios = Anuncio.objects.filter(usuario=request.user)  # Filtrar anúncios do usuário
    creditos= Credito.objects.get(user=request.user)
    lista_pedidos = []  
    ultimas_vendas = []
    month = datetime.datetime.now()
    for i in anuncios:
        vendas = Pedido.objects.filter(carrinho_str__icontains=i.nome, date__month=month.month, status_pedido= "Concluida" )
        ultimas_vendas.append(vendas)
    total_vendas = len(ultimas_vendas)
    for i in anuncios:
            try:
                pedido_anuncio = Pedido.objects.filter(carrinho_str__icontains=i.nome, status_pagamento="Concluida")
                lista_pedidos.extend(pedido_anuncio)  
            except Pedido.DoesNotExist:
                pass
    print( lista_pedidos)
    context = {
        'creditos':creditos,
        'total_vendas':total_vendas,
        'vendas' : lista_pedidos,
        'anuncios' :anuncios,
    }
    return render(request, 'dashboard/vendas.html', context)

def comprovanteView(request, id_pedido):

    pedido =  Pedido.objects.get(id=id_pedido)
    
    if request.method == 'POST':
        
        comprovante = request.POST.get('comprovante')
        pedido.comprovante = comprovante
        
        pedido.save()
        return redirect('minhasVendas')
    else:
        context = {
            'pedido': pedido,
        }
        return render(request, 'dashboard/comprovante.html', context)
    
    
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
                'error_message' : error,
                'creditos': creditos_usuario,
                
            }
            return render(request, 'index/creditos.html', context)

            
        
        try :
            
            creditos_usuario.valor_antigo = creditos_usuario.valor
            creditos_usuario.valor = creditos_usuario.valor - carrinho_total.total
            produtos_pedido = []
            for i in produtos_carrinho:
               produtos_pedido.append(i.produto.nome)
               
            creditos_usuario.save()

            pedido.create(
                user_remetente = user,
                valor_carrinho = carrinho_total.total,
                carrinho = carrinho_total,
                carrinho_str = produtos_pedido,
                status_pagamento = "Concluida",
                status_pedido = "Pendente",
                metodo_pagamento="Creditos"
                
            
            ) 
            print('pedido criado')
            pedido = Pedido.objects.filter(user_remetente=user)   
            
            ultimo_pedido= pedido.last()
            
        except IntegrityError as e:
            print(str(e))
            error = str(e)
            context = {
                'error' : error,
                'creditos': creditos_usuario,
                
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
   
            'creditos': creditos_usuario,
            
                }
        return render(request, 'index/pedidos.html', context )
    

def creditosView (request):
    
    context={}
    return render(request, 'index/creditos.html', context)
def confirmarEntregaView (request, id):
    
    pedido = Pedido.objects.get(id=id)
    pedido.status_pedido  = "Concluida"
    pedido.confirm_client  = "True"
    pedido.save()
    validador_pedido(pedido.id)
    
    return redirect('dashboard')



def rec_senhaView (request):
    user_request = request.user
    
    if request.method == 'POST':
        email = request.POST['email']
        if email is not None:
            try:
                user = User.objects.get(email=email)
                if user == user_request:
                    pass
                
            except User.DoesNotExist :
                
                user = None
        
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                nome_usuario  = user.username
                email_subject = 'Recuperação de Senha'
                email_from = "gleydevelopment@gmail.com"
                
                email_body = f"Olá {nome_usuario} Tudo bem ? Foi feita uma solicitação de recuperação de senha para sua conta na Gameniack. Para prosseguir o procedimento, acesse o link abaixo, http://gleydevelopment.com.br/reset_senha/{uid}/{token}." + "Se por acaso não foi voce que solicitou, faça imediatamente a troca de senha"
                send_mail(email_subject, email_body,email_from, [email], fail_silently=False)
                return redirect('msg_senha')
            else:
                    error_message = 'E-mail não encontrado'
                    return render(request, 'index/recuperar-senha.html', {'error_message': error_message})
        else:
                error_message = '   Digite um e-mail'
                return render(request, 'index/recuperar-senha.html', {'error_message': error_message})
    else:
        return render(request, 'index/recuperar-senha.html')


def msg_senhaView (request):
    
    logout(request)
    
    
    return  render (request, 'index/msg_senha.html' )
    
     
     
def reset_senha(request, uidb64, token):
    
    try:
        uid = force_str( urlsafe_base64_decode (uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None


    if user is not None and default_token_generator.check_token(user, token):
      
        
        if request.method == 'POST':
            password = request.POST['password']
            user.set_password(password)
            user.save()
            return redirect('login') 
        else:
            print('recsenha')
            return render(request, 'index/recuperar_senha.html', {'uidb64': uidb64, 'token': token})
    else:
        return render(request, 'index/reset_senha_invalido.html')

   
    
def teste (request):
    return render(request, 'index/recuperar-senha-resetar.html')

