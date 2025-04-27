import pymysql

class Disciplina:
    def __init__(self, codigo, nome):
        """
        Inicializa uma disciplina com código e nome.
        """
        self.__codigo = codigo
        self.__nome = nome

    def salvar_no_banco(self) -> bool:
        """
        Salva a disciplina no banco de dados.
        """
        sucesso = False
        try:
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
                CREATE TABLE IF NOT EXISTS sistema_avaliacao.Disciplinas (
                    codigo VARCHAR(50) PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL
                )
            ''')

            # Insere a disciplina
            cursor.execute(
                "INSERT INTO sistema_avaliacao.Disciplinas (codigo, nome) VALUES (%s, %s)",
                (self.__codigo, self.__nome)
            )
            conn.commit()
            sucesso = True
        except pymysql.err.IntegrityError:
            print(f"Disciplina com código '{self.__codigo}' já existe.")
            sucesso = False
        except Exception as e:
            print(f"Erro ao salvar disciplina: {e}")
            sucesso = False
        finally:
            conn.close()
            return sucesso

    def __repr__(self):
        return f"Disciplina(codigo={self.__codigo}, nome={self.__nome})"

    @staticmethod
    def listar_disciplinas():
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='senha',
            database='sistema_avaliacao',
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sistema_avaliacao.Disciplinas")
        disciplinas = cursor.fetchall()
        conn.close()
        return disciplinas

    @staticmethod
    def excluir_disciplina(codigo):
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='senha',
            database='sistema_avaliacao',
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sistema_avaliacao.Disciplinas WHERE codigo = %s", (codigo,))
        conn.commit()
        conn.close()

    # Getters
    def get_codigo(self):
        return self.__codigo

    def get_nome(self):
        return self.__nome
