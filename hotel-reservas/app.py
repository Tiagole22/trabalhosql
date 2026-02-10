# Responsável por iniciar o servidor Flask. Ele importa a aplicação 

#!/usr/bin/env python3
import sys
import os

# Adicionar o diretório do projeto ao sys.path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app import create_app
    
    if __name__ == '__main__':
        app = create_app()
        
        # Configurações de desenvolvimento
        debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
        port = int(os.getenv('FLASK_PORT', 5000))
        host = os.getenv('FLASK_HOST', '127.0.0.1')
        
        print(f"\n🏨 Servidor Flask iniciando...")
        print(f"📍 URL: http://{host}:{port}")
        print(f"🔧 Debug: {debug}\n")
        
        app.run(
            host=host,
            port=port,
            debug=debug
        )
except ImportError as e:
    print(f"❌ Erro ao importar: {e}")
    print("\n📦 Instale as dependências com:")
    print("   pip3 install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro: {e}")
    sys.exit(1)
