from .classUsuario import Usuario

class Admin(Usuario):
    def __init__(self, email, senha):
        """
        Inicializa a instância da classe Admin, que herda de Usuario.
        O atributo 'type' é automaticamente definido como 1 para Admin.
        """
        super().__init__(email, senha, tipo=1)  # tipo=1 identifica administrador

    def __repr__(self):
        return f"Admin(email={self.get_email()}, type={self.get_type()})"
    

