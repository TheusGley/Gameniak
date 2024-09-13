<?php

    namespace Main;

use Main\DB\Sql;
use \Rain\Tpl;
    use \Main\Model\User;


    class Page{


 
       
        private $tpl;
        public $Getconfig;

        public $Site_Theme = "header";

        private $options = [];
        private $defaults = [


                'header' => true,
                'footer' => true,
                'data'=>[]


        ];

     
   
        public function setData($data = array()){
            foreach($data as $key => $value){
                $this ->tpl->assign($key, $value);
                
            }

        }



        public function getTheme()
        {
            return $this->Site_Theme;
        }
        
        

//--------------
//HEADER
//--------------

  

        public function __construct($opts = array(), $tpl_Dir = 'views'.DIRECTORY_SEPARATOR."index" )
        {
            $this ->options = array_merge($this->defaults, $opts);


            $_SESSION[User::SITE_CONFIGURATION]['theme'] = $_COOKIE['theme'];
            if(isset($_SESSION[User::SITE_CONFIGURATION]['theme'])){  $this->Site_Theme = $_SESSION[User::SITE_CONFIGURATION]['theme'];}

            $config = array(
                "tpl_dir" => $_SERVER['DOCUMENT_ROOT'].DIRECTORY_SEPARATOR.$tpl_Dir.DIRECTORY_SEPARATOR,
                "cache_dir" => $_SERVER['DOCUMENT_ROOT'].DIRECTORY_SEPARATOR."views-cache".DIRECTORY_SEPARATOR);
            
                
             
                Tpl::configure( $config );
              
            
                $this -> tpl = new Tpl;
               
     

                $this ->setData($this ->options['data']);
               
               if($this -> options['header'] === true){

                $sql = new Sql();

                $query = "
                   SELECT * FROM tb_categories
                   ORDER BY dtregister DESC              
                ";

              

                $categories = $sql->select($query);
      


                $FinalPrice = 00.00;   
                $Itens = array();
                $CartCount = 0;

             
               
               
              

                if(isset($_SESSION[User::CART_VALUES]))
                {
                    

                    $queryGetCart = "SELECT * FROM tb_products WHERE idproduct = :idproduct";    
                 
                    $max = 0;
                    if(count($_SESSION[User::CART_VALUES]) > 0){
                        $max = max(array_keys($_SESSION[User::CART_VALUES])) ;
                    }
                                
                    for($i = 0; $i <= $max; $i++ )   
                    {
                       
                        if( isset( $_SESSION[User::CART_VALUES][$i] ) )
                        {                                                
                            $Itens[$i] = $sql->select($queryGetCart, ['idproduct' => $_SESSION[User::CART_VALUES][$i] ]);                            
                            $FinalPrice += $Itens[$i][0]['vlprice'];
                        }

                    }
                    $CartCount = count($_SESSION[User::CART_VALUES]);
                }
                
                // echo "<pre>";
                // var_dump($Itens);
                // exit;


             
                          
                    $this -> setData(
                        


                        array(
                        'categories' =>  $categories,   
                        'isLogged' => User::checkLogin(),
                        'Item' => $Itens,
                        'CartCount' => $CartCount,
                        'CartPrice' => $FinalPrice
                        )
                                     
                    );

                    
        
                    $this -> tpl -> draw($this->Site_Theme);                       
                
               } 
        }  
//--------------
//HEADER
//--------------


      
        

        public function setTpl($name, $data = array(), $returnHTML = false)
        {
          
            $this ->setData($data);


            return $this ->tpl->draw($name, $returnHTML);

        }


//--------------
//Footer
//--------------

        public function __destruct()
        {
               
            if($this -> options['footer'] === true){
                $this -> tpl ->draw("footer");
               } 
           
        }
//--------------
//Footer
//--------------
  
  }
  
    

?>