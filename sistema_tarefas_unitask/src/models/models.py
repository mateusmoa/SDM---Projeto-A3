from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

class TipoUsuario(Enum):
    FUNCIONARIO = 'funcionario'
    SUPERVISOR = 'supervisor'
    GERENTE = 'gerente'

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com tarefas (para funcionários)
    tarefas = db.relationship('Tarefa', backref='funcionario', lazy=True, 
                             foreign_keys='Tarefa.funcionario_id')
    
    # Relacionamento com tarefas criadas (para supervisores)
    tarefas_criadas = db.relationship('Tarefa', backref='supervisor', lazy=True,
                                     foreign_keys='Tarefa.supervisor_id')
    
    def __init__(self, nome, email, senha, tipo):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'tipo': self.tipo,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None
        }

class StatusTarefa(Enum):
    PENDENTE = 'pendente'
    CONCLUIDA = 'concluida'

class Tarefa(db.Model):
    __tablename__ = 'tarefas'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default=StatusTarefa.PENDENTE.value, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_conclusao = db.Column(db.DateTime, nullable=True)
    
    # Chaves estrangeiras
    funcionario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    def __init__(self, titulo, descricao, funcionario_id, supervisor_id):
        self.titulo = titulo
        self.descricao = descricao
        self.funcionario_id = funcionario_id
        self.supervisor_id = supervisor_id
        self.status = StatusTarefa.PENDENTE.value
    
    def concluir(self):
        self.status = StatusTarefa.CONCLUIDA.value
        self.data_conclusao = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'status': self.status,
            'funcionario_id': self.funcionario_id,
            'supervisor_id': self.supervisor_id,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_conclusao': self.data_conclusao.isoformat() if self.data_conclusao else None
        }
