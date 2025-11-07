import os
from flask import Flask
from flask_cors import CORS
from extensions import db 
from routes import register_routes
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', 'png,jpg,jpeg,jfif')

# Cria pasta se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
CORS(app)

# Upload das imagens
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = set(ALLOWED_EXTENSIONS.split(','))

# Configurações do seu banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://u794777727_BlackBrothers1:senhanovaBD157@193.203.175.99/u794777727_BlackBrotherBD'
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True
}

# Configuração do JWT.
app.config['JWT_SECRET_KEY'] = "blackbrothers_top_2025_app_seguro_9x82!@#"

# Inicializando o SQLAlchemy com a aplicação Flask
db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Registrando as rotas
register_routes(app, db)

print("\n🔍 Rotas registradas:")
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint:30s} | {','.join(rule.methods):20s} | {rule.rule}")
print("\n")

@app.route('/')
def index():
    
    return "🚀 API Black Brothers está rodando com sucesso!"

    
with app.app_context():
    db.create_all()

# Inicia o servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
