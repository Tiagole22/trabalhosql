from app import db
from datetime import datetime
from decimal import Decimal

class Hospede(db.Model):
    """Modelo para Hóspedes"""
    __tablename__ = 'hospedes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento
    reservas = db.relationship('Reserva', backref='hospede', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Hospede {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'email': self.email
        }

class Quarto(db.Model):
    """Modelo para Quartos"""
    __tablename__ = 'quartos'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False, unique=True)
    tipo = db.Column(db.String(50), nullable=False)  # Solteiro, Casal, Suite, etc
    preco = db.Column(db.Numeric(10, 2), nullable=False)  # Preço da diária
    status = db.Column(db.String(20), default='LIVRE')  # LIVRE, OCUPADO
    descricao = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento
    reservas = db.relationship('Reserva', backref='quarto', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Quarto {self.numero}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'tipo': self.tipo,
            'preco': float(self.preco),
            'status': self.status,
            'descricao': self.descricao
        }

class Reserva(db.Model):
    """Modelo para Reservas"""
    __tablename__ = 'reservas'
    
    id = db.Column(db.Integer, primary_key=True)
    id_hospede = db.Column(db.Integer, db.ForeignKey('hospedes.id'), nullable=False)
    id_quarto = db.Column(db.Integer, db.ForeignKey('quartos.id'), nullable=False)
    entrada = db.Column(db.Date, nullable=False)
    saida = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(20), default='ATIVA')  # ATIVA, CANCELADA, FINALIZADA
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Reserva {self.id}>'
    
    def calcular_total(self):
        """Calcula o total da reserva baseado nos dias e preço do quarto"""
        dias = (self.saida - self.entrada).days
        return float(self.quarto.preco) * dias
    
    def get_dias(self):
        """Retorna a quantidade de dias da reserva"""
        return (self.saida - self.entrada).days
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_hospede': self.id_hospede,
            'id_quarto': self.id_quarto,
            'entrada': self.entrada.isoformat(),
            'saida': self.saida.isoformat(),
            'total': float(self.total) if self.total else self.calcular_total(),
            'status': self.status,
            'dias': self.get_dias()
        }
