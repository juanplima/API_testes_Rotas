from flask import Blueprint, request, jsonify
from extensions import db
from models import *

routes = Blueprint('routes', __name__)

def register_routes(app, db):
    app.register_blueprint(routes)

def generic_crud(model):
    model_name = model.__tablename__

    @routes.route(f"/{model_name}", methods=["GET"])
    def get_all(model=model):
        records = model.query.all()
        return jsonify([r.to_dict() for r in records])
    get_all.__name__ = f"get_all_{model_name}"

    @routes.route(f"/{model_name}/<int:id>", methods=["GET"])
    def get_one(id, model=model):
        record = model.query.get_or_404(id)
        return jsonify(record.to_dict())
    get_one.__name__ = f"get_one_{model_name}"

    @routes.route(f"/{model_name}", methods=["POST"])
    def create(model=model):
        data = request.json
        record = model(**data)
        db.session.add(record)
        db.session.commit()
        return jsonify(record.to_dict()), 201
    create.__name__ = f"create_{model_name}"

    @routes.route(f"/{model_name}/<int:id>", methods=["PUT"])
    def update(id, model=model):
        data = request.json
        record = model.query.get_or_404(id)
        for key, value in data.items():
            setattr(record, key, value)
        db.session.commit()
        return jsonify(record.to_dict())
    update.__name__ = f"update_{model_name}"

    @routes.route(f"/{model_name}/<int:id>", methods=["DELETE"])
    def delete(id, model=model):
        record = model.query.get_or_404(id)
        db.session.delete(record)
        db.session.commit()
        return '', 204
    delete.__name__ = f"delete_{model_name}"

# Registra todas as rotas CRUD para os modelos
models_list = [
    Estado, Cidade, Bairro, CEP, Tipo_Endereco, Endereco, Academia,
    Tipo_Telefone, Pessoa, Telefone, Usuario, Cargo, Empregado, Dieta,
    Treino, Tipo_Pagamento, Plano, Tipo_Plano, Aluno, Menu_Principal,
    Comunidade, Feedbacks, Tipo_Feedbacks
]

for m in models_list:
    generic_crud(m)

# ROTA GET
@routes.route("/menu_inicial/<int:id_aluno>", methods=["GET"])
def menu_inicial(id_aluno):
    aluno = Aluno.query.get_or_404(id_aluno)

    usuario = Usuario.query.get(aluno.FK_Usuario_ID)
    plano = Plano.query.get(aluno.FK_Planos_ID)
    tipo_plano = Tipo_Plano.query.get(plano.FK_TipoPlano_ID) if plano else None
    pessoa = Pessoa.query.get(usuario.FK_Pessoa_ID) if usuario else None

    return jsonify({
        "Aluno": {
            "ID": aluno.Matricula,
        },
        "Usuario": {
            "ID": usuario.ID_Usuario if usuario else None,
            "Login": usuario.Login if usuario else None,
        },
        "Pessoa": {
            "Nome": pessoa.Nome if pessoa else None,
            "Email": pessoa.Email if pessoa else None,
        },
        "Plano": {
            "ID": plano.ID_Planos if plano else None,
            "Nome": tipo_plano.Nome if tipo_plano else None,
        }
    })

# ROTA POST
@routes.route("/menu_inicial", methods=["POST"])
def create_menu_inicial():
    data = request.json

    pessoa_data = data.get("Pessoa")
    pessoa = Pessoa(**pessoa_data)
    db.session.add(pessoa)
    db.session.flush()  

    
    usuario_data = data.get("Usuario")
    usuario = Usuario(**usuario_data, FK_Pessoa_ID=pessoa.CPF)
    db.session.add(usuario)
    db.session.flush()

    
    aluno_data = data.get("Aluno")
    aluno = Aluno(**aluno_data, FK_Usuario_ID=usuario.ID_Usuario)
    db.session.add(aluno)

    db.session.commit()

    return jsonify({
        "Aluno": aluno.to_dict(),
        "Usuario": usuario.to_dict(),
        "Pessoa": pessoa.to_dict()
    }), 201

