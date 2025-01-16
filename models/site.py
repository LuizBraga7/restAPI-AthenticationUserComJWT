from sql_alchemy import banco  # Importa a instância do banco de dados.

class SiteModel(banco.Model):
    """
    Representa um modelo para a tabela 'sites' no banco de dados.
    """

    # Define o nome da tabela.
    __tablename__ = 'sites'

    # Define as colunas da tabela.
    site_id = banco.Column(banco.Integer, primary_key=True)  # ID único do site.
    url = banco.Column(banco.String(80))  # URL do site.
    hoteis = banco.relationship('HotelModel')  # Relacionamento com os hotéis.

    def __init__(self, url):
        """
        Inicializa os atributos do site.
        """
        self.url = url

    def json(self):
        """
        Retorna os dados do site no formato JSON, incluindo os hotéis relacionados.
        """
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hoteis': [hotel.json() for hotel in self.hoteis]  # Lista de hotéis do site.
        }
    
    @classmethod
    def find_site(cls, url):
        """
        Busca um site pelo URL.
        """
        return cls.query.filter_by(url=url).first()
    
    @classmethod
    def find_by_id(cls, site_id):
        """
        Busca um site pelo ID.
        """
        return cls.query.filter_by(site_id=site_id).first()

    def save_site(self):
        """
        Salva o site no banco de dados.
        """
        banco.session.add(self)
        banco.session.commit()
    
    def delete_site(self):
        """
        Remove o site e todos os hotéis associados do banco de dados.
        """
        # Remove os hotéis relacionados ao site.
        [hotel.delete_hotel() for hotel in self.hoteis]
        # Remove o site.
        banco.session.delete(self)
        banco.session.commit()
