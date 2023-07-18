



# Intrucciones:
# Para poder realizar esta prueba el MAIN del ORM debe estar ejecutandose previamente por un lado. Por otro, en una session diferente de VSC u otro IDE, lanzar este script.
# Si luego de la corrida completa no hubo salida alguna por STDOUT, significa que los tests fueron exitosos.

import requests

# #######################################################################################################
# CONSULTA COMERCIO 

# !!!!!!!!!VERSION MUY BASICA
url = 'http://127.0.0.1:8000/shops?cuit=23456789234' 
response = requests.get(url)
if response.status_code == 200:  
    data = response.json()  
else:
    print('Error en Consulta Comercio por CUIT. Código de estado:', response.status_code)


# !!!!!!!!!VERSION CON ASSERT
url = 'http://127.0.0.1:8000/shops'
cuit = 23456789234
def consulta_comercio (url : str, cuit):
    cuit_str  = str(cuit)
    data = requests.get (url+'?cuit='+cuit_str)
    assert data.status_code == 200, "No se pudo realizar la consulta de un comercio"
    return data.json()
 
# print (consulta_comercio(url, cuit))
consulta_comercio(url, cuit)


########################################################################################################
# CONSULTA CATEGORIA

# !!!!!!!!!VERSION MUY BASICA
url = 'http://127.0.0.1:8000/category?category_id=1' 
response = requests.get(url)
if response.status_code != 200:  
    print('La consulta por ID CATEGORIA no fue exitosa. Código de estado:', response.status_code)

url = 'http://127.0.0.1:8000/category?title=leche'
response = requests.get(url)
if response.status_code != 200:  
    print('La consulta por NOMBRE DE CATEGORIA no fue exitosa. Código de estado:', response.status_code)

url = 'http://127.0.0.1:8000/category?description=lacteos'
response = requests.get(url)
if response.status_code != 200:  
    print('La consulta por DESCRIPCION DE CATEGORIA no fue exitosa. Código de estado:', response.status_code)


# !!!!!!!!!VERSION CON ASSERT - CATEGORIA ID
url = 'http://127.0.0.1:8000/category' 
category_id = 1
def consulta_categoria (url : str, category_id):
    category_id_str  = str(category_id)
    data = requests.get (url+'?category_id='+category_id_str)
    assert data.status_code == 200, "No se pudo realizar la consulta CATEGORIA ID"
    return data.json()

# print (consulta_categoria(url, category_id))
consulta_categoria(url, category_id)


# !!!!!!!!!VERSION CON ASSERT - TITLE
url = 'http://127.0.0.1:8000/category' 
title = 'LECHE'
def consulta_categoria (url : str, title : str):
    data = requests.get (url+'?title='+title)
    assert data.status_code == 200, "No se pudo realizar la consulta CATEGORIA POR NOMBRE"
    return data.json()

# print (consulta_categoria(url, title))
consulta_categoria(url, title)


# !!!!!!!!!VERSION CON ASSERT - DESCRIPTION
url = 'http://127.0.0.1:8000/category' 
description = 'LacTEos'
def consulta_categoria (url : str, description : str):
    data = requests.get (url+'?description='+description)
    assert data.status_code == 200, "No se pudo realizar la consulta CATEGORIA POR DESCRIPCION"
    return data.json()

# print (consulta_categoria(url, description))
consulta_categoria(url, description)



########################################################################################################
# CONSULTA REFERENCIAS

# !!!!!!!!!!VERSION MUY BASICA
url = 'http://127.0.0.1:8000/reference?category_id=1' 
response = requests.get(url)
if response.status_code != 200:  
    print('La consulta por ID REFERENCIA no fue exitosa. Código de estado:', response.status_code)

url = 'http://127.0.0.1:8000/reference?title=La%20martona'
response = requests.get(url)
if response.status_code != 200:  
    print('La consulta por NOMBRE DE REFERENCIA no fue exitosa. Código de estado:', response.status_code)


# !!!!!!!!!VERSION CON ASSERT - CATEGORY ID
url = 'http://127.0.0.1:8000/reference' 
category_id = 1
def consulta_referencia (url : str, category_id : int):
    category_id_str = str(category_id)
    data = requests.get (url+'?category_id='+category_id_str)
    assert data.status_code == 200, "No se pudo realizar la consulta por ID de REFERENCIA"
    return data.json()

# print (consulta_referencia(url, category_id))
consulta_referencia(url, category_id)


# !!!!!!!!!VERSION CON ASSERT - TITLE
url = 'http://127.0.0.1:8000/reference' 
title = 'creMON'
def consulta_referencia (url : str, title : str):
    data = requests.get (url+'?title='+title)
    assert data.status_code == 200, "No se pudo realizar la consulta por NOMBRE DE REFERENCIA"
    return data.json()

# print (consulta_referencia(url, title))
consulta_referencia(url, title)



########################################################################################################
# CONSULTA PRODUCTOS INGRESADOS POR LOS COMERCIOS

# !!!!!!!!!VERSION MUY BASICA
url = 'http://127.0.0.1:8000/product?title=cindor' 
response = requests.get(url)
if response.status_code != 200:  
    print('La consulta por NOMBRE DE PRODUCTO no fue exitosa. Código de estado:', response.status_code)

url = 'http://127.0.0.1:8000/product?id=1'
response = requests.get(url)
if response.status_code != 200:  
    print('La consulta por ID DE PRODUCTO no fue exitosa. Código de estado:', response.status_code)

# url = 'http://127.0.0.1:8000/product?shop_id=1'
response = requests.get(url)
if response.status_code != 200:  
    print('La consulta por PRODUCTO POR COMERCIO no fue exitosa. Código de estado:', response.status_code)

# url = 'http://127.0.0.1:8000/product?maker=mastellone'
response = requests.get(url)
if response.status_code != 200:  
    print('La consulta PRODUCTO POR FABRICANTE no fue exitosa. Código de estado:', response.status_code)

# url = 'http://127.0.0.1:8000/product?load_date=2023-05-15'
response = requests.get(url)
if response.status_code != 200:  
    print('La consulta por FECHA DE CARGA DE PRODUCTO no fue exitosa. Código de estado:', response.status_code)



# !!!!!!!!!VERSION CON ASSERT - TITLE
url = 'http://127.0.0.1:8000/product' 
title = 'cinDor'
def consulta_productos (url : str, title : str):
    data = requests.get (url+'?title='+title)
    assert data.status_code == 200, "No se pudo realizar la consulta por NOMBRE DE PRODUCTO"
    return data.json()

# print (consulta_productos(url, title))
consulta_productos(url, title)


# !!!!!!!!!VERSION CON ASSERT - ID
url = 'http://127.0.0.1:8000/product' 
id = 1
def consulta_productos (url : str, id : int):
    id_str = str(id)
    data = requests.get (url+'?id='+id_str)
    assert data.status_code == 200, "No se pudo realizar la consulta por ID DE PRODUCTO"
    return data.json()

# print (consulta_productos(url,id))
consulta_productos(url, id)


# !!!!!!!!!VERSION CON ASSERT - SHOP_ID
url = 'http://127.0.0.1:8000/product' 
shop_id = 1
def consulta_productos (url : str, shop_id : int):
    shop_id_str = str(shop_id)
    data = requests.get (url+'?shop_id='+shop_id_str)
    assert data.status_code == 200, "No se pudo realizar la consulta de PRODUCTO POR SHOP ID"
    return data.json()

# print (consulta_productos(url,shop_id))
consulta_productos(url, shop_id)


# !!!!!!!!!VERSION CON ASSERT - FABRICANTE
url = 'http://127.0.0.1:8000/product' 
maker = 'mastellone'
def consulta_productos (url : str, maker : str):
    data = requests.get (url+'?maker='+maker)
    assert data.status_code == 200, "No se pudo realizar la consulta de PRODUCTO POR FABRICANTE"
    return data.json()

# print (consulta_productos(url,maker))
consulta_productos(url, maker)


# !!!!!!!!!VERSION CON ASSERT - FECHA
url = 'http://127.0.0.1:8000/product' 
load_date = '2023-05-15'
def consulta_productos (url : str, load_date : str):
    data = requests.get (url+'?load_date='+load_date)
    assert data.status_code == 200, "No se pudo realizar la consulta de PRODUCTO POR FECHA DE CARGA"
    return data.json()

# print (consulta_productos(url,load_date))
consulta_productos(url, load_date)


# ########################################################################################################
# # ALTA DE NUEVA CATEGORIA (unica alta a modo de ejemplo)


# # !!!!!!!!!VERSION CON ASSERT
# url = 'http://127.0.0.1:8000/category' 
# title='oliVA'
# description='acitES'


# def alta_categoria (url : str, title : str, description : str):
#     new_category_json={
#                     "title": title,
#                     "description": description
#                     }
#     data = requests.post (url,json = new_category_json)
#     assert data.status_code == 200, "No se pudo realizar el ALTA DE LA CATEGORIA"
#     return data.json()

# # print (alta_categoria(url,title, description))
# alta_categoria(url,title, description)


