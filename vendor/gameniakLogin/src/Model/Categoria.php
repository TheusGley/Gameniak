<?php

    namespace Main\Model;

    use \Main\Model;
    use \Main\DB\Sql;
    use Main\Rule;

class Categoria extends Model
    {




        public function update(){


            $sql = new Sql();
          

         
     

            
            $query = "CALL sp_categories_update(

             :idcat,
             :descat,
             :desresume,
             :dtregister

            );";

           $results = $sql->select($query, [

                ':idcat'=>$this->getidcat(),
                ':descat'=>$this->getdescat(),
                ':desresume'=>$this->getdesresume(),
                ':dtregister'=>$this->getdtregister()
             
     

            ]);  


            

            if( count($results) > 0 ){

                $this -> setData( $results[0] );

            }//endif
            
        }//endmethod









        public function get($idcat){




                $sql = new Sql();

                $query = "  
                
                    SELECT * FROM tb_categories 
                    WHERE idcat = :idcat
                    ORDER BY a.dtregister DESC
                    LIMIT 1;
                ";

                $results = $sql -> select($query, [

                    ':idcat' => $idcat

                ]);
          

                if (count($results) > 0 ) {
                    
                    $this->setData( $results[0] );
                    
                }

        }//END FUNCTION


        public function getAll(){


            $sql = new Sql();
            $query = "SELECT * FROM tb_categories ORDER BY idcat DESC";
        
            return $sql->select($query);
        }



        public function DeleteCategorie($idcat) {

            $sql = new Sql();
            $query = "DELETE FROM tb_categories WHERE idcat = :idcat";
        
          try 
          {
             $sql->QuerySQL($query,[
                 'idcat' => $idcat
             ]);


             User::setSucess(Rule::CATEGORY_DELETED_SUCEFULL);
             header("Location: /admin/visualizar-categorias");
             exit;
             
          } 
          catch (\Exception $th) {
           
            User::setSucess(Rule::CATEGORY_DELETED_ERROR);
            header("Location: /admin/visualizar-categorias");
            exit;

          }
           
                    

        }

    }//END CLASS



?>