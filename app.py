from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Inicializa o Flask
app = Flask(__name__)

# Configura o banco de dados
<<<<<<< HEAD
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://u794777727_BlackBrothers:blackjP157@srv1526.hstgr.io:3306/u794777727_BlackBrotherBD'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa os objetos do SQLAlchemy e Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Importar as rotas depois da inicialização do app, db e ma
from routes import *

# Roda o app
if __name__ == '__main__':
    app.run(debug=True)
=======
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://u794777727_BlackBrothers1:senhanovaBD157@193.203.175.99/u794777727_BlackBrotherBD'
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True
}


db = SQLAlchemy()
ma = Marshmallow()


from models import *

# Agora inicializa db e ma com o app
db.init_app(app)
ma.init_app(app)


from routes import *

# Criar as tabelas no banco de dados
with app.app_context():
    db.create_all()

# Roda o app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

>>>>>>> 830632856cfb4e2b6e8e8faa463b178a19115496
