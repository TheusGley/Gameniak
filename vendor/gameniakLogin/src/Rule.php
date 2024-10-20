<?php

namespace Main;

        class Rule{

                const DEVELOPMENT = "gameniakmarketplace.com.br"; 
                
                //LOGIN
                const ERROR_EMAIL = "Informe o seu Email";
                const VALIDATE_EMAIL = "O Email parece estar em um formator inválido | Por favor, tente novamente.";

                const ERROR_PASSWORD = "Por favor, não deixe campos em branco!";

                const PASSWORD_LENGHT_MIN = 6;
                const PASSWORD_LENGHT_MAX = 20;

                const VALIDATE_PASSWORD = "A senha deve ter de ".Rule::PASSWORD_LENGHT_MIN. " até " .Rule::PASSWORD_LENGHT_MAX." caracteres | Por favor, tente novamente.";            
                
                const ERROR_LOGIN = "Usuário inexistente ou senha inválida";
                //FIM LOGIN

                //CARRINHOS
                const CART_ITEM_EXISTS = "Este item já existe no seu carrinho | Por favor, tente novamente. ";
                const ADICIONADO_COM_SUCESSO = "O Item foi adicionado ao seu carrinho | Obrigado por utilizar os nosso serviços.";
                const ERROR_CART_EMPTY = "O seu carrinho está vazio | Por favor, adicione algum item e tente novamente. ";

                const ERROR_NOTFOUNDED = "Usuário não encontrado";
                const ERROR_BOOL = "Utilize um valor válido";
                const VALIDATE_BOOL = "O valor precisa estar entre 0 e 1";


                const UPDATE_ITEM = "Atualizado com sucesso!";

                //Atualizar Senha de usuário Comum
                const INCORRECT_CONFIRM = "As senhas não coincidem" ;   
                const SUCESS_PASSWORD = "Senha alterada com sucesso | Obrigado por utilizar os nossos serviços!";
                //Atualizar Senha de usuário Comum


                //Exibição de Usuários no painel administrador
                const PAGINATION_MAXNUMBER = 999;
                const PAGINATION_MINNUMBER = 1;
                const PAGINATION_ITENSPERPAGE = 10;
                //Exibição de Usuários no painel administrador


                //Atualizar Senha de usuário administrador
                const ERROR_CURRENT_PASS = "Por favor, insira a senha antiga.";
                const VERIFY_CURRENT_PASS = "A nova senha não pode ser igual a anterior, tente novamente";
                const VERIFY_PASSWORD = "A senha atual informada é inválida. Por favor, tente novamente.";
                //Atualizar Senha de usuário administrador
            
                //Recovery de senha de administrador
                const ERROR_SET_RECOVERY = "Ocorreu um erro desconhecido ao realizar esta ação | Por favor, tente novemente.";
                const WEBSITE_ROOT_ADRESS = "http://gameniakmarketplace.com.br";  //Trocar o HTTP por HTTPS
          
          
                const URI_ADMIN = "admin";
                const URI_RECOVERY = "recuperar-senha";
                const URI_RECOVERYSENT = "redefinir";
                const URI_USER_LOGIN = "login";
                const URI_SUPPORT = "central-ajuda";

                const ERROR_GET_RECOVERY = "Houve um erro inesperado | Por favor, volte no Email e clique novamente no Link que você recebeu 
                | Caso o erro persista, aguarde aproximadamente 60 minutos e peça uma nova recuperação de senha ou entre em contato com o suporte ";
                //Recovery de senha de administrador


                
                //REGISTRAR
                const ERROR_NAME = "Informe o seu Nome";      
                const VALIDATE_NAME =  "O seu nome não pode conter caracteres especiais ou números | Por favor, tente novamente";
                const VALIDATE_FULL_NAME = "Este nome não parece estar completo";
 
                const ERROR_EMAIL_CONFIRM = "Informe a confirmação do e-mail";

                const VALIDATE_EMAIL_CONFIRM = "Os emails informados precisam ser iguais | Por favor, tente novamente";
                const ERROR_INTERMS = "Por favor, marque o checkbox se estiver de acordo com os termos de uso";

                const CHECK_USER_EXISTS = "Já existe uma conta cadastrada com este email | Por favor, utilize outro ";

                const ERROR_REGISTER = "Ocorreu um erro momentâneo devido a uma instabilidade na conexão de internet entre o nosso servidor
                e o seu dispositivo | Por favor, tente se cadastrar novamente | caso ainda sim o erro persista, entre em contato com o suporte";

                const ERROR_ENTITIES = "Ocorreu um erro momentâneo devido a uma instabilidade na conexão de internet entre o nosso servidor
                e o seu dispositivo | Porém sua conta foi criada | Por favor, faça o login utilizando o email e senha escolhidos | 
                caso ocorra algum erro entre em contato com o suporte";
               
                const EMAIL_RECOVERY_SUBJECT = "Recuperação de senha";
                const EMAIL_REGISTER_SUCCESS = "Cadastro - GameniakMarketplace";

          
                const SUCCES_UPDATE_INFO = "Seu Perfil atualizado com sucesso | Obrigado por utilizar os nossos serviços!";
                const ERROR_UPDATE_INFO = "Ocorreu um erro ao atualizar oseu perfil | Por favor, tente novamente.";

            

                const INCORRECT_FIELDS = "Os campos não parecem estar completos | Por favor, verifique e tente novamente. ";


                //ÁREA DE CHECKOUT PARA O MERCADO PAGO
                const ERROR_FIRST_NAME = "";
                const ERROR_SECOUND_NAME = "";
                const ERROR_PHONE_NUMBER = "";
                const ERROR_STATE_SELECTED = "";


                const PASSWORD_SENDED_SUCCESS = "Enviamos para o seu e-mail um link para recuperar a senha da sua conta | Obrigado por utilizar os nosso serviços.";

                //ÁREA DE CONFIGURAÇÕES ADM
                const CATEGORY_CREATED_SUCCES = "Categoria criada com sucesso | Obrigado por utilizar os nosso serviços";


                //ÁREA DE CATEGORIAS ADM
                const CATEGORY_DELETED_SUCEFULL = "Categoria deletada com sucesso | Obrigado por utilizar os nosso serviços";
                const CATEGORY_DELETED_ERROR = "Ocorreu um erro desconhecido ao deletar essa categoria | Por favor, tente novamente";

                
                //PROCURAR SERVIÇOS NO INDEX
                const SearchError = "Infelizmente não encontramos nenhum serviço | Por favor, tente novamente";

                //ÁREA DE MODIFICAR SERVICOS
                const ERROR_UNAUTHORIZED_SERVICE = "Você não possui permissão para fazer isso!";

                const PURCHASE_DELETED_ERROR = "Ocorreu um erro ao deletar este recibo | Por favor, tente novamente";
                const PURCHASE_DELETED_SUCCESS = "Recibo deletado com sucesso | Obrigado por utilizar nossos serviços ";


        
                const ERROR_PRODUCT_DELETED = "Ocorreu um erro ao deletar este produto | Por favor, tente novamente.";
                const PRODUCT_SUCCEFUL_UPDATED = "Produto atualizado com sucesso | Obrigado por utilizar nossos serviços ";
                const PRODUCT_SUCCEFUL_DELETED = "Produto deletado com sucesso | Obrigado por utilizar nossos serviços ";

                //CONSTANTES DE SERVIÇO (ADICIONAR PLANO)
                const ERROR_SERVICE_NAME = "Nome inválido ou não informado | Por favor, verifique os campos e tente novamente.";
                const ERROR_SERVICE_RESUME = "Descrição Breve inválida ou não informada | Por favor, verifique os campos e tente novamente." ;
                const ERROR_SERVICE_DESCRIPTION = "Descrição inválida ou não informada | Por favor, verifique os campos e tente novamente.";
                const ERROR_SERVICE_OBJECTIVE = "Função do serviço inválida ou não informada | Por favor, verifique os campos e tente novamente."; 
                const ERROR_SERVICE_CATEGORY = "Categoria do serviço inválida ou não informada | Por favor, verifique os campos e tente novamente.";
                const ERROR_SERVICE_TAGS = "Tags do serviço inválidas ou não informadas | Por favor, verifique os campos e tente novamente.";
                const ERROR_SERVICE_PRICE = "Valor do serviço inválido ou não informado | Por favor, verifique os campos e tente novamente.";
                const ERROR_SERVICE_IMAGES = "Não foram encontradas imagens para o seu serviço | Por favor, envie alguma imagem e tente novamente.";
                const ERROR_SERVICE_IMAGES_UPLOAD = "Ocorreu um erro ao enviar as suas imagens | Por favor, atualize a página e tente novamente.";

                const SUCCESS_CREATED = "Seu anúncio foi publicado com sucesso | Obrigado por utilizar os nossos serviços, é sempre um prazer poder te ajudar!";



                const ERROR_SERVICE_VALIDATE_NAME = "Não utilize números ou caracteres especiais no nome do seu serviço | Por favor, tente novamente.";
                const ERROR_SERVICE_VALIDATE_RESUME = "Não utilize números ou caracteres especiais na pequena descrição do seu serviço | Por favor, tente novamente.";
                const ERROR_SERVICE_VALIDATE_DESCRIPTION = "Não utilize números ou caracteres especiais na descrição do seu serviço | Por favor, tente novamente.";
                const ERROR_SERVICE_VALIDATE_OBJECTIVE = "Não utilize números ou caracteres especiais no objetivo do seu serviço | Por favor, tente novamente.";
                const ERROR_SERVICE_VALIDATE_CATEGORY = "Não utilize números ou caracteres especiais na categoria do seu serviço | Por favor, tente novamente.";
                const ERROR_SERVICE_VALIDATE_TAGS = "Não utilize números em alguma das tags do seu serviço | Por favor, tente novamente.";
                const ERROR_SERVICE_VALIDATE_PRICE = "Não utilize letras no valor do seu serviço | Por favor, tente novamente.";
                
                const ERROR_IMAGE_SIZE = "Uma ou mais imagens são muito grandes, não podemos utilizar | Por favor, redimensione ou nos envie outra.";
                const ERROR_IMAGE_MAX = "Você atingiu o limite máximo de imagens (Máximo de QUATRO) | Por favor, exclua algumas imagens .";


                const MaxNumberOfImages = 4;
                const MaxSizeOfImages = 2; //EM MEGABYTE (MB)
                
                const VALOR_TAXA_SERVICO = '10%';

             
                //ENDEREÇO
                const ADDRESS_UPDATED = "Suas informações de endereço foram atualizadas com sucesso | Obrigado por utilizar os nossos serviços";
                const ADDRESS_ERROR = "Suas informações não foram atualizadas | Por favor, não deixe campos em branco!";



                //TENTATIVAS DE COMPRA
                const NOT_CONNECTED_USER_BUY = "Você precisa estar conectado para fazer isso | Por favor, tente novamente.";
                const SAMEUSER_BUY_TRY = "Você não pode comprar o seu próprio produto.";
                const ADMIN_TRY_BUY = "Você precisa estar logado em uma conta de usuário comum.";
                const SUCCEFULL_PURCHASED_APROVADO = "Compra Autorizada com sucesso.";
                const SUCCEFULL_PURCHASED_PENDENTE = "Compra Pendente.";
                const SUCCEFULL_PURCHASED_CANCELADO = "Compra Cancelada.";


                //VARIAVEIS GLOBAIS PADRÃO DE CADASTRO

                const DEFAULT_INADMIN = 0;
                const DEFAULT_INSELLER = 1;
                const DEFAULT_INBUYER = 1;
                const DEFAULT_INSTATUS = 1;
                const DEFAULT_INAUTOSTATUS = 1;
                const DEFAULT_INTYPEDOC = 0; //0 CPF -> 1 CNPJ
                const DEFAULT_COUNTRY_AREA = 55;
             

        }

?>