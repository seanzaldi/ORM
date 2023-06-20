from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# sessionmaker se utiliza normalmente para configurar una instancia de Session con una serie de opciones comunes y, 
# a partir de ahí, crear nuevas instancias de Session según sea necesario. 
# Es una forma de centralizar la configuración y la creación de sesiones en un solo lugar.

# Diferencia entre Session y sessionmaker:
# En resumen, la diferencia clave entre Session y sessionmaker es la siguiente:

# Session es una clase que representa una conexión a la base de datos y proporciona métodos para interactuar con ella.
# sessionmaker es una función que se utiliza para configurar y crear una fábrica de sesiones, es decir, 
# una función u objeto que se invoca para obtener instancias de Session.

sqlalchemy_database_url="sqlite:///./BD.db"
engine=create_engine(sqlalchemy_database_url,connect_args={"check_same_thread":False})
sessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()

