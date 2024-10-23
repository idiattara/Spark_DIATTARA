def  rechercheIT(list :List[Any], elt:Any):Boolean={

  for (e  <- list){
    if (e==elt) return true
  }
  return  false 
}

def  rechercheREC(list :List[Any], elt:Any):Boolean={
  list match{
    case Nil => false
    case head::Nil => if(head==elt) return true else  return   false 
    case head::queu => if(head==elt) return true else  return   rechercheREC(queu, elt)
  }
}

def  rechercheLamb(list :List[Any], elt:Any)=list.filter(e=>e==elt).length >= 1
