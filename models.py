from sqlalchemy import Column, Integer, String, DATE, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Shop (Base):
    __tablename__='shops'

    id=Column(Integer,primary_key=True,index=True, autoincrement=True)
    cuit=Column(Integer, unique=True, index=True, nullable=False)
    name=Column(String, nullable=False )
    password=Column(String, nullable=False)
    tel=Column(Integer, nullable=False)
    address=Column(String, nullable=False)
    email=Column(String)
      
    items=relationship("Product",back_populates="seller")
    

class Product (Base):
    __tablename__='products'

    id=Column(Integer,primary_key=True,index=True, autoincrement=True)
    shop_id=Column(Integer, ForeignKey("shops.id"),nullable=False)
    category_id=Column(Integer,ForeignKey("categories.id"),nullable=False)
    date=Column(DATE, nullable=False)
    title=Column(String, nullable=False)
    size=Column(Integer)
    maker=Column(String)
    notes=Column(String)
    price=Column(Integer,nullable=False)

    seller=relationship("Shop",back_populates="items")
    group=relationship("Category",back_populates="items")


class Category (Base):
    __tablename__='categories'

    id=Column(Integer,primary_key=True,index=True, autoincrement=True)
    title=Column(String, nullable=False)
    description=Column(String, nullable=False)

    items=relationship("Product",back_populates="group")
    source=relationship("Reference_Prices",back_populates="group")


class Reference_Products (Base):
    __tablename__='reference_products'

    id=Column(Integer,primary_key=True,index=True, autoincrement=True)
    title=Column(String, nullable=False)
    size=Column(Integer,nullable=False)
    maker=Column(String,nullable=False)
          
    price_reference=relationship("Reference_Prices",back_populates="product_name")


class Reference_Prices (Base):
    __tablename__='reference_prices'

    id=Column(Integer,primary_key=True,index=True, autoincrement=True)
    id_product_reference=Column(Integer,ForeignKey("reference_products.id"))
    category_id=Column(Integer,ForeignKey("categories.id"))
    date=Column(DATE, nullable=False)
    notes=Column(String)
    price=Column(Integer,nullable=False)
          
    group=relationship("Category",back_populates="source")
    product_name=relationship("Reference_Products",back_populates="price_reference")
