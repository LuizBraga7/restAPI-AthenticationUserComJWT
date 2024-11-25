from sql_alchemy import banco  # Importa a instância do banco de dados.

class UsuarioModel(banco.Model):
    """
    Representa um modelo para a tabela 'usuarios' no banco de dados.
    """

    # Define o nome da tabela.
    __tablename__ = 'usuarios'

    # Define as colunas da tabela.
    user_id = banco.Column(banco.Integer, primary_key=True)  # ID único do usuário.
    login = banco.Column(banco.String(40))  # Login do usuário.
    senha = banco.Column(banco.String(40))  # Senha do usuário.

    def __init__(self, login, senha):
        """
        Inicializa os atributos do usuário.
        """
        self.login = login
        self.senha = senha

    def json(self):
        """
        Retorna os dados do usuário no formato JSON.
        """
        return {
            'user_id': self.user_id,  # Identificador único do usuário.
            'login': self.login       # Login do usuário (não retorna a senha por segurança).
        }
    
    @classmethod
    def find_user(cls, user_id):
        """
        Busca um usuário pelo ID.
        """
        return cls.query.filter_by(user_id=user_id).first()
    
    @classmethod
    def find_by_login(cls, login):
        """
        Busca um usuário pelo login.
        """
        return cls.query.filter_by(login=login).first()

    def save_user(self):
        """
        Salva o usuário no banco de dados.
        """
        banco.session.add(self)
        banco.session.commit()
    
    def delete_user(self):
        """
        Remove o usuário do banco de dados.
        """
        banco.session.delete(self)
        banco.session.commit()
