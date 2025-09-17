from flask import Blueprint, request, jsonify
from extensions import db
from models import *
from flask_jwt_extended import create_access_token, jwt_required

routes = Blueprint('routes', __name__)

def register_routes(app, db):
    app.register_blueprint(routes)

def generic_crud(model):
    model_name = model.__tablename__

    @routes.route(f"/{model_name}", methods=["GET"])
    @jwt_required()
    def get_all(model=model):
        query_params = request.args.to_dict()

        if query_params:
            query = model.query
            for key, value in query_params.items():
                column = getattr(model, key, None)
                if column is not None:
                    query = query.filter(column == value)
            records = query.all()
        else:
            records = model.query.all()
        return jsonify([r.to_dict() for r in records])
    get_all.__name__ = f"get_all_{model_name}"

    @routes.route(f"/{model_name}/<int:id>", methods=["GET"])
    @jwt_required()
    def get_one(id, model=model):
        record = model.query.get_or_404(id)
        return jsonify(record.to_dict())
    get_one.__name__ = f"get_one_{model_name}"

    @routes.route(f"/{model_name}", methods=["POST"])
    @jwt_required()
    def create(model=model):
        data = request.json
        record = model(**data)
        db.session.add(record)
        db.session.commit()
        return jsonify(record.to_dict()), 201
    create.__name__ = f"create_{model_name}"

    @routes.route(f"/{model_name}/<int:id>", methods=["PUT"])
    @jwt_required()
    def update(id, model=model):
        data = request.json
        record = model.query.get_or_404(id)
        for key, value in data.items():
            setattr(record, key, value)
        db.session.commit()
        return jsonify(record.to_dict())
    update.__name__ = f"update_{model_name}"

    @routes.route(f"/{model_name}/<int:id>", methods=["DELETE"])
    @jwt_required()
    def delete(id, model=model):
        record = model.query.get_or_404(id)
        db.session.delete(record)
        db.session.commit()
        return '', 204
    delete.__name__ = f"delete_{model_name}"

@routes.route("/Usuario/login", methods=["POST"])
def login_usuario():
    print(">>> ENTROU NA ROTA DE LOGIN <<<")
    
    data = request.json
    login = data.get("login")
    senha = data.get("senha")

    print(f"Login recebido: {login}, Senha recebida: {senha}")

    if not login or not senha:
        return jsonify({"error": "Campos 'login' e 'senha' são obrigatórios"}), 400

    # Verifica se usuário existe
    usuario = Usuario.query.filter_by(Login=login, Senha=senha).first()
    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404

    # Verifica se é aluno
    aluno = Aluno.query.filter_by(FK_Usuario_ID=usuario.ID_Usuario).first()
    if not aluno:
        return jsonify({"error": "Usuário não é aluno"}), 403

    # Cria token JWT
    access_token = create_access_token(identity=str(usuario.ID_Usuario))
    return jsonify({
        "usuario": usuario.to_dict(),
        "token": access_token
    }), 200


# Registra todas as rotas CRUD para os modelos
models_list = [
    Estado, Cidade, Bairro, CEP, Tipo_Endereco, Endereco, Academia,
    Tipo_Telefone, Pessoa, Telefone, Usuario, Cargo, Empregado, Dieta,
    Treino, Tipo_Pagamento, Plano, Tipo_Plano, Aluno, Menu_Principal,
    Comunidade, Feedbacks, Tipo_Feedbacks
]

for m in models_list:
    generic_crud(m)
