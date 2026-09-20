from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, id, usuario, email, password):
        self.id = id
        self.usuario = usuario
        self.email = email
        self.password = password