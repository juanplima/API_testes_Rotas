from flask import Blueprint, app, current_app, request, jsonify, send_from_directory
from extensions import db
from models import *
from flask_jwt_extended import create_access_token, jwt_required
from sqlalchemy.exc import IntegrityError
import os
import mercadopago

routes = Blueprint('routes', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

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

            if isinstance(data, list):
                records = [TreinoExercicio(**item) for item in data]
                db.session.add_all(records)
                db.session.commit()
                return jsonify([r.to_dict() for r in records]), 201
        
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

        except IntegrityError as e:
            db.session.rollback()

            if "foreign key constraint fails" in str(e).lower():
                print(f"[AVISO] Não foi possível deletar {model_name} {id}: registro referenciado em outra tabela.")
                return jsonify({
                    "error": "Nao e possivel excluir este registro, pois ele esta sendo utilizado em outro local."
                }), 400
            
            # Outro erro de integridade (não relacionado a FK)
            print(f"[AVISO] Erro de integridade ao deletar {model_name} {id}: {e}")
            return jsonify({
                "error": "Erro de integridade nos dados."
            }), 400

        except Exception as e:
            db.session.rollback()
            print(f"[ERRO] Erro interno ao deletar {model_name} {id}: {e}")
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
    print(">>> ENTROU NA ROTA DE LOGIN ADMIN <<<")
    
    data = request.json
    login = data.get("login")
    senha = data.get("senha")

    print(f"Login recebido: {login}, Senha recebida: {senha}")

    if not login or not senha:
        return jsonify({"error": "Campos 'login' e 'senha' são obrigatórios"}), 400

    usuario = Usuario.query.filter_by(Login=login, Senha=senha).first()
    if not usuario:
        return jsonify({"error": "Usuário ou senha inválidos"}), 404

    pessoa = Pessoa.query.filter_by(CPF=usuario.FK_Pessoa_ID).first()
    
    if not pessoa:
        nome_usuario = usuario.Login 
        email_usuario = "Não informado"
    else:
        nome_usuario = pessoa.Nome
        email_usuario = pessoa.Email

    access_token = create_access_token(identity=str(usuario.ID_Usuario))
    
    return jsonify({
        "usuario": {
            "ID_Usuario": usuario.ID_Usuario,
            "Login": usuario.Login,
            "Nome": nome_usuario,
            "Email": email_usuario
        },
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

@routes.route("/Tipo_Plano/register", methods=["GET"])
def get_all_Tipo_Plano_register():
    try:
        query_params = request.args.to_dict()
        query = Tipo_Plano.query  # Sempre usando Tipo_Plano diretamente

        # Aplica filtros se houver query params
        for key, value in query_params.items():
            column = getattr(Tipo_Plano, key, None)
            if column is not None:
                query = query.filter(column == value)

        records = query.all()
        return jsonify([r.to_dict() for r in records])
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Erro interno: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

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
    # ... (código existente)
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
    # ... (código existente)
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
        usuario_data['Data_Nascimento'] = pessoa.DtNasc
        lista_de_usuarios.append(usuario_data)
    return jsonify(lista_de_usuarios)

@routes.route("/treinos/detalhes", methods=["GET"])
@jwt_required()
def get_treinos_com_detalhes():
    # ... (código existente)
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
    # ... (código existente)
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
    # ... (código existente)
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
    # ... (código existente)
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
    # ... (código existente)
    sdk = get_mp_sdk()
    data = request.json
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
            "payment_methods": {},
            "notification_url": data.get("notification_url")
        }
        preference_response = sdk.preference().create(preference_data)
        return jsonify(preference_response["response"]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route("/webhook", methods=["POST"])
def webhook():
    # ... (código existente)
    body = request.json
    print("Webhook MP:", body)
    return jsonify({"status": "received"}), 200

@routes.route('/Upload', methods=['POST'])
def upload_file():
    # ... (código existente)
    if 'imagem' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    file = request.files['imagem']
    if file and allowed_file(file.filename):
        filename = file.filename
        upload_folder = current_app.config['UPLOAD_FOLDER'] 
        os.makedirs(upload_folder, exist_ok=True)
        path = os.path.join(upload_folder, filename)
        file.save(path)
        image_url = f"/uploads/{filename}"
        return jsonify({'ImagemURL': image_url}), 200
    return jsonify({'error': 'Arquivo inválido'}), 400

@routes.route('/uploads/<path:filename>')
def get_uploaded_file(filename):
    # ... (código existente)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(upload_folder, filename)

# Registra todas as rotas CRUD para os modelos
models_list = [
    Estado, Cidade, Bairro, CEP, Tipo_Endereco, Endereco, Academia,
    Tipo_Telefone, Pessoa, Telefone, Usuario, Cargo, Empregado, Dieta,
    Treino, Exercicio, TreinoExercicio, Tipo_Pagamento, Plano, Tipo_Plano, Aluno,
    Comunidade, Feedbacks, Tipo_Feedbacks, Frequencia, Videos, Eventos, ContasAReceber, ContasAPagar, Categoria
]

for m in models_list:
    generic_crud(m)