from flask import Blueprint, request, jsonify
from src.models.models import db, Usuario, Tarefa, StatusTarefa, TipoUsuario
from src.routes.auth import  tipo_usuario_required
from datetime import datetime

supervisor_bp = Blueprint('supervisor', __name__)

@supervisor_bp.route('/tarefas', methods=['POST'])

@tipo_usuario_required('supervisor')
def criar_tarefa(usuario_atual):
    """
    Endpoint para o supervisor criar uma nova tarefa
    """
    data = request.get_json()
    
    if not data or not data.get('titulo') or not data.get('funcionario_id'):
        return jsonify({'message': 'Dados incompletos para criar tarefa!'}), 400
    
    # Verificar se o funcionário existe
    funcionario = Usuario.query.filter_by(
        id=data.get('funcionario_id'),
        tipo=TipoUsuario.FUNCIONARIO.value
    ).first()
    
    if not funcionario:
        return jsonify({'message': 'Funcionário não encontrado!'}), 404
    
    nova_tarefa = Tarefa(
        titulo=data.get('titulo'),
        descricao=data.get('descricao', ''),
        funcionario_id=funcionario.id,
        supervisor_id=usuario_atual.id
    )
    
    db.session.add(nova_tarefa)
    db.session.commit()
    
    return jsonify({
        'message': 'Tarefa criada com sucesso',
        'tarefa': nova_tarefa.to_dict()
    }), 201

@supervisor_bp.route('/tarefas', methods=['GET'])

@tipo_usuario_required('supervisor')
def listar_tarefas_criadas(usuario_atual):
    """
    Endpoint para o supervisor listar todas as tarefas que ele criou
    """
    tarefas = Tarefa.query.filter_by(supervisor_id=usuario_atual.id).all()
    
    return jsonify({
        'tarefas': [tarefa.to_dict() for tarefa in tarefas]
    })

@supervisor_bp.route('/tarefas/funcionario/<int:funcionario_id>', methods=['GET'])

@tipo_usuario_required('supervisor')
def listar_tarefas_funcionario(usuario_atual, funcionario_id):
    """
    Endpoint para o supervisor listar todas as tarefas de um funcionário específico
    """
    # Verificar se o funcionário existe
    funcionario = Usuario.query.filter_by(
        id=funcionario_id,
        tipo=TipoUsuario.FUNCIONARIO.value
    ).first()
    
    if not funcionario:
        return jsonify({'message': 'Funcionário não encontrado!'}), 404
    
    tarefas = Tarefa.query.filter_by(
        funcionario_id=funcionario_id,
        supervisor_id=usuario_atual.id
    ).all()
    
    return jsonify({
        'funcionario': funcionario.to_dict(),
        'tarefas': [tarefa.to_dict() for tarefa in tarefas]
    })

@supervisor_bp.route('/tarefas/pendentes', methods=['GET'])

@tipo_usuario_required('supervisor')
def listar_tarefas_pendentes(usuario_atual):
    """
    Endpoint para o supervisor listar todas as tarefas pendentes que ele criou
    """
    tarefas = Tarefa.query.filter_by(
        supervisor_id=usuario_atual.id,
        status=StatusTarefa.PENDENTE.value
    ).all()
    
    return jsonify({
        'tarefas': [tarefa.to_dict() for tarefa in tarefas]
    })

@supervisor_bp.route('/tarefas/concluidas', methods=['GET'])

@tipo_usuario_required('supervisor')
def listar_tarefas_concluidas(usuario_atual):
    """
    Endpoint para o supervisor listar todas as tarefas concluídas que ele criou
    """
    tarefas = Tarefa.query.filter_by(
        supervisor_id=usuario_atual.id,
        status=StatusTarefa.CONCLUIDA.value
    ).all()
    
    return jsonify({
        'tarefas': [tarefa.to_dict() for tarefa in tarefas]
    })

@supervisor_bp.route('/funcionarios', methods=['GET'])

@tipo_usuario_required('supervisor')
def listar_funcionarios(usuario_atual):
    """
    Endpoint para o supervisor listar todos os funcionários disponíveis
    """
    funcionarios = Usuario.query.filter_by(tipo=TipoUsuario.FUNCIONARIO.value).all()
    
    return jsonify({
        'funcionarios': [funcionario.to_dict() for funcionario in funcionarios]
    })

@supervisor_bp.route("/tarefas/<int:tarefa_id>", methods=["PUT"])
@tipo_usuario_required(TipoUsuario.SUPERVISOR.value)
def editar_tarefa(usuario_atual, tarefa_id):
    """
    Endpoint para o supervisor editar uma tarefa que ele criou.
    Permite alterar título, descrição e o funcionário atribuído.
    """
    tarefa = Tarefa.query.filter_by(id=tarefa_id, supervisor_id=usuario_atual.id).first()

    if not tarefa:
        return jsonify({"message": "Tarefa não encontrada ou você não tem permissão para editá-la."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "Nenhum dado fornecido para atualização."}), 400

    # Atualizar campos permitidos
    if "titulo" in data:
        tarefa.titulo = data["titulo"]
    if "descricao" in data:
        tarefa.descricao = data["descricao"]
    
    # Se for reatribuir a tarefa, verificar se o novo funcionário existe
    if "funcionario_id" in data:
        novo_funcionario_id = data["funcionario_id"]
        # Verificar se o funcionário existe e é do tipo correto
        funcionario = Usuario.query.filter_by(
            id=novo_funcionario_id,
            tipo=TipoUsuario.FUNCIONARIO.value
        ).first()
        if not funcionario:
            return jsonify({"message": f"Funcionário com ID {novo_funcionario_id} não encontrado."}), 404
        tarefa.funcionario_id = novo_funcionario_id
        # Opcional: Resetar status se reatribuir? Depende da regra de negócio.
        # tarefa.status = StatusTarefa.PENDENTE.value
        # tarefa.data_conclusao = None

    db.session.commit()

    return jsonify({
        "message": "Tarefa atualizada com sucesso",
        "tarefa": tarefa.to_dict()
    })


@supervisor_bp.route("/tarefas/<int:tarefa_id>", methods=["DELETE"])
@tipo_usuario_required(TipoUsuario.SUPERVISOR.value)
def excluir_tarefa(usuario_atual, tarefa_id):
    """
    Endpoint para o supervisor excluir uma tarefa que ele criou.
    """
    tarefa = Tarefa.query.filter_by(id=tarefa_id, supervisor_id=usuario_atual.id).first()

    if not tarefa:
        return jsonify({"message": "Tarefa não encontrada ou você não tem permissão para excluí-la."}), 404

    db.session.delete(tarefa)
    db.session.commit()

    return jsonify({"message": "Tarefa excluída com sucesso"})