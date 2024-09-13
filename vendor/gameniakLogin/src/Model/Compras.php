<?php

namespace Main\Model;
use \Main\Model;
use \Main\DB\Sql;


class Compras extends Model
    {




        public function update(){


            $sql = new Sql();
          

        
            
            $query = "CALL sp_purchases_update(
                  
             :idcompra,    
             :idproduto,
             :idseller,
             :iduser,
             :idpagamento,
             :desproduct,
             :desresume,
             :vlprice,
             :desstatus,
             :despayamentmethod,
             :dessellername,
             :desbuyerip,
             :dtbuy

            );";

           $results = $sql->select($query, [

                ':idcompra'=>$this->getidcompra(),
                ':idproduto'=>$this->getidproduto(),
                ':idseller'=>$this->getidseller(),
                ':iduser'=>$this->getiduser(),
                ':idpagamento'=>$this->getidpagamento(),
                ':desproduct'=>$this->getdesproduct(),
                ':desresume'=>$this->getdesresume(),
                ':vlprice'=>$this->getvlprice(),
                ':desstatus'=>$this->getdesstatus(),
                ':despayamentmethod'=>$this->getdespayamentmethod(),
                ':dessellername'=>$this->getdessellername(),
                ':desbuyerip'=>$this->getdesbuyerip(),          
                ':dtbuy'=>$this->getdtbuy()
               
            ]);  


        
            if( count($results) > 0 ){

                $this -> setData( $results[0] );

            }//endif
            
        }//endmethod











        public function get($buyid){




                $sql = new Sql();

                $query = "  
                
                SELECT * FROM tb_compras 
                WHERE idcompra = :idcompra
                ORDER BY dtbuy DESC
                LIMIT 1;

                 
                ";

             return $results = $sql -> select($query, [

                    ':idcompra' => $buyid

                ]);
          

                if (count($results) > 0 ) {
                    
                    $this->setData( $results[0] );
                    
                }

        }//END FUNCTION









        public function getAllPurchases(){
           
            $sql = new Sql();
        
    
            $query = "  
            
            SELECT * FROM tb_compras        
            ORDER BY dtbuy DESC
                   
            ";

           return $sql->select($query);

        }


    

            


    }//END CLASS



?>