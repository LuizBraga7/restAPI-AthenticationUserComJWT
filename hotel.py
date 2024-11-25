from flask_restful import Resource, reqparse  # Classes base para criar APIs RESTful.
from models.hotel import HotelModel          # Modelo do hotel no banco de dados.
from resources.filtros import (             # Filtros para consultas personalizadas.
    normalize_path_params,
    consulta_sem_cidade,
    consulta_com_cidade
)
from models.site import SiteModel           # Modelo do site no banco de dados.
from flask_jwt_extended import jwt_required # Controle de autenticação JWT.
import sqlite3                              # Para interagir diretamente com o banco SQLite.

# Define parâmetros aceitos na URL para filtros.
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str, location='args')
path_params.add_argument('estrelas_min', type=float, location='args')
path_params.add_argument('estrelas_max', type=float, location='args')
path_params.add_argument('diaria_min', type=float, location='args')
path_params.add_argument('diaria_max', type=float, location='args')
path_params.add_argument('limit', type=float, location='args')
path_params.add_argument('offset', type=float, location='args')

# Classe para manipular a lista de todos os hotéis.
class Hoteis(Resource):
    def get(self):
        # conectando no banco
        caminho_banco = r'C:\Users\lfsoares\OneDrive - Sistema FIEMG\Área de Trabalho\LUIZ\8.Cursos\2.REST_APIs_Flask\app\banco.db'
        connection = sqlite3.connect(caminho_banco)
        cursor = connection.cursor()

        # Processa os filtros fornecidos.
        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        # Executa a consulta com ou sem cidade.
        consulta = consulta_sem_cidade if not parametros.get('cidade') else consulta_com_cidade
        tupla = tuple([parametros[chave] for chave in parametros])
        resultado = cursor.execute(consulta, tupla)

        # Organiza os resultados.
        hoteis = [
            {
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4],
                'site_id': linha[5]
            } for linha in resultado
        ]

        connection.close()
        return {'hoteis': hoteis}, 200

# Recurso para manipular dados de um hotel específico.
class Hotel(Resource):
    # Define os argumentos necessários para criar ou atualizar um hotel.
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="O campo 'nome' é obrigatório.")
    argumentos.add_argument('estrelas', type=float, required=True, help="O campo 'estrelas' é obrigatório.")
    argumentos.add_argument('diaria', type=float, required=True, help="O campo 'diaria' é obrigatório.")
    argumentos.add_argument('cidade', type=str, required=True, help="O campo 'cidade' é obrigatório.")
    argumentos.add_argument('site_id', type=int, required=True, help="O campo 'site_id' é obrigatório.")

    @staticmethod
    def find_hotel(hotel_id):
        """Busca um hotel pelo ID no banco de dados."""
        return HotelModel.query.filter_by(hotel_id=hotel_id).first()

    def get(self, hotel_id):
        """Retorna os dados de um hotel específico pelo ID."""
        hotel = self.find_hotel(hotel_id)
        if hotel:
            return hotel.json(), 200
        return {'message': 'Hotel não encontrado.'}, 404

    @jwt_required()
    def post(self, hotel_id):
        """Adiciona um novo hotel."""
        if self.find_hotel(hotel_id):
            return {'message': f"Hotel com id '{hotel_id}' já existe."}, 400

        dados = Hotel.argumentos.parse_args()
        if not SiteModel.find_by_id(dados.get('site_id')):
            return {'message': 'O hotel deve estar associado a um site válido.'}, 400

        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
            return hotel.json(), 201
        except Exception as e:
            return {'message': f'Erro ao salvar o hotel: {str(e)}'}, 500

    @jwt_required()
    def put(self, hotel_id):
        """Atualiza os dados de um hotel ou cria um novo caso não exista."""
        dados = Hotel.argumentos.parse_args()
        hotel = self.find_hotel(hotel_id)

        if hotel:
            try:
                hotel.update_hotel(**dados)
                hotel.save_hotel()
                return hotel.json(), 200
            except Exception as e:
                return {'message': f'Erro ao atualizar o hotel: {str(e)}'}, 500
        else:
            hotel = HotelModel(hotel_id, **dados)
            try:
                hotel.save_hotel()
                return hotel.json(), 201
            except Exception as e:
                return {'message': f'Erro ao criar o hotel: {str(e)}'}, 500

    @jwt_required()
    def delete(self, hotel_id):
        """Remove um hotel pelo ID."""
        hotel = self.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
                return {'message': f"Hotel '{hotel.nome}' deletado com sucesso."}, 200
            except Exception as e:
                return {'message': f'Erro ao deletar o hotel: {str(e)}'}, 500
        return {'message': 'Hotel não encontrado.'}, 404