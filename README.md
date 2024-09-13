# GAMENIAK MARKETPLACE - CP2 S.A

Pequeno guia sobre a instalação do site em um servidor.

## 🔐 CONTA DE ADMINISTRADOR PADRÃO
- Login : admin@gameniakmarketplace.com
- Senha : @admin123321

## ☕ Versão do PHP

- PHP >= 7.3 OU 7.4.12

## 🔔 AVISO

```php
ob_start()
```
- Adicione a linha "ob_start()" Ao colocar o site em um servidor, SE FOR EM LOCALHOST NÃO PRECISA! [ARQUIVO DA LINHA](index.php) 


## ✅ CRIANDO O BANCO DE DADOS 


- 1 ) Para encontrar o arquivo do banco de dados, vá até -> [ESTE DIRETÓRIO](/Banco_De_Dados).

- 2 ) Agora basta pegar o arquivo em .SQL e importar para o seu [BANCO DE DADOS](/vendor/gameniakLogin/src/DB/Sql.php).


## ✅ CONECTANDO O BANCO DE DADOS 

- PARA DEFINIR O LOGIN DO BANCO DE DADOS, VÁ ATÉ -> [ESTE DIRETÓRIO](/vendor/gameniakLogin/src/DB/Sql.php).



## 🔔🔔 AVISO IMPORTANTÍSSIMO 

Este arquivo .SQL contém 4 (QUATRO) STORAGE PROCEDURES, são elas :

- [sp_addresses_update](vendor/gameniakLogin/src/Model/Address.php)

- [sp_products_update](/vendor/gameniakLogin/src/Model/Products.php)

- [sp_purchases_update](/vendor/gameniakLogin/src/Model/Compras.php)

- [sp_users_update](/vendor/gameniakLogin/src/Model/User.php)

Se assegure de que as quatro Storage Procedures estão presentes no seu banco de dados!


## 📌 Diretórios Importantes

- [DIRETÓRIO DOS ARQUIVOS HTML](/views)
- [DIRETÓRIO DOS ARQUIVOS JS/CSS/IMAGENS](/res)
- [DIRETÓRIO DOS ARQUIVOS PHP](/Pages)
- [DIRETÓRIO DAS CLASSES (PHP)](/vendor/gameniakLogin/src/)
- [DIRETÓRIO DO BANCO DE DADOS](/vendor/gameniakLogin/src/DB/Sql.php)

- [ARQUIVO PARA IMPORTAR O BANCO DE DADOS](/Banco_De_Dados/db_gameniak.sql)




## 🛍️ Bibliotecas/Frameworks Utilizados

Frameworks escolhidos : 
```php
echo ("Slim Framework" . " & " . "Rain TPL");
```
Bibliotecas Utilizadas :
```javascript
alert (" Bootstrap ( CSS & JS ) " + " PORTO TMT " + " PLUGINS SECUNDÁRIOS EX : DATATABLES (TABELAS) ");
```
Banco de dados / Estruturas de dados :
```php
var_dump( array( 'MySql', 'JSON', 'AJAX' ) );
```


<!-- ## 🛍️ Guias do sistema 

Explicação do Código [Pastas e Classes](https://www.youtube.com/watch?v=mPx8hCWsXgw).
Explicação do Site  [VERSÃO BETA 0.1](https://www.youtube.com/watch?v=9Zg65gtQsV8). -->


## 📲 Modificação no .HTACCES para forçar HTTPS (CASO USE CPANEL)
RewriteCond %{HTTPS} off 
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

## 🚪 Aviso Final

