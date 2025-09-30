from flask import Blueprint, app, request, jsonify
from extensions import db
from models import *
from flask_jwt_extended import create_access_token, jwt_required
import os
import mercadopago

routes = Blueprint('routes', __name__)

def get_mp_sdk():
    token = os.getenv("MP_ACCESS_TOKEN")
    if not token:
        raise ValueError("MP_ACCESS_TOKEN não definido!")
    return mercadopago.SDK(token.strip())

def get_secret():
    secret = os.getenv("REGISTRATION_SECRET")
    if not secret:
        raise RuntimeError("REGISTRATION_SECRET não definido! Verifique o .env")
    return secret

def register_routes(app, db):
    app.register_blueprint(routes)

def generic_crud(model):
    model_name = model.__tablename__

    @routes.route(f"/{model_name}", methods=["GET"])
    @jwt_required()
    def get_all(model=model):
        try:
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
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Erro interno: {e}")
            return jsonify({"error": "Erro interno do servidor"}), 500
    get_all.__name__ = f"get_all_{model_name}"

    @routes.route(f"/{model_name}/<int:id>", methods=["GET"])
    @jwt_required()
    def get_one(id, model=model):
        try:
            record = model.query.get_or_404(id)
            return jsonify(record.to_dict())
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Erro interno: {e}")
            return jsonify({"error": "Erro interno do servidor"}), 500
    get_one.__name__ = f"get_one_{model_name}"

    @routes.route(f"/{model_name}", methods=["POST"])
    @jwt_required()
    def create(model=model):
        try:
            data = request.json
            record = model(**data)
            db.session.add(record)
            db.session.commit()
            return jsonify(record.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Erro interno: {e}")
            return jsonify({"error": "Erro interno do servidor"}), 500
    create.__name__ = f"create_{model_name}"

    @routes.route(f"/{model_name}/<int:id>", methods=["PUT"])
    @jwt_required()
    def update(id, model=model):
        try:
            data = request.json
            record = model.query.get_or_404(id)
            for key, value in data.items():
                setattr(record, key, value)
            db.session.commit()
            return jsonify(record.to_dict())
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Erro interno: {e}")
            return jsonify({"error": "Erro interno do servidor"}), 500
    update.__name__ = f"update_{model_name}"

    @routes.route(f"/{model_name}/<int:id>", methods=["DELETE"])
    @jwt_required()
    def delete(id, model=model):
        try:
            record = model.query.get_or_404(id)
            db.session.delete(record)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Erro interno: {e}")
            return jsonify({"error": "Erro interno do servidor"}), 500
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

@routes.route("/Admin/login", methods=["POST"])
def login_admin():
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

    # Cria token JWT
    access_token = create_access_token(identity=str(usuario.ID_Usuario))
    return jsonify({
        "usuario": usuario.to_dict(),
        "token": access_token
    }), 200


# ================================ CADASTROS INICIAIS ==========================================
@routes.route("/Usuario/register", methods=["POST"])
def register_usuario():
    client_code = request.headers.get("X-Registration-Secret")
    if client_code != get_secret():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    novo_usuario = Usuario(**data)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify(novo_usuario.to_dict()), 201

@routes.route("/Telefone/register", methods=["POST"])
def register_telefone():
    client_code = request.headers.get("X-Registration-Secret")
    if client_code != get_secret():
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    novo_telefone = Telefone(**data)
    db.session.add(novo_telefone)
    db.session.commit()
    return jsonify(novo_telefone.to_dict()), 201

@routes.route("/Plano/register", methods=["POST"])
def register_plano():
    client_code = request.headers.get("X-Registration-Secret")
    if client_code != get_secret():
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    novo_plano = Plano(**data)
    db.session.add(novo_plano)
    db.session.commit()
    return jsonify(novo_plano.to_dict()), 201

@routes.route("/Pessoa/register", methods=["POST"])
def register_pessoa():
    client_code = request.headers.get("X-Registration-Secret")
    if client_code != get_secret():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    nova_pessoa = Pessoa(**data)
    db.session.add(nova_pessoa)
    db.session.commit()
    return jsonify(nova_pessoa.to_dict()), 201


# =============================== ADMIN ROUTES ==========================================
@routes.route("/alunos/detalhes", methods=["GET"])
@jwt_required()
def get_alunos_com_detalhes():
    resultados = db.session.query(
        Aluno, Pessoa, Tipo_Plano
    ).join(
        Usuario, Aluno.FK_Usuario_ID == Usuario.ID_Usuario
    ).join(
        Pessoa, Usuario.FK_Pessoa_ID == Pessoa.CPF
    ).join(
        Plano, Aluno.FK_Planos_ID == Plano.ID_Planos
    ).join(
        Tipo_Plano, Plano.FK_TipoPlano_ID == Tipo_Plano.ID_TipoPlanos
    ).all()
    lista_de_alunos = []
    for aluno, pessoa, tipo_plano in resultados:
        aluno_data = aluno.to_dict()
        aluno_data['Nome'] = pessoa.Nome 
        aluno_data['Email'] = pessoa.Email
        aluno_data['CPF'] = pessoa.CPF
        aluno_data['Nome_Plano'] = tipo_plano.Nome
        aluno_data['Preco_Plano'] = float(tipo_plano.Preco)
        lista_de_alunos.append(aluno_data)
    return jsonify(lista_de_alunos)

@routes.route("/usuarios/detalhes", methods=["GET"])
@jwt_required()
def get_usuarios_com_detalhes():
    resultados = db.session.query(
        Usuario, 
        Pessoa
    ).join(
        Pessoa, Usuario.FK_Pessoa_ID == Pessoa.CPF
    ).all()

    lista_de_usuarios = []
    for usuario, pessoa in resultados:
        usuario_data = usuario.to_dict()
        usuario_data['Nome'] = pessoa.Nome
        usuario_data['Email'] = pessoa.Email
        usuario_data['CPF'] = pessoa.CPF
        lista_de_usuarios.append(usuario_data)
    return jsonify(lista_de_usuarios)

@routes.route("/treinos/detalhes", methods=["GET"])
@jwt_required()
def get_treinos_com_detalhes():
    resultados = db.session.query(Treino, Pessoa).join(Empregado, Treino.FK_Empregado_ID == Empregado.ID_Empregado).join(Usuario, Empregado.FK_Usuario_ID == Usuario.ID_Usuario).join(Pessoa, Usuario.FK_Pessoa_ID == Pessoa.CPF).all()
    lista_de_treinos = []
    for treino, pessoa in resultados:
        treino_data = treino.to_dict()
        treino_data['Nome_Instrutor'] = pessoa.Nome 
        lista_de_treinos.append(treino_data)
    return jsonify(lista_de_treinos)

@routes.route("/empregados/detalhes", methods=["GET"])
@jwt_required()
def get_empregados_com_detalhes():
    resultados = db.session.query(Empregado, Pessoa).join(Usuario, Empregado.FK_Usuario_ID == Usuario.ID_Usuario).join(Pessoa, Usuario.FK_Pessoa_ID == Pessoa.CPF).all()
    lista_de_empregados = []
    for empregado, pessoa in resultados:
        empregado_data = empregado.to_dict()
        empregado_data['Nome'] = pessoa.Nome
        lista_de_empregados.append(empregado_data)
    return jsonify(lista_de_empregados)
    
@routes.route("/usuarios/nao-alunos", methods=["GET"])
@jwt_required()
def get_usuarios_nao_alunos():
    try:
        subquery = db.session.query(Aluno.FK_Usuario_ID).subquery()
        resultados = db.session.query(Usuario, Pessoa).join(Pessoa, Usuario.FK_Pessoa_ID == Pessoa.CPF).filter(Usuario.ID_Usuario.notin_(subquery)).all()
        lista_de_usuarios = [{"ID_Usuario": usuario.ID_Usuario, "Nome": pessoa.Nome, "Email": pessoa.Email, "Login": usuario.Login} for usuario, pessoa in resultados]
        return jsonify(lista_de_usuarios)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route("/usuarios/nao-funcionarios", methods=["GET"])
@jwt_required()
def get_usuarios_nao_funcionarios():
    try:
        subquery = db.session.query(Empregado.FK_Usuario_ID).subquery()
        resultados = db.session.query(Usuario, Pessoa).join(Pessoa, Usuario.FK_Pessoa_ID == Pessoa.CPF).filter(Usuario.ID_Usuario.notin_(subquery)).all()
        lista_de_usuarios = [{"ID_Usuario": usuario.ID_Usuario, "Nome": pessoa.Nome, "Email": pessoa.Email, "Login": usuario.Login} for usuario, pessoa in resultados]
        return jsonify(lista_de_usuarios)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# =============================== PAYMENT API ==========================================
@routes.route("/create_preference", methods=["POST"])
def create_preference():
    sdk = get_mp_sdk()
    data = request.json
    # espera que data contenha, por exemplo:
    #   items: lista de dicts com title, quantity, unit_price, etc
    #   payer: opcional
    try:
        preference_data = {
            "items": data.get("items", []),
            "payer": data.get("payer", {}),
            "back_urls": {
                "success": data.get("back_urls", {}).get("success"),
                "failure": data.get("back_urls", {}).get("failure"),
                "pending": data.get("back_urls", {}).get("pending"),
            },
            "auto_return": "approved",
            "payment_methods": {
                # opcional: limitar ou excluir meios
                # ex: "excluded_payment_methods": [{ "id": "visa" }],
                # "excluded_payment_types": ...
            },
            "notification_url": data.get("notification_url")
        }
        preference_response = sdk.preference().create(preference_data)
        # preference_response["response"] tem os dados
        return jsonify(preference_response["response"]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route("/webhook", methods=["POST"])
def webhook():
    # receber notificações do Mercado Pago.
    body = request.json
    print("Webhook MP:", body)
    return jsonify({"status": "received"}), 200

# Registra todas as rotas CRUD para os modelos
models_list = [
    Estado, Cidade, Bairro, CEP, Tipo_Endereco, Endereco, Academia,
    Tipo_Telefone, Pessoa, Telefone, Usuario, Cargo, Empregado, Dieta,
    Treino, Exercicio, TreinoExercicio, Tipo_Pagamento, Plano, Tipo_Plano, Aluno,
    Comunidade, Feedbacks, Tipo_Feedbacks, Frequencia, Videos
]

for m in models_list:
    generic_crud(m)
