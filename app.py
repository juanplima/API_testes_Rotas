from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://u794777727_BlackBrothers1:senhaTopBD157A$@srv1526.hstgr.io:3306/u794777727_BlackBrotherBD'
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Criação do db sem associar diretamente ao app
db = SQLAlchemy()

# Inicialização do db com o app
db.init_app(app)

class MyModelSchema(Schema):
    id = fields.Int()
    name = fields.Str()

# Importação de modelos
from models import *  

# Inicialização do banco de dados dentro do contexto do app
with app.app_context():
    db.create_all()

# Importação das rotas
from routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
