import pymysql

class Usuario:
    def __init__(self, email, senha, tipo=0):
        """
        Inicializa a instância da classe Usuario e salva no banco de dados.
        """
        self.__email = email
        self.__senha = senha
        self.__type = tipo  # tipo pode ser personalizado

        # Salvar no banco de dados
        self.salvar_no_banco()

    def salvar_no_banco(self):
        """
        Salva o usuário no banco de dados MySQL via PyMySQL.
        """
        try:
            # Conexão com o banco de dados MySQL
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='senha',
                database='sistema_avaliacao',
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = conn.cursor()

            # Cria a tabela se não existir
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    email VARCHAR(255) PRIMARY KEY,
                    senha VARCHAR(255) NOT NULL,
                    type INT NOT NULL
                )
            ''')

            # Insere o usuário
            cursor.execute("INSERT INTO usuarios (email, senha, type) VALUES (%s, %s, %s)",
                           (self.__email, self.__senha, self.__type))
            conn.commit()
        except pymysql.err.IntegrityError:
            print(f"Usuário com email '{self.__email}' já existe.")
        finally:
            conn.close()

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
