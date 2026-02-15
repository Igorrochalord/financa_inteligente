import bcrypt
from src.database import db

def register_user(username, password, name, salario=0.0):
    users_col = db.get_collection('users')
    if users_col is None: return None, "Erro de Banco de Dados"

    if users_col.find_one({'username': username}):
        return None, "Usuário já existe!"
    
    # Criptografia
    bytes_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes_password, salt)
    
    new_user = {
        'username': username,
        'password': hashed_password.decode('utf-8'),
        'name': name,
        'salario': float(salario) # Novo campo Salário
    }
    
    users_col.insert_one(new_user)
    
    # Retorna o próprio usuário para login automático
    return new_user, "Conta criada! Entrando..."

def login_user(username, password):
    users_col = db.get_collection('users')
    if users_col is None: return None

    user = users_col.find_one({'username': username})
    
    if user:
        bytes_password = password.encode('utf-8')
        hashed_password = user['password'].encode('utf-8')
        
        if bcrypt.checkpw(bytes_password, hashed_password):
            return user
            
    return None