from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Estado(db.Model):
<<<<<<< HEAD
=======
    __tablename__ = 'Estado'  
>>>>>>> 830632856cfb4e2b6e8e8faa463b178a19115496
    ID_Estado = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(200), nullable=False)

class Cidade(db.Model):
<<<<<<< HEAD
    ID_Cidade = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(200), nullable=False)
    FK_Estado_ID = db.Column(db.Integer, db.ForeignKey('estado.ID_Estado'), nullable=False)

class Bairro(db.Model):
    ID_Bairro = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(2000), nullable=False)
    FK_Cidade_ID = db.Column(db.Integer, db.ForeignKey('cidade.ID_Cidade'), nullable=False)

class CEP(db.Model):
    ID_CEP = db.Column(db.Integer, primary_key=True)
    numeroCEP = db.Column(db.String(20), nullable=False)
    FK_Bairro_ID = db.Column(db.Integer, db.ForeignKey('bairro.ID_Bairro'), nullable=False)

class TipoEndereco(db.Model):
=======
    __tablename__ = 'Cidade'  
    ID_Cidade = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(200), nullable=False)
    FK_Estado_ID = db.Column(db.Integer, db.ForeignKey('Estado.ID_Estado'), nullable=False)

    estado = db.relationship('Estado', backref=db.backref('Cidades', lazy=True))

class Bairro(db.Model):
    __tablename__ = 'Bairro'  
    ID_Bairro = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(2000), nullable=False)
    FK_Cidade_ID = db.Column(db.Integer, db.ForeignKey('Cidade.ID_Cidade'), nullable=False)

    cidade = db.relationship('Cidade', backref=db.backref('Bairros', lazy=True))

class CEP(db.Model):
    __tablename__ = 'CEP'  
    ID_CEP = db.Column(db.Integer, primary_key=True)
    numeroCEP = db.Column(db.String(20), nullable=False)
    FK_Bairro_ID = db.Column(db.Integer, db.ForeignKey('Bairro.ID_Bairro'), nullable=False)

    bairro = db.relationship('Bairro', backref=db.backref('ceps', lazy=True))

class TipoEndereco(db.Model):
    __tablename__ = 'Tipo_Endereco'  
>>>>>>> 830632856cfb4e2b6e8e8faa463b178a19115496
    ID_Tipo_END = db.Column(db.Integer, primary_key=True)
    Descricao = db.Column(db.String(1000), nullable=False)

class Endereco(db.Model):
<<<<<<< HEAD
=======
    __tablename__ = 'Endereco'  
>>>>>>> 830632856cfb4e2b6e8e8faa463b178a19115496
    ID_Endereco = db.Column(db.Integer, primary_key=True)
    Logradouro = db.Column(db.String(100), nullable=False)
    Numero = db.Column(db.String(10), nullable=False)
    Complemento = db.Column(db.String(100))
<<<<<<< HEAD
    FK_CEP_ID = db.Column(db.Integer, db.ForeignKey('cep.ID_CEP'), nullable=False)
    FK_Tipo_End = db.Column(db.Integer, db.ForeignKey('tipo_endereco.ID_Tipo_END'), nullable=False)

class Academia(db.Model):
    CNPJ = db.Column(db.BigInteger, primary_key=True)
    Nome = db.Column(db.String(100), nullable=False)
    FK_Endereco_ID = db.Column(db.Integer, db.ForeignKey('endereco.ID_Endereco'), nullable=False)

class TipoTelefone(db.Model):
=======
    FK_CEP_ID = db.Column(db.Integer, db.ForeignKey('CEP.ID_CEP'), nullable=False)
    FK_Tipo_End = db.Column(db.Integer, db.ForeignKey('Tipo_Endereco.ID_Tipo_END'), nullable=False)

class Academia(db.Model):
    __tablename__ = 'Academia'  
    CNPJ = db.Column(db.String(14), primary_key=True)  
    Nome = db.Column(db.String(100), nullable=False)
    FK_Endereco_ID = db.Column(db.Integer, db.ForeignKey('Endereco.ID_Endereco', ondelete="CASCADE"), nullable=True)

    endereco = db.relationship('Endereco', backref=db.backref('Academias', cascade="all, delete"))

class TipoTelefone(db.Model):
    __tablename__ = 'Tipo_Telefone'  
>>>>>>> 830632856cfb4e2b6e8e8faa463b178a19115496
    ID_TipoTEL = db.Column(db.Integer, primary_key=True)
    Descricao = db.Column(db.String(100), nullable=False)

class Pessoa(db.Model):
<<<<<<< HEAD
=======
    __tablename__ = 'Pessoa'  
>>>>>>> 830632856cfb4e2b6e8e8faa463b178a19115496
    CPF = db.Column(db.BigInteger, primary_key=True)
    Nome = db.Column(db.String(200), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    DtNasc = db.Column(db.Date, nullable=False)
<<<<<<< HEAD
    FK_Academia_ID = db.Column(db.BigInteger, db.ForeignKey('academia.CNPJ'), nullable=False)

class Telefone(db.Model):
    ID_Telefone = db.Column(db.Integer, primary_key=True)
    Telefone01 = db.Column(db.String(11), nullable=False)
    Telefone02 = db.Column(db.String(11))
    FK_CPF = db.Column(db.BigInteger, db.ForeignKey('pessoa.CPF'), nullable=False)
    FK_TipoTel_ID = db.Column(db.Integer, db.ForeignKey('tipo_telefone.ID_TipoTEL'), nullable=False)

class Usuario(db.Model):
    ID_Usuario = db.Column(db.Integer, primary_key=True)
    Login = db.Column(db.String(250), nullable=False)
    Senha = db.Column(db.String(250), nullable=False)
    FK_Pessoa_ID = db.Column(db.BigInteger, db.ForeignKey('pessoa.CPF'), nullable=False)

class Cargo(db.Model):
=======
    FK_Academia_ID = db.Column(db.BigInteger, db.ForeignKey('Academia.CNPJ'), nullable=False)

class Telefone(db.Model):
    __tablename__ = 'Telefone'  
    ID_Telefone = db.Column(db.Integer, primary_key=True)
    Telefone01 = db.Column(db.String(11), nullable=False)
    Telefone02 = db.Column(db.String(11))
    FK_CPF = db.Column(db.BigInteger, db.ForeignKey('Pessoa.CPF'), nullable=False)
    FK_TipoTel_ID = db.Column(db.Integer, db.ForeignKey('Tipo_Telefone.ID_TipoTEL'), nullable=False)

class Usuario(db.Model):
    __tablename__ = 'Usuario'  
    ID_Usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    Login = db.Column(db.String(250), nullable=False)
    Senha = db.Column(db.String(250), nullable=False)
    FK_Pessoa_ID = db.Column(db.BigInteger, db.ForeignKey('Pessoa.CPF'), nullable=False)


class Cargo(db.Model):
    __tablename__ = 'Cargo'  
>>>>>>> 830632856cfb4e2b6e8e8faa463b178a19115496
    ID_Cargo = db.Column(db.Integer, primary_key=True)
    Nome_Cargo = db.Column(db.String(1000), nullable=False)
    Atuacao = db.Column(db.String(1000), nullable=False)

class Empregado(db.Model):
<<<<<<< HEAD
=======
    __tablename__ = 'Empregado'  
>>>>>>> 830632856cfb4e2b6e8e8faa463b178a19115496
    ID_Empregado = db.Column(db.Integer, primary_key=True)
    Carga_Horaria = db.Column(db.Integer, nullable=False)
    Salario = db.Column(db.Numeric(10, 2), nullable=False)
    Descricao = db.Column(db.String(1000))
<<<<<<< HEAD
    FK_Usuario_ID = db.Column(db.Integer, db.ForeignKey('usuario.ID_Usuario'), nullable=False)
    FK_Cargo_ID = db.Column(db.Integer, db.ForeignKey('cargo.ID_Cargo'), nullable=False)

class Dieta(db.Model):
=======
    FK_Usuario_ID = db.Column(db.Integer, db.ForeignKey('Usuario.ID_Usuario'), nullable=False)
    FK_Cargo_ID = db.Column(db.Integer, db.ForeignKey('Cargo.ID_Cargo'), nullable=False)

class Dieta(db.Model):
    __tablename__ = 'Dieta'  
>>>>>>> 830632856cfb4e2b6e8e8faa463b178a19115496
    ID_Dieta = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(200), nullable=False)
    Titulo_Refeicao = db.Column(db.String(1000), nullable=False)
    Descricao_Refeicao = db.Column(db.Text, nullable=False)
<<<<<<< HEAD
    FK_Empregado_ID = db.Column(db.Integer, db.ForeignKey('empregado.ID_Empregado'), nullable=False)

class Treino(db.Model):
=======
    FK_Empregado_ID = db.Column(db.Integer, db.ForeignKey('Empregado.ID_Empregado'), nullable=False)

class Treino(db.Model):
    __tablename__ = 'Treino'  
>>>>>>> 830632856cfb4e2b6e8e8faa463b178a19115496
    ID_Treino = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(1000), nullable=False)
    Exercicio_Concluido = db.Column(db.Text, nullable=False)
    Video = db.Column(db.String(2400))
<<<<<<< HEAD
    FK_Empregado_ID = db.Column(db.Integer, db.ForeignKey('empregado.ID_Empregado'), nullable=False)

class TipoPagamento(db.Model):
=======
    FK_Empregado_ID = db.Column(db.Integer, db.ForeignKey('Empregado.ID_Empregado'), nullable=False)

class TipoPagamento(db.Model):
    __tablename__ = 'Tipo_Pagamento'  
>>>>>>> 830632856cfb4e2b6e8e8faa463b178a19115496
    ID_Forma = db.Column(db.Integer, primary_key=True)
    Descricao = db.Column(db.String(100), nullable=False)

class TipoPlano(db.Model):
<<<<<<< HEAD
=======
    __tablename__ = 'Tipo_Plano'  
>>>>>>> 830632856cfb4e2b6e8e8faa463b178a19115496
    ID_TipoPlanos = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(1000), nullable=False)
    Preco = db.Column(db.Numeric(5, 2), nullable=False)
    Beneficios = db.Column(db.String(1000), nullable=False)

class Plano(db.Model):
<<<<<<< HEAD
    ID_Planos = db.Column(db.Integer, primary_key=True)
    FK_TipoPlano_ID = db.Column(db.Integer, db.ForeignKey('tipo_plano.ID_TipoPlanos'), nullable=False)

class Aluno(db.Model):
    Matricula = db.Column(db.Integer, primary_key=True)
    FK_Usuario_ID = db.Column(db.Integer, db.ForeignKey('usuario.ID_Usuario'), nullable=False)
    FK_Planos_ID = db.Column(db.Integer, db.ForeignKey('plano.ID_Planos'), nullable=False)

class MenuPrincipal(db.Model):
=======
    __tablename__ = 'Plano'  
    ID_Planos = db.Column(db.Integer, primary_key=True)
    FK_TipoPlano_ID = db.Column(db.Integer, db.ForeignKey('Tipo_Plano.ID_TipoPlanos'), nullable=False)

class Aluno(db.Model):
    __tablename__ = 'Aluno' 
    Matricula = db.Column(db.Integer, primary_key=True)
    FK_Usuario_ID = db.Column(db.Integer, db.ForeignKey('Usuario.ID_Usuario'), nullable=False)
    FK_Planos_ID = db.Column(db.Integer, db.ForeignKey('Plano.ID_Planos'), nullable=False)

class MenuPrincipal(db.Model):
    __tablename__ = 'Menu_Principal'  
>>>>>>> 830632856cfb4e2b6e8e8faa463b178a19115496
    ID_Menu = db.Column(db.Integer, primary_key=True)
    Informacoes = db.Column(db.String(2000), nullable=False)
    Feedbacks = db.Column(db.String(2000))
    Titulo_Video = db.Column(db.String(2000))
    Videos = db.Column(db.String(2200))
<<<<<<< HEAD
    FK_Aluno_ID = db.Column(db.Integer, db.ForeignKey('aluno.Matricula'), nullable=False)
    FK_Treino_ID = db.Column(db.Integer, db.ForeignKey('treino.ID_Treino'), nullable=False)

class Comunidade(db.Model):
=======
    FK_Aluno_ID = db.Column(db.Integer, db.ForeignKey('Aluno.Matricula'), nullable=False)
    FK_Treino_ID = db.Column(db.Integer, db.ForeignKey('Treino.ID_Treino'), nullable=False)

class Comunidade(db.Model):
    __tablename__ = 'Comunidade'  
>>>>>>> 830632856cfb4e2b6e8e8faa463b178a19115496
    ID_Comunidade = db.Column(db.Integer, primary_key=True)
    Informacoes = db.Column(db.String(2000))
    Feedbacks = db.Column(db.String(2000))
    Titulo_Video = db.Column(db.String(2000))
    Videos = db.Column(db.String(2200))

class TipoFeedbacks(db.Model):
<<<<<<< HEAD
=======
    __tablename__ = 'Tipo_Feedbacks'  
>>>>>>> 830632856cfb4e2b6e8e8faa463b178a19115496
    ID_TipoFeedbacks = db.Column(db.Integer, primary_key=True)
    Topico = db.Column(db.String(2000), nullable=False)
    Descricao = db.Column(db.String(2200), nullable=False)

class Feedbacks(db.Model):
<<<<<<< HEAD
    ID_Feedbacks = db.Column(db.Integer, primary_key=True)
    FK_TipoFeedbacks_ID = db.Column(db.Integer, db.ForeignKey('tipo_feedbacks.ID_TipoFeedbacks'), nullable=False)
=======
    __tablename__ = 'Feedbacks'  
    ID_Feedbacks = db.Column(db.Integer, primary_key=True)
    FK_TipoFeedbacks_ID = db.Column(db.Integer, db.ForeignKey('Tipo_Feedbacks.ID_TipoFeedbacks'), nullable=False)
>>>>>>> 830632856cfb4e2b6e8e8faa463b178a19115496
