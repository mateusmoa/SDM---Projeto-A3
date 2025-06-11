from flask import Blueprint, request, jsonify, session # Adicionado session
from src.models.models import db, Usuario, Tarefa, StatusTarefa, TipoUsuario 
from src.routes.auth import tipo_usuario_required 
from datetime import datetime

funcionario_bp = Blueprint("funcionario", __name__)

@funcionario_bp.route("/tarefas", methods=["GET"])

@tipo_usuario_required(TipoUsuario.FUNCIONARIO.value) 
def listar_tarefas(usuario_atual):
    """
    Endpoint para o funcionário listar suas tarefas
    """
    
    tarefas = Tarefa.query.filter_by(funcionario_id=usuario_atual.id).all()
    return jsonify({
        "tarefas": [tarefa.to_dict() for tarefa in tarefas]
    })

@funcionario_bp.route("/tarefas/<int:tarefa_id>/concluir", methods=["PUT"])

@tipo_usuario_required(TipoUsuario.FUNCIONARIO.value)
def concluir_tarefa(usuario_atual, tarefa_id):
    """
    Endpoint para o funcionário marcar uma tarefa como concluída
    """
    tarefa = Tarefa.query.filter_by(id=tarefa_id, funcionario_id=usuario_atual.id).first()
    
    if not tarefa:
        return jsonify({"message": "Tarefa não encontrada ou não pertence a este funcionário"}), 404
    
    if tarefa.status == StatusTarefa.CONCLUIDA.value:
        return jsonify({"message": "Tarefa já está concluída"}), 400
    
    tarefa.concluir() 
    db.session.commit()
    
    return jsonify({
        "message": "Tarefa concluída com sucesso",
        "tarefa": tarefa.to_dict()
    })

@funcionario_bp.route("/tarefas/pendentes", methods=["GET"])

@tipo_usuario_required(TipoUsuario.FUNCIONARIO.value)
def listar_tarefas_pendentes(usuario_atual):
    """
    Endpoint para o funcionário listar apenas suas tarefas pendentes
    """
    tarefas = Tarefa.query.filter_by(
        funcionario_id=usuario_atual.id,
        status=StatusTarefa.PENDENTE.value
    ).all()
    
    return jsonify({
        "tarefas": [tarefa.to_dict() for tarefa in tarefas]
    })

@funcionario_bp.route("/tarefas/concluidas", methods=["GET"])

@tipo_usuario_required(TipoUsuario.FUNCIONARIO.value)
def listar_tarefas_concluidas(usuario_atual):
    """
    Endpoint para o funcionário listar apenas suas tarefas concluídas
    """
    tarefas = Tarefa.query.filter_by(
        funcionario_id=usuario_atual.id,
        status=StatusTarefa.CONCLUIDA.value
    ).all()
    
    return jsonify({
        "tarefas": [tarefa.to_dict() for tarefa in tarefas]
    })

@funcionario_bp.route("/perfil", methods=["GET"])

@tipo_usuario_required(TipoUsuario.FUNCIONARIO.value)
def ver_perfil(usuario_atual):
    """
    Endpoint para o funcionário visualizar seu perfil
    """
    return jsonify({
        "usuario": usuario_atual.to_dict()
    })

