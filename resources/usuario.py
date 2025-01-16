from flask_restful import Resource, reqparse
from models.usuario import UsuarioModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
import hmac
from blacklist import BLACKLIST

# Definindo os parâmetros necessários para os métodos POST (login e senha)
atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help='O campo login não pode ser deixado em branco')
atributos.add_argument('senha', type=str, required=True, help='O campo senha não pode ser deixado em branco')
atributos.add_argument('ativado', type=bool)


# Classe para manipulação de usuários (GET, DELETE)
class User(Resource):
    def get(self, user_id):
        # Procura um usuário pelo ID
        user = UsuarioModel.find_user(user_id)
        if user:
            return user.json(), 200  # Retorna o usuário em formato JSON
        return {'message': 'User not found'}, 404  # Se não encontrado, retorna erro

    @jwt_required()  # Requer autenticação JWT para o DELETE
    def delete(self, user_id):
        # Exclui um usuário pelo ID
        user = UsuarioModel.find_user(user_id)
        if user:
            try:
                user.delete_user()  # Tenta deletar o usuário
            except:
                return {'message': 'Erro interno ao tentar deletar dados do banco'}, 500  # Erro no banco
            return {'message': f"user {user.json().get('login')} deleted"}  # Sucesso
        return {'message': 'User not found.'}, 404  # Usuário não encontrado


# Classe para registrar um novo usuário
class UserRegister(Resource):
    def post(self):
        # Recebe os dados do POST
        dados = atributos.parse_args()
        
        # Verifica se o login já existe
        if UsuarioModel.find_by_login(dados['login']):
            return {'message': f"The login {dados['login']} already exists."}, 400  # Erro se login já existir

        # Cria e salva o novo usuário
        user = UsuarioModel(**dados)
        user.ativado = False
        user.save_user()
        return {'message': 'User created successfully!'}, 201  # Usuário criado com sucesso


# Classe para realizar o login do usuário
class UserLogin(Resource):
    @classmethod
    def post(cls):
        # Recebe os dados do POST (login e senha)
        dados = atributos.parse_args()
        
        # Verifica se o usuário existe e se a senha está correta
        user = UsuarioModel.find_by_login(dados['login'])
        if user and hmac.compare_digest(user.senha, dados['senha']):
            if not user.ativado:  # Verifica se o usuário não está ativado
                return {'message': 'User not confirmed.'}, 400
            
            # Cria o token de acesso JWT se as credenciais forem válidas e o usuário estiver ativado
            token_de_acesso = create_access_token(identity=str(user.user_id))
            return {'access_token': token_de_acesso}, 200  # Retorna o token
        
        # Retorna erro se login ou senha estiverem incorretos
        return {'message': 'The username or password is incorrect'}, 401


# Classe para realizar o logout do usuário
class UserLogout(Resource):
    @jwt_required()  # Requer autenticação JWT para o POST
    def post(self):
        # Adiciona o token JWT à lista negra para invalidar
        jwt_id = get_jwt()['jti']  # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200  # Sucesso no logout

class UserConfirm(Resource):
    #raiz_do_site/confirmacao/{user_id}
    @classmethod
    def get(cls, user_id):
        user = UsuarioModel.find_user(user_id)

        if not user:
            return {'message': f'User id {user_id} não ativado.'}, 404

        user.ativado = True
        user.save_user()
        return {'message': f'User id {user_id} confirmed sucessfully.'}, 200
