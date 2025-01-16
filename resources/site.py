from flask_restful import Resource
from models.site import SiteModel

# Classe para manipulação dos sites (GET, POST, DELETE)
class Sites(Resource):
    def get(self):
        # Retorna todos os sites registrados no banco
        return {'sites': [site.json() for site in SiteModel.query.all()]}

class Site(Resource):
    def get(self, url):
        # Procura um site pelo URL e retorna seus dados ou mensagem de erro
        site = SiteModel.find_site(url)
        if site:
            return site.json()
        return {'message': f'Site {url} not found'}, 404  # Caso não encontrado

    def post(self, url):
        # Cria um novo site se ele não existir
        if SiteModel.find_site(url):
            return {'message': 'The site already exists'}, 400  # Caso o site já exista
        site = SiteModel(url)
        try:
            site.save_site()  # Tenta salvar o site
        except:
            return {'message': 'Internal error occurred while creating the site'}, 500  # Erro no servidor
        return site.json()  # Retorna o site criado

    def delete(self, url):
        # Exclui o site baseado no URL
        site = SiteModel.find_site(url)
        if site:
            site.delete_site()  # Exclui o site do banco
            return {'message': f'Site {site.url} deleted successfully'}
        return {'message': 'Site not found'}, 404  # Caso o site não seja encontrado
