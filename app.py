from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel  # Importa as classes de recursos para manipulação de hotéis.
from resources.usuario import User, UserRegister, UserLogin, UserLogout, UserConfirm  # Importa as classes de recursos para manipulação de usuários
from resources.site import Site, Sites  # Importa as classes de recursos para manipulação de sites
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST  # Importa a lista negra de tokens JWT

# Caminho para o banco de dados SQLite
caminho_banco = r'C:\Users\lfsoares\OneDrive - Sistema FIEMG\Área de Trabalho\LUIZ\8.Cursos\2.REST_APIs_Flask\app\banco.db'

# Instancia o aplicativo Flask
app = Flask(__name__)

# Configurações do banco de dados e autenticação JWT
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{caminho_banco}'  # Caminho do banco de dados
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa o rastreamento de modificações
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'  # Chave secreta para JWT
app.config['JWT_BLACKLIST_ENABLED'] = True  # Habilita a lista negra para tokens revogados

# Instancia a API do Flask-RESTful e o gerenciador JWT
api = Api(app)
jwt = JWTManager(app)

# Função antes de cada requisição para criar o banco de dados, se necessário
@app.before_request
def cria_banco():
    """Cria o banco de dados e suas tabelas antes da primeira requisição."""
    banco.create_all()

# Função para verificar se o token está na lista negra
@jwt.token_in_blocklist_loader
def verifica_blacklist(jwt_header, jwt_data):
    return jwt_data['jti'] in BLACKLIST  # Verifica se o token está na blacklist

# Função que retorna mensagem de erro quando o token é revogado
@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_data):
    return jsonify({'message': 'You have been logged out'}), 401  # Resposta de token inválido

# Adiciona os endpoints da API para os recursos definidos
api.add_resource(Hoteis, '/hoteis')  # Endpoint para listar todos os hotéis
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')  # Endpoint para manipular um hotel específico
api.add_resource(User, '/usuarios/<int:user_id>')  # Endpoint para manipular usuário pelo ID
api.add_resource(UserRegister, '/cadastro')  # Endpoint para registrar um novo usuário
api.add_resource(UserLogin, '/login')  # Endpoint para login de usuário
api.add_resource(UserLogout, '/logout')  # Endpoint para logout de usuário
api.add_resource(Sites, '/sites')  # Endpoint para listar sites
api.add_resource(Site, '/site/<string:url>')  # Endpoint para manipular site específico
api.add_resource(UserConfirm, '/confirmacao/<int:user_id>')

if __name__ == '__main__':
    # Importa o banco de dados e inicializa o aplicativo
    from sql_alchemy import banco
    banco.init_app(app)
    # Executa o servidor de desenvolvimento Flask
    app.run(debug=True)

# Como acessar os recursos:
# 1. Lista de hotéis: GET em http://127.0.0.1:5000/hoteis
# 2. Operações em um hotel específico: GET/POST/PUT/DELETE em http://127.0.0.1:5000/hoteis/<hotel_id>
