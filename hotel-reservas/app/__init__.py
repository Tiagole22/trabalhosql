# Executar

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app(config_name=None):
    """Factory para criar a aplicação Flask"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Importar configuração
    from config import config
    app.config.from_object(config[config_name])
    
    # Inicializar banco de dados
    db.init_app(app)
    
    # Registrar blueprints
    from app.routes import hospedes_bp, quartos_bp, reservas_bp, main_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(hospedes_bp, url_prefix='/hospedes')
    app.register_blueprint(quartos_bp, url_prefix='/quartos')
    app.register_blueprint(reservas_bp, url_prefix='/reservas')
    
    # Criar tabelas
    with app.app_context():
        db.create_all()
    
    return app
