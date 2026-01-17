from dataclasses import dataclass

@dataclass
class Prodotto:
    id:int
    product_name:str
    brand_id:int
    category_id:int
    model_year:int
    list_price:float


    def __hash__(self):
        return hash(self.id)