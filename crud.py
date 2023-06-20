
from datetime import date,timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.orm import joinedload
import models, schemas, utils






########################################################################################################
# INSERTS

# Alta Comercio 
def create_shop(db: Session, store: schemas.Shop):
    hashed_password = utils.hash_password(store.password)
    db_store = models.Shop(
                        cuit=store.cuit, 
                        name=store.name.lower(), 
                        password=hashed_password, 
                        tel=store.tel, 
                        address=store.address.lower(), 
                        email=store.email.lower()
                        )
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return 'Resource created'
    

# Alta de Categoria 
def create_category(db: Session, type_product: schemas.Category):
    db_type_product = models.Category(
                        title=type_product.title.lower(), 
                        description=type_product.description.lower()
                        )
    db.add(db_type_product)
    db.commit()
    db.refresh(db_type_product)
    return 'Resource created'


# Alta Producto 
def create_product(db:Session,new_product:schemas.Product):
    # PROBANDO EL FORMATEO DE FECHA (notar sutil diferencia entre strP... y strF...)
    # new_date = datetime.strptime(new_product.date, "%Y-%m-%d")
    # format_date=new_date.strftime("%Y-%m-%d")
    db_new_product = models.Product(
                            shop_id=new_product.shop_id, 
                            date=new_product.date, 
                            category_id=new_product.category_id, 
                            title=new_product.title.lower(), 
                            size=new_product.size, 
                            maker=new_product.maker.lower(), 
                            notes=new_product.notes.lower(), 
                            price=new_product.price
                            )
    db.add(db_new_product)
    db.commit()
    db.refresh(db_new_product)
    return 'Resource created'


# Alta producto de Referencia
def create_product_reference (db:Session, product_reference: schemas.Reference_Products):
    db_product_reference = models.Reference_Products(
                            title=product_reference.title.lower(), 
                            size=product_reference.size, 
                            maker=product_reference.maker.lower()
                            )
    db.add(db_product_reference)
    db.commit()
    db.refresh(db_product_reference)
    return 'Resource created'
    

# Alta precio de Referencia
def create_price_reference (db:Session, price_reference: schemas.Reference_Prices):
    db_price_reference = models.Reference_Prices(
                    id_product_reference=price_reference.id_product_reference, 
                    category_id=price_reference.category_id, 
                    date=price_reference.date, 
                    notes=price_reference.notes.lower(), 
                    price=price_reference.price
                    )
    db.add(db_price_reference)
    db.commit()
    db.refresh(db_price_reference)
    return 'Resource created'



########################################################################################################
# SELECTS

# Validacion de existencia previa de una Categoria OK
def get_category_by_title(db: Session, title: str):
    return db.query(models.Category).filter((models.Category.title == utils.convert_lowercase(title))).all()


# Validacion de existencia previa de un Producto incluido en el programa OK
def get_product_reference (db: Session, title: str, size: int, maker: str):
    return db.query(models.Reference_Products).filter(and_(
                                models.Reference_Products.title == utils.convert_lowercase(title), 
                                models.Reference_Products.size == size, 
                                models.Reference_Products.maker == utils.convert_lowercase(maker))).all()


# Validacion de existencia previa de un precio de Referencia OK
def get_price_reference(db: Session, id_product_reference: int, category_id: int, date: date):
    return db.query(models.Reference_Prices).filter(and_(
                            models.Reference_Prices.id_product_reference == id_product_reference, 
                            models.Reference_Prices.category_id == category_id, 
                            models.Reference_Prices.date == date)).all()


# Validacion de existencia previa de Producto de venta al publico OK
def get_producto_by_shop_id_and_date(db:Session, title:str, shop_id=int,date_register=date):
    return db.query(models.Product).filter(and_(
                                models.Product.title == utils.convert_lowercase(title), 
                                models.Product.shop_id==shop_id, 
                                models.Product.date == date_register)).first()


# Comercio - Consulta general y validacion de existencia previa. OK
def get_shop_by_cuit(db: Session, cuit: int):
    return db.query(models.Shop).filter(models.Shop.cuit == cuit).first()


# Consulta Categoria OK
def get_category_by_id_title_description(db: Session, category_id: int, title: str, description: str = None):
    
    if title is not None:
        # title = title.lower()
        title = utils.convert_lowercase(title)
    if description is not None:
        # description = description.lower()
        description = utils.convert_lowercase(description)
    
    return db.query(models.Category).filter(
                            (models.Category.id == category_id)|
                            (models.Category.title == title)|
                            (models.Category.description == description)).first()


# Consulta Producto OK
def get_product_by_title_shopid_maker_id_date_categoryid(db: Session, id: int = None, shop_id: int = None, category_id: int = None, load_date: date = None, title: str = None, maker: str = None):
    
    if title is not None:
        title = utils.convert_lowercase(title)
    if maker is not None:
        maker = utils.convert_lowercase(maker)
    
    return db.query(models.Product).filter(
                            (models.Product.id == id)|
                            (models.Product.shop_id == shop_id)|
                            (models.Product.category_id == category_id)|
                            (models.Product.date == load_date)|
                            (models.Product.title == title)|
                            (models.Product.maker == maker)).all()


# ESTARIA FUNCIONANDO PERO LA INFO QUE ME TRAE ES DE UNA SOLA TABLA. TAMBIEN VER QUE ME TRAE TODOS LOS PRECIOS ACORDADOS PARA UNA CATEGORIA
# POR AHI CONVIENE QUEDARSE SOLO CON EL ULTIMO, POR FECHA.
# Consulta Producto/Precio de Referencia 
def get_reference_by_categoryID_or_title_or_IDreference(db: Session, category_id: int = None, title: str = None, id_product_reference: int = None):
    
    if title is not None:
        title = utils.convert_lowercase(title)

    return db.query(models.Reference_Prices).join(models.Reference_Products).filter(
                                (models.Reference_Prices.category_id == category_id)|
                                (models.Reference_Prices.id_product_reference == id_product_reference)|
                                (models.Reference_Products.title == title)).all()


# CONSULTA PRINCIPAL, precios por encima de los valores acordados OK!!!!!!!!!!
def get_products_above_reference(db: Session, category_title: str):
    category_data= db.query(models.Category).filter(models.Category.title==utils.convert_lowercase(category_title)).first()
    reference_price= db.query(models.Reference_Prices).filter(models.Reference_Prices.category_id == category_data.id).all()
    last_object_reference_price = reference_price[-1]
    last_reference_price_date = last_object_reference_price.date
    final = db.query(models.Product).filter(and_(
                                    models.Product.date>=last_reference_price_date, 
                                    models.Product.date<=last_reference_price_date+timedelta(days=60),  
                                    models.Product.category_id == last_object_reference_price.category_id,
                                    models.Product.price > last_object_reference_price.price)
                                    ).options(joinedload(models.Product.seller).defer(models.Shop.password)).all()
    return final
    








   
    






