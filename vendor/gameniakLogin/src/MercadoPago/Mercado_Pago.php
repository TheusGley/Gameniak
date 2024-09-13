<?php 



namespace Main\MercadoPago;



use Main\Rule;

use Main\DB\Sql;

use \Main\Model\User;

use Main\Model\Address;
use \Main\Model\Dependentes;





    class Mercado_Pago  extends \PHPUnit\Framework\TestCase
    {


        public function CreateDesConstsConnection()
        {
        //=====================
        $sql = new Sql();
        $query = "SELECT * FROM tb_consts";
        return $sql->select($query);
        //=====================
        }


        public function CreateMercadoPagoOrder()
        {
           
            $connection = $this->CreateDesConstsConnection();
            $AcessToken = getConstValues($connection, 'desmercadopagotoken');     
            \MercadoPago\SDK::setAccessToken($AcessToken);      
         
            $preference = new \MercadoPago\Preference();
            $preference->back_urls = array(
                        "success" => Rule::DEVELOPMENT . "/feedback",
                        "failure" => Rule::DEVELOPMENT . "/feedback",
                        "pending" => Rule::DEVELOPMENT . "/feedback"
            );
            $preference->auto_return = "approved";

            // ===========================
            // Cria um item na preferência
            // ===========================
            $Cart_Values = $_SESSION[User::CART_VALUES];
            $Array_Item = array();
        
            if(count($Cart_Values) == 1)
            {           
                $key = array_keys($Cart_Values)[0];          
                $ItemInfo = getProductInfo($Cart_Values[$key])[0];              
                $item = new \MercadoPago\Item();
                $item->title = $ItemInfo['desproduct'];
                $item->quantity = 1;
                $item->external_reference = 1;
                $item->unit_price = $ItemInfo['vlprice'];
                array_push($Array_Item, $item);
            }

            else if(count($Cart_Values) >= 2)
            {            
                $max = max(array_keys($Cart_Values));           
                for($i = 0; $i <= $max; $i++)
                {
                    if( isset( $Cart_Values[$i] ) )
                    {                                                                   
                        $ItemInfo[$i] = getProductInfo($Cart_Values[$i])[0];                                                   
                        $item[$i] = new \MercadoPago\Item();
                        $item[$i]->title = $ItemInfo[$i]['desproduct'];
                        $item[$i]->quantity = 1;
                        $item[$i]->unit_price = $ItemInfo[$i]['vlprice'];
                        array_push($Array_Item, $item[$i]);                   
                    }                                 
                }                        
            }
            // ===========================
            // Encerra a preferência
            // ===========================
      
            $preference->items = $Array_Item;      
            $preference->save();
        
            header('Location: ' . $preference->sandbox_init_point);
            exit;
            // echo "<pre>";
            // var_dump($preference); 
            // exit;
        } 

        

 }



