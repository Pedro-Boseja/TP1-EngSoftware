from .classUsuario import Usuario
import pymysql
import config

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
                password=config.senha_banco,
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

            if self._is_email_ja_cadastrado(self.get_email()):
                return False

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
        except Exception as e:
            return False
        finally:
            conn.close()

    def get_nome(self):
        return self.__nome

    def get_matricula(self):
        return self.__matricula
    
    def _is_email_ja_cadastrado(self, email):
        """
        Verifica se o email já existe no banco de dados.
        """
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password=config.senha_banco,
            database='sistema_avaliacao',
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sistema_avaliacao.Professores WHERE email = %s', (email,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def __repr__(self):
        return f"Professor(nome={self.nome}, matricula={self.matricula}, email={self.get_email()}, type={self.get_type()})"
