import unittest
from datetime import datetime
import requests



class consultas_precios_comercios_categorias (unittest.TestCase):

        def setUp (self):
                self.url="http://127.0.0.1:8000/"

        def test_la_API_esta_atendiendo_peticiones (self):
               
                #When
                response = requests.get(self.url) 
                
                #Then
                self.assertEqual(response.status_code, 200, "API no responde")

        def test_si_consulta_categoria_esta_disponible (self):
               
                #Give
                category_id = 2
               
                #When
                response = requests.get (self.url+'category?category_id='+str(category_id))
               
                #Then
                self.assertEqual(response.status_code, 200, "La categoria no fue encontrada")
        
        def test_si_consulta_datos_de_contacto_de_un_comercio_esta_disponible (self):
               
                #Give
                cuit = 23456789234
               
                #When
                response = requests.get(self.url+'shops?cuit='+str(cuit))
               
                #Then
                self.assertEqual(response.status_code, 200, "El CUIT no fue encontrado")

        def test_si_consulta_precios_por_encima_de_los_acuerdos_esta_disponible (self):
                
                #Give
                categoria = 'Harina 0000'
                
                #When
                response = requests.get (self.url+'prices_above_limit?category_title='+categoria)
                
                #Then
                self.assertEqual(response.status_code, 200, "No hay productos que esten por encima de los valores de referencia")
                

        def test_consulta_precios_por_arriba_de_los_acuerdos_funciona_correctamente (self):
                # Voy a verificar que la respuesta efectivamente es un precio que esta por encima de un precio de referencia.
                
                #Give
                # categoria = 'Harina 0000'
                categoria = 'leche'
                
                #When
                #Precios de Referencia
                categoria_response = requests.get (self.url+'category?title='+categoria)
                data_categoria = categoria_response.json()
                id_categoria_producto = data_categoria['id']
                referencia = requests.get (self.url+'reference?category_id='+str(id_categoria_producto))
                referencia_data = referencia.json()
                
                precio_referencia = referencia_data[0]['price']
                fecha_referencia = datetime.strptime(referencia_data[0]['date'], "%Y-%m-%d").date()
                
                if len(referencia_data) > 1:
                        for obj in referencia_data [1:]:
                                fecha_siguiente_json = datetime.strptime(obj['date'], "%Y-%m-%d").date()
                                if fecha_siguiente_json > fecha_referencia:
                                        precio_referencia = obj['price']
                                        fecha_referencia = fecha_siguiente_json

                #Then
                # Productos caros, precios superan los acuerdos. Consulta principal a controlar
                response = requests.get (self.url+'prices_above_limit?category_title='+categoria)
                data_precios_elevados = response.json()

                for obj in data_precios_elevados:
                        fecha_relevada_producto = datetime.strptime (obj['date'], "%Y-%m-%d").date()
                        self.assertGreater (obj['price'],precio_referencia, "La evalucion de precios elevados no fue correcta, un precio reportado cumplia el acuerdo")
                        self.assertGreater (datetime.strptime(obj['date'], "%Y-%m-%d").date(),fecha_referencia, "La evalucion de precios elevados no fue correcta, un producto tenia un precio anterior a la fecha de implementacion")

            
  
if __name__=='__main__':
    unittest.main()






