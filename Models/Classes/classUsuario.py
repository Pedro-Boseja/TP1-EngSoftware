class Usuario:
    def __init__(self, email, senha, tipo=0):
        """
        Inicializa a instância da classe Usuario e salva no banco de dados.
        """
        self.__email = email
        self.__senha = senha
        self.__type = tipo  # tipo pode ser personalizado

    def __repr__(self):
        return f"Usuario(email={self.__email}, type={self.__type})"

    def verificar_senha(self, senha_input):
        return self.__senha == senha_input

    def alterar_senha(self, nova_senha):
        self.__senha = nova_senha
        print("Senha alterada com sucesso.")

    def get_email(self):
        return self.__email

    def get_type(self):
        return self.__type

    def set_email(self, novo_email):
        self.__email = novo_email

    def set_type(self, novo_type):
        self.__type = novo_type
