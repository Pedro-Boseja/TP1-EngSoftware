from .classUsuario import Usuario
import pymysql

class Professor(Usuario):
    def __init__(self, nome, matricula, email, senha):
        """
        Inicializa a instância da classe Professor.
        Atributo 'type' definido como 2 (professor).
        """
        self.nome = nome
        self.matricula = matricula
        super().__init__(email, senha, tipo=2)

    def salvar_no_banco(self):
        """
        Salva o professor no banco de dados MySQL via PyMySQL.
        """
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='senha',
                database='sistema_avaliacao',
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sistema_avaliacao.Professores (
                    email VARCHAR(255) PRIMARY KEY,
                    senha VARCHAR(255) NOT NULL,
                    nome VARCHAR(255) NOT NULL,
                    matricula VARCHAR(50) NOT NULL,
                    tipo INT NOT NULL
                )
            ''')

            cursor.execute('''
                INSERT INTO sistema_avaliacao.Professores (email, senha, nome, matricula, tipo)
                VALUES (%s, %s, %s, %s, %s)
            ''', (
                self.get_email(), 
                self.get_senha(), 
                self.nome, 
                self.matricula, 
                self.get_type()
                ))
            
            conn.commit()
            return True  # sucesso
        except pymysql.err.IntegrityError:
            print(f"Professor com email '{self.get_email()}' já existe.")
            return False
        except Exception as e:
            print(f"Erro ao salvar professor no banco: {e}")
            return False
        finally:
            conn.close()

    def get_nome(self):
        return self.__nome

    def get_matricula(self):
        return self.__matricula
    
    def __repr__(self):
        return f"Professor(nome={self.nome}, matricula={self.matricula}, email={self.get_email()}, type={self.get_type()})"
