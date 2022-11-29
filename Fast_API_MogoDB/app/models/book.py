from odmantic import Model

class BookModel(Model):
    keyword : str
    pulicher : str
    price : str
    image : str
    
    class Config:
        collection = "books"
        

# db(faspi=pj) -> collection books -> document