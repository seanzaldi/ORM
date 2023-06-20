
from pydantic import BaseModel
from datetime import date
from typing import Union


class Shop(BaseModel):
    cuit:int
    name:str
    password:str
    tel:int
    address:str
    email:str
    
    class Config:
        orm_mode=True


class Product(BaseModel):
    shop_id:int
    category_id:int
    date:date
    title:str
    size:Union[int, None] = None
    maker:Union[str, None] = None
    notes:Union[str, None] = None
    price:int
     
    class Config:
        orm_mode=True


class Category(BaseModel):
    title:str
    description:str

    class Config:
        orm_mode=True


class Reference_Products(BaseModel):

    title:str
    size:int
    maker:str
    
    class Config:
        orm_mode=True


class Reference_Prices(BaseModel):
    
    id_product_reference:int
    category_id:int
    date:date
    notes:Union[str, None] = None
    price:int
    
    class Config:
        orm_mode=True

