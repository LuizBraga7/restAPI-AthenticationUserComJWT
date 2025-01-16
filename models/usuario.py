from sql_alchemy import banco  # Importa a instância do banco de dados.
from flask import request, url_for
from requests import post

MAILGUN_DOMAIN = "sandbox9b717522aad84275a9f99b738597e8f9.mailgun.org"
MAILGUN_API_KEY = 1
FROM_TITLE = 1
FROM_EMAIL = 1

class UsuarioModel(banco.Model):
    """
    Representa um modelo para a tabela 'usuarios' no banco de dados.
    """

    # Define o nome da tabela.
    __tablename__ = 'usuarios'

    # Define as colunas da tabela.
    user_id = banco.Column(banco.Integer, primary_key=True)  # ID único do usuário.
    login = banco.Column(banco.String(40), nullable=False, unique=True)  # Login do usuário.
    senha = banco.Column(banco.String(40), nullable=False)  # Senha do usuário.
    email = banco.Column(banco.String(80), nullable=False, unique=True)  # Tipo corrigido
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, senha, email, ativado):
        """
        Inicializa os atributos do usuário.
        """
        self.login = login
        self.senha = senha
        self.email = email
        self.ativado = ativado

    def json(self):
        """
        Retorna os dados do usuário no formato JSON.
        """
        return {
            'user_id': self.user_id,  # Identificador único do usuário.
            'login': self.login,       # Login do usuário (não retorna a senha por segurança).
            'email': self.email,
            'ativado': self.ativado
        }
    
    def send_confirmation_email(self):
    # http://127.0.0.1:5000//confirmacao/1
        link = request.url_root[:-1] + url_for('UserConfirm', user_id=self.user_id)
        return post(f'https://api.mailgun.net/v3{MAILGUN_DOMAIN}/messages',
                    auth=('api', MAILGUN_API_KEY),
                    data={'from': f'{FROM_TITLE} <{FROM_EMAIL}>',
                    'to': self.email,
                    'subject': 'Confirmação de cadastro',
                    'text': f'Confirme seu cadastro clicando no link a seguir: {link}',
                    'html': f'<html><p> Confirme seu cadastro clicando no link a seguir: <a href={link}CONFIRMAR EMAIL</a></p></html>.'
                    })
    
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
