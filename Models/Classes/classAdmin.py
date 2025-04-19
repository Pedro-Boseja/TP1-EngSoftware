from .classUsuario import Usuario
import pymysql

class Admin(Usuario):
    def __init__(self, email, senha):
        """
        Inicializa a instância da classe Admin, que herda de Usuario.
        O atributo 'tipo' é automaticamente definido como 1 para Admin.
        """
        super().__init__(email, senha, tipo=1)  # tipo=1 identifica administrador

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
                CREATE TABLE IF NOT EXISTS Administradores (
                    email VARCHAR(255) PRIMARY KEY,
                    senha VARCHAR(255) NOT NULL,
                    tipo INT NOT NULL
                )
            ''')

            # Insere o usuário
            cursor.execute(
                "INSERT INTO Administradores (email, senha, tipo) VALUES (%s, %s, %s)",
                (self.get_email(), self.get_senha(), self.get_type())
            )
            conn.commit()
            return True  # sucesso
        except pymysql.err.IntegrityError:
            print(f"Usuário com email '{self.get_email()}' já existe.")
            return False
        except Exception as e:
            print(f"Erro ao salvar admin no banco: {e}")
            return False
        finally:
            conn.close()

    def __repr__(self):
        return f"Admin(email={self.get_email()}, tipo={self.get_type()})"
