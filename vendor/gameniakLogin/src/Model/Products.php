<?php

    namespace Main\Model;

    use \Main\Model;
    use \Main\DB\Sql;
use Main\Rule;

class Products extends Model
    {




        public function update(){


            $sql = new Sql();
          

        
            
            $query = "CALL sp_products_update(

             :idproduct,
             :iduser,
             :incategory,
             :desproduct,
             :desresume,
             :desdescription,
             :desreason,
             :destags,
             :vlprice,
             :vtaxa,
             :desimages,
             :dtregister
          
    
            );";

           $results = $sql->select($query, [

                ':idproduct'=>$this->getidproduct(),
                ':iduser'=>$this->getiduser(),
                ':incategory'=>$this->getincategory(),
                ':desproduct'=>$this->getdesproduct(),
                ':desresume'=>$this->getdesresume(),
                ':desdescription'=>$this->getdesdescription(),
                ':desreason'=>$this->getdesreason(),
                ':destags'=>$this->getdestags(),
                ':vlprice'=>$this->getvlprice(),
                ':vtaxa'=>$this->getvtaxa(),
                ':desimages'=>$this->getdesimages(),
                ':dtregister'=>$this->getdtregister()
                     
     

            ]);  


          

            if( count($results) > 0 ){

                $this -> setData( $results[0] );

            }//endif
            
        }//endmethod











        public function get($idproduct){




                $sql = new Sql();

                $query = "  
                
                SELECT * FROM tb_products 
                WHERE idproduct = :idproduct
                ORDER BY dtregister DESC
                LIMIT 1;

                 
                ";

             return $results = $sql -> select($query, [

                    ':idproduct' => $idproduct

                ]);
          

                if (count($results) > 0 ) {
                    
                    $this->setData( $results[0] );
                    
                }

        }//END FUNCTION





        public function getAllProducts(){
           
            $sql = new Sql();

            $query = "  
            
            SELECT * FROM tb_products 
            ORDER BY dtregister DESC
                   
            ";

           return $sql->select($query);

        }













 //===================================
 //===================================
 //===================================
 //===================================
        public function getProductsBySortText($SortText){
           
            $sql = new Sql();
        
            $QueryWithFilterByCategory = "         
            SELECT * FROM tb_products        
            WHERE desproduct LIKE CONCAT('%', :search, '%') 
            AND incategory = :incategory    
            ORDER BY
            (CASE WHEN desproduct LIKE CONCAT('%', :search, '%') then 1  END )  DESC          
            ";
        
        
            $QueryWithoutFilterByCategory = "         
            SELECT * FROM tb_products        
            WHERE desproduct LIKE CONCAT('%', :search, '%') 
            ORDER BY
            (CASE  WHEN desproduct LIKE CONCAT('%', :search, '%') then 1  END )  DESC          
            ";

            $QueryJustByCategory = "         
            SELECT * FROM tb_products        
            WHERE incategory = :incategory    
            ORDER BY dtregister DESC
            ";



            if($SortText['categoria'] != 0 )
            {

                if(trim($SortText['procurar']) == "" || $SortText['procurar'] == NULL)
                {
                     
                    $results = $sql->select($QueryJustByCategory,[               
                        ':incategory' => $SortText['categoria']
                    ]);

                }
                else
                { $results = $sql->select($QueryWithFilterByCategory,[ ':search' => $SortText['procurar'],':incategory' => $SortText['categoria']  ]);  }

                
                //===================================
                if($results != NULL ||  trim($results) != '')
                { return $results; }                 
              
                else
                {
                    User::setError(Rule::SearchError);
                    header("Location: /");
                    exit;
                }               
              //===================================
              
            }
            else
            {                              
                $results = $sql->select($QueryWithoutFilterByCategory,[ ':search' => $SortText['procurar'] ]);         
              
                //===================================
                if($results != NULL || trim($results) != '') { return $results; }    
                else
                {
                    User::setError(Rule::SearchError);
                    header("Location: /");
                    exit;
                }  
                 //===================================   

            } 
                   
        }

 //===================================
 //===================================
 //===================================
 //===================================

























//============================================================================>
        public function setError($error, $code){
            header('HTTP/1.1 500 Campo Preenchido Incorretamente');
            header('Content-Type: application/json; charset=UTF-8');
            die(json_encode(array('message' => $error, 'code' => $code)));
            
        }

        //VERIFICA SE TEM O VALOR FOI SETADO E SE É IGUAL A NULO
        public function CheckCharacterError($value, $error)
        { if( !isset($value) || $value == '' ){  $this->setError($error,rand(1,10000));  }   }
           
        //VERIFICA SE A STRING É VÁLIDA
        public function CheckValidateError($VALIDATE_METHOD, $error) { 
        if( ( $value = $VALIDATE_METHOD ) === false){  $this->setError($error,rand(1,1000));   } 
            else{ return $value; }  }
//============================================================================>       
            public function setErrorADMIN($error, $ID){
                User::setError($error);
                if(User::checkLogin()){
                    header('Location: /dashboard/editar-servico/'.setHash($ID));   
                }else{
                    header('Location: /admin/anuncios/editar/'.setHash($ID)); 
                }
                 
                exit;                
           }
            //VERIFICA SE TEM O VALOR FOI SETADO E SE É IGUAL A NULO
            public function CheckCharacterErrorADMIN($value, $error, $ID)
            { if( !isset($value) || $value == '' ){  $this->setErrorADMIN($error,$ID);  }   }
               
            //VERIFICA SE A STRING É VÁLIDA
            public function CheckValidateErrorADMIN($VALIDATE_METHOD, $error,$ID) { 
            if( ( $value = $VALIDATE_METHOD ) === false){  $this->setErrorADMIN($error,$ID);   } 
                else{ return $value; }  }
//============================================================================>                  
            
  
           public function SetIMGLink($value, $position)
            {

               
                if( isset($value[$position]) || $value[$position] = "" ){                                                        
                       return '/' . $value[$position];                                                   
                }
                else
                {
                   return '/res/UsersUploads/products_support/notfound.png';       
                }
            }

    

            





            public function DeleteProduct($SearchResults, $isrouteAdmin){



                $UserFolderName = explode('/',$SearchResults[0][0])[3];
                $FolderName = explode('/',$SearchResults[0][0])[4];
                
                try {
                //====================================>
                //BASICAMENTE, VAI PERCORRER TODOS OS ARQUVIOS DO DIRETÓRIO, ELIMINAR UM POR UM, E DEPOIS APAGAR A PASTA.
                //====================================>
                $dir = 'res' . DIRECTORY_SEPARATOR . 'UsersUploads' . DIRECTORY_SEPARATOR .  'products_images' .  DIRECTORY_SEPARATOR . $UserFolderName . DIRECTORY_SEPARATOR . $FolderName;
                $it = new \RecursiveDirectoryIterator($dir, \RecursiveDirectoryIterator::SKIP_DOTS);
                $files = new \RecursiveIteratorIterator($it,
                \RecursiveIteratorIterator::CHILD_FIRST);
                foreach($files as $file) {
                    if ($file->isDir()){
                        rmdir($file->getRealPath());
                    } else {
                        unlink($file->getRealPath());
                    }
                }
               
               
                        try 
                            {
                                rmdir($dir);
                            } 
                        catch (\Throwable $th) 
                            {
                                User::setError(Rule::ERROR_PRODUCT_DELETED);
                                if($isrouteAdmin){
                                    header("Location: /admin/visualizar-anuncios");
                                }
                                else{
                                    header("Location: /dashboard/gerenciar-anuncios");
                                }
                           
                                exit;
                            }
     
                } catch (\Throwable $th) {
                    User::setError(Rule::ERROR_PRODUCT_DELETED);
                    if($isrouteAdmin){
                        header("Location: /admin/visualizar-anuncios");
                    }
                    else{
                        header("Location: /dashboard/gerenciar-anuncios");
                    }
                    exit;
                }
            
              
               
                
                User::setSucess(Rule::PRODUCT_SUCCEFUL_DELETED);
                if($isrouteAdmin){
                    header("Location: /admin/visualizar-anuncios");
                }
                else{
                    header("Location: /dashboard/gerenciar-anuncios");
                }
                exit;
            }









            
    }//END CLASS



?>