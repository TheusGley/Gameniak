<?php

namespace Main\Model;

use Main\Rule;
use \Main\Model;
use Main\DB\Sql;


class Item extends Model
    {

      

        public function Clear_Cart()
        {
            $_SESSION[User::CART_VALUES] = NULL;
        }

   
        public function Create_Item($idItem)
        {
     
            if(!isset($_SESSION[User::CART_VALUES]))
            {
                $_SESSION[User::CART_VALUES] = array();              
            }
                 
            if( in_array($idItem, $_SESSION[User::CART_VALUES]) )
            {             
                User::setError(Rule::CART_ITEM_EXISTS);
                header("Location: /");
                exit;
            }
            array_push($_SESSION[User::CART_VALUES], $idItem );
            User::setSucess(Rule::ADICIONADO_COM_SUCESSO);
        }
        

        
     



    }
        


?>