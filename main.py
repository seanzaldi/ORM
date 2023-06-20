#################################
# Sebastian Anz.

# ORM - API - Primeros pasos
# V1.2
#################################




from datetime import date
from fastapi import FastAPI 
from fastapi import status
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import Response
import uvicorn
from sqlalchemy.orm import Session
from database import sessionLocal, engine
import schemas
import models
import crud
import utils



tags_metadata = [
    {
        "name": "Home",
        "description": "Endpoint raiz",
    },
    {
        "name": "Comercios",
        "description": "Operaciones habilitadas para los **Comercios**",
    },
    {
        "name": "Gobierno",   
        "description": "Operaciones habilitadas exclusivamente para el **Gobierno**",
    },
     {
        "name": "Consultas generales",   
        "description": "Consultas Publicas",
    },
    ]


app = FastAPI(title="API Precios Maximos",description="ORM - Primeros pasos",\
            version="1.2",\
            contact={
                    "name":"Sebastian Anz",\
                    "email":"sanz@albertcapacitacion.com"\
                    },
            openapi_tags=tags_metadata
            )


# Dependency
def get_db():
    db = sessionLocal ()
    try:
        #generador
        yield db
    finally:
        db.close()



########################################################################################################
# CREAR TABLAS EN LA BD

models.Base.metadata.create_all(bind=engine)



########################################################################################################
# HOME

@app.get("/",tags=["Home"])
def home():
    """
    Practico ORM - Precios cuidados.
    """
    return{"API para controlar precios."}



########################################################################################################
# ALTAS

#Alta de Comercio
@app.post("/shops", status_code=status.HTTP_201_CREATED, tags=["Comercios"])
def create_shop(shop: schemas.Shop, db: Session = Depends(get_db)):
    """
    Alta de comercio.
    """
    #pregunta si el comercio existe, si existe Exeption.
    db_shop = crud.get_shop_by_cuit(db, cuit=shop.cuit)
    if db_shop:
        raise HTTPException(status_code=409, detail="Shop already registered")

    status = crud.create_shop(db=db, store=shop)
    if status == 'Resource created':
        return {'message':status}
    else:
        raise HTTPException(status_code=422, detail="Can't create the register")


#Alta de categoria
@app.post("/category", status_code=status.HTTP_201_CREATED, tags=["Gobierno"])
def create_category(category: schemas.Category, db: Session = Depends(get_db)):
    """
    Alta de categoria.
    """
    #pregunta si la category existe, si existe Exeption.
    db_category = crud.get_category_by_title(db, title=category.title)
    if db_category:
        raise HTTPException(status_code=409, detail="Category alrready registered")
    status = crud.create_category(db=db, type_product=category)
    if status == 'Resource created':
        return {'message':status}
    else: 
        raise HTTPException(status_code=422, detail="Can't create the register")
    

#Alta de producto - venta al publico
@app.post("/product", status_code=status.HTTP_201_CREATED, tags=["Comercios"])
def create_product(product:schemas.Product, db: Session = Depends(get_db)):
    """
    Alta de producto y valor de venta al publico.
    """
    #pregunta si el Shop_ID, title, para una FECHA dada ya existen. En caso afirmativo Exeption.
    db_product = crud.get_producto_by_shop_id_and_date(db, title=product.title, shop_id=product.shop_id, date_register=product.date)
    if db_product:
        raise HTTPException(status_code=409, detail="Product alrredy registered")
    
    status = crud.create_product(db=db, new_product=product)
    if status == 'Resource created':
        return {'message':status}
    else: 
        raise HTTPException(status_code=422, detail="Can't create the register")
    

#Alta producto de referencia
@app.post("/reference/product", status_code=status.HTTP_201_CREATED, tags=["Gobierno"])
def create_reference_product(reference: schemas.Reference_Products, db: Session = Depends(get_db)):
    """
    Alta de nuevo producto al programa Precios Maximos.
    """
    db_reference = crud.get_product_reference(db, title=reference.title, size=reference.size, maker=reference.maker)
    if db_reference:
        raise HTTPException(status_code=409, detail="Reference product alrready registered")
    status = crud.create_product_reference(db=db, product_reference=reference)
    if status == 'Resource created':
        return {'message':status}
    else: 
        raise HTTPException(status_code=422, detail="Can't create the register")
    

#Alta precio de referencia
@app.post("/reference/price", status_code=status.HTTP_201_CREATED, tags=["Gobierno"])
def create_reference_price(reference: schemas.Reference_Prices, db: Session = Depends(get_db)):
    """
    Alta de nuevo precio maximo para un producto previamente includio en el programa.
    """
    #pregunta si el ID para una FECHA dada existen, si es asi Exeption.
    db_reference = crud.get_price_reference(db, id_product_reference=reference.id_product_reference,category_id=reference.category_id,date=reference.date)
    if db_reference:
        raise HTTPException(status_code=409, detail="Reference price alrredy registered")
    status = crud.create_price_reference(db=db, price_reference=reference)
    if status == 'Resource created':
        return {'message':status}
    else: 
        raise HTTPException(status_code=422, detail="Can't create the register")
 


########################################################################################################
# CONSULTAS

# Comercio
@app.get("/shops", tags=["Consultas generales"])
def read_shop(cuit:int, db: Session = Depends(get_db)):
    """
    Datos de comercio.
    """
    db_shop = crud.get_shop_by_cuit(db, cuit=cuit)
    if db_shop:     
        response_dict = {
                    "cuit":db_shop.cuit,
                    "name": utils.convert_title(db_shop.name),
                    "phone":db_shop.tel,
                    "adress":utils.convert_capitalize(db_shop.address),
                    "email":db_shop.email,
        }
        return response_dict    #No devuelvo la pass.
    else:
        return Response (status_code=status.HTTP_204_NO_CONTENT)
        

# Categoria
@app.get("/category",tags=["Consultas generales"])
def read_category(category_id: int = None, title: str = None, description: str = None, db: Session = Depends(get_db)):
    """
    Informacion de una categoria.
    """
    db_category = crud.get_category_by_id_title_description(db, category_id=category_id, title=title, description=description)
    if db_category:
        return db_category
    else:
        return Response (status_code=status.HTTP_204_NO_CONTENT)


# Producto
@app.get("/product", tags=["Consultas generales"])
def read_product(title: str = None, id: int = None, shop_id: int = None, category_id: int = None, maker: str = None, load_date: date = None, db: Session = Depends(get_db)):
    """
    Consulta de productos ingresados por los comercios y valores de comercializacion.
    """
    db_product = crud.get_product_by_title_shopid_maker_id_date_categoryid(db, id=id, shop_id=shop_id, category_id=category_id, load_date=load_date, title=title, maker=maker)
    if db_product:
        return db_product
    else:
        return Response (status_code=status.HTTP_204_NO_CONTENT)

#LOS CAMPOS DEL TIPO INT NO PUEDEN  ESTAR VACIOS AL MOSMENTO DE HACER EL GET. 
#TENER EN CUENTA QUE ESTOY HACIENDO CONSULTAS DEL TIPO "OR". ESTO SUCEDE EN POSTMAN
#YA QUE AHI PUEDO PONER UN QUERY PARAMETER SIN NIGUNO VALOR, NO ASI EN LA DOCUMENTACION DE FASTAPI.
#AHI CAMPO QUE NO COMPLETO, CAMPO QUE NO SE PONE EN LA URL PARA HACER EL QUERY PARAMETER.


# Precio testigo o de referencia
@app.get("/reference", tags=["Consultas generales"])
def read_reference(category_id: int = None, title: str = None, id_product_reference: int = None, db: Session = Depends(get_db)):
    """
    Consulta de precio acordado por el Nombre Comercial, el ID de referencia o el ID de categoria.
    Tener en cuenta que un producto posiblemente tenga varios precios acordados en el tiempo.
    La consulta por categoria despliega todos los productos acordados para la misma.
    """
        
    db_reference = crud.get_reference_by_categoryID_or_title_or_IDreference(db, category_id=category_id, title=title, id_product_reference=id_product_reference)
    if db_reference:
        return db_reference
    else:
        return Response (status_code=status.HTTP_204_NO_CONTENT)
        

# Verificar contraseña
@app.get("/shops/verify", tags=["Comercios"])
def verify_pass(cuit:int, password: str, db: Session = Depends(get_db)):
    """
    Validación.
    """
    db_shop = crud.get_shop_by_cuit(db, cuit=cuit)
    if db_shop:
        if utils.verify_password(password, db_shop.password):
            return Response (status_code=status.HTTP_202_ACCEPTED)
        else:
            return Response (status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response (status_code=status.HTTP_204_NO_CONTENT)




########################################################################################################
# PRECIOS POR ENCIMA DE LOS VALORES DE REFERENCIA

# Selecciono una categoria de la tabla categorias, busco la misma en la tabla referencias los precios de esa
# categoria y me quedo con la fecha mas reciente. Obtengo el precio.
# Busco en Products aquellos que, para esa categoria y que en una fecha Mayor o menor, 
# tengan un precio mayor al obtenido anteriormente.
# Informo producto y shop

@app.get("/prices_above_limit", tags=["Gobierno"])
def expensive_products(category_title: str, db: Session = Depends(get_db)):
    """
    Productos que superan los valores maximos acordados.
    """
    db_products_above_limit = crud.get_products_above_reference(db,category_title=category_title)
    if db_products_above_limit:
        return db_products_above_limit
    else:
        return Response (status_code=status.HTTP_204_NO_CONTENT)
        




########################################################################################################
# Daemon
if __name__ == "__main__":
       
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000,
        log_level="info",
        reload=True 
    )














