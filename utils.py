
import bcrypt


#Todas a minusculas
def convert_lowercase (characters: str)->str:
    new_characters = characters.lower()
    return new_characters

#Primer letra de cada plabra en Mayuscula
def convert_title (characters: str)->str:
    new_characters = characters.title()
    return new_characters

#Primer letra del String
def convert_capitalize (characters: str)->str:
    new_characters = characters.capitalize()
    return new_characters

#Codificar Password
def hash_password(password):
    # Genera una valor aleatorio para ser agregado a la contraseña.
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    # Retorna el hash
    return hashed_password.decode('utf-8')

#Verificar Password
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))



