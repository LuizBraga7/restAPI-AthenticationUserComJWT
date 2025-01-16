from sql_alchemy import banco  # Importa a instância do banco de dados.

class HotelModel(banco.Model):
    """
    Representa um modelo para a tabela 'hoteis' no banco de dados.
    """

    # Define o nome da tabela.
    __tablename__ = 'hoteis'

    # Define as colunas da tabela.
    hotel_id = banco.Column(banco.String, primary_key=True)  # ID único do hotel.
    nome = banco.Column(banco.String(80))  # Nome do hotel.
    estrelas = banco.Column(banco.Float(precision=1))  # Classificação do hotel (0 a 5 estrelas).
    diaria = banco.Column(banco.Float(precision=2))  # Valor da diária.
    cidade = banco.Column(banco.String(40))  # Cidade onde o hotel está localizado.
    site_id = banco.Column(banco.Integer, banco.ForeignKey('sites.site_id'))  # ID do site associado.

    def __init__(self, hotel_id, nome, estrelas, diaria, cidade, site_id):
        """
        Inicializa os atributos do hotel.
        """
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.site_id = site_id

    def json(self):
        """
        Retorna os dados do hotel no formato JSON.
        """
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade,
            'site_id': self.site_id
        }
    
    @classmethod
    def find_hotel(cls, hotel_id):
        """
        Busca um hotel pelo ID.
        """
        return cls.query.filter_by(hotel_id=hotel_id).first()
    
    def save_hotel(self):
        """
        Salva o hotel no banco de dados.
        """
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, nome, estrelas, diaria, cidade):
        """
        Atualiza os dados do hotel.
        """
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
    
    def delete_hotel(self):
        """
        Remove o hotel do banco de dados.
        """
        banco.session.delete(self)
        banco.session.commit()
