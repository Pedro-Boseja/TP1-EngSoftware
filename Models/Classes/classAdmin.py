from .classUsuario import Usuario
import pymysql

class Admin(Usuario):
    def __init__(self, email, senha):
        """
        Inicializa a instância da classe Admin, que herda de Usuario.
        O atributo 'type' é automaticamente definido como 1 para Admin.
        """
        super().__init__(email, senha, tipo=1)  # tipo=1 identifica administrador

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
            cursor.execute("INSERT INTO administradores (email, senha, type) VALUES (%s, %s, %s)",
                            (self.__email, self.__senha, self.__type))
            conn.commit()
        except pymysql.err.IntegrityError:
            print(f"Usuário com email '{self.__email}' já existe.")
        finally:
            conn.close()

    def __repr__(self):
        return f"Admin(email={self.get_email()}, type={self.get_type()})"
    

