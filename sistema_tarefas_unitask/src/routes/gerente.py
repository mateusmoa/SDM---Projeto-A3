from flask import Blueprint, request, jsonify
from src.models.models import db, Usuario, Tarefa, StatusTarefa, TipoUsuario
from src.routes.auth import tipo_usuario_required
from sqlalchemy import func

gerente_bp = Blueprint('gerente', __name__)

@gerente_bp.route('/relatorios/tarefas-cadastradas', methods=['GET'])
@tipo_usuario_required('gerente')
def relatorio_tarefas_cadastradas(usuario_atual):
    """
    Endpoint para o gerente obter relatório de todas as tarefas cadastradas
    """
    tarefas = Tarefa.query.all()
    
    if not tarefas:
        return jsonify({'message': 'Não há tarefas cadastradas no sistema'}), 404
    
    # Agrupar tarefas por supervisor
    tarefas_por_supervisor = {}
    for tarefa in tarefas:
        supervisor = Usuario.query.filter_by(id=tarefa.supervisor_id).first()
        if supervisor.nome not in tarefas_por_supervisor:
            tarefas_por_supervisor[supervisor.nome] = []
        
        tarefas_por_supervisor[supervisor.nome].append(tarefa.to_dict())
    
    return jsonify({
        'total_tarefas': len(tarefas),
        'tarefas_por_supervisor': tarefas_por_supervisor
    })

@gerente_bp.route('/relatorios/tarefas-pendentes', methods=['GET'])
@tipo_usuario_required('gerente')
def relatorio_tarefas_pendentes(usuario_atual):
    """
    Endpoint para o gerente obter relatório de todas as tarefas pendentes
    """
    tarefas_pendentes = Tarefa.query.filter_by(status=StatusTarefa.PENDENTE.value).all()
    
    if not tarefas_pendentes:
        return jsonify({'message': 'Não há tarefas pendentes no sistema'}), 404
    
    # Agrupar tarefas por funcionário
    tarefas_por_funcionario = {}
    for tarefa in tarefas_pendentes:
        funcionario = Usuario.query.filter_by(id=tarefa.funcionario_id).first()
        if funcionario.nome not in tarefas_por_funcionario:
            tarefas_por_funcionario[funcionario.nome] = []
        
        tarefas_por_funcionario[funcionario.nome].append(tarefa.to_dict())
    
    return jsonify({
        'total_tarefas_pendentes': len(tarefas_pendentes),
        'tarefas_por_funcionario': tarefas_por_funcionario
    })

@gerente_bp.route('/relatorios/funcionarios-sem-tarefas-pendentes', methods=['GET'])
@tipo_usuario_required('gerente')
def relatorio_funcionarios_sem_tarefas_pendentes(usuario_atual):
    """
    Endpoint para o gerente obter relatório de funcionários sem tarefas pendentes
    """
    # Subquery para encontrar funcionários com tarefas pendentes
    funcionarios_com_pendencias = db.session.query(Tarefa.funcionario_id).filter_by(
        status=StatusTarefa.PENDENTE.value
    ).distinct().subquery()
    
    # Encontrar funcionários que não estão na subquery
    funcionarios_sem_pendencias = Usuario.query.filter_by(
        tipo=TipoUsuario.FUNCIONARIO.value
    ).filter(
        ~Usuario.id.in_(funcionarios_com_pendencias)
    ).all()
    
    if not funcionarios_sem_pendencias:
        return jsonify({'message': 'Todos os funcionários possuem tarefas pendentes'}), 404
    
    return jsonify({
        'total_funcionarios_sem_pendencias': len(funcionarios_sem_pendencias),
        'funcionarios': [funcionario.to_dict() for funcionario in funcionarios_sem_pendencias]
    })

@gerente_bp.route('/relatorios/resumo-geral', methods=['GET'])
@tipo_usuario_required('gerente')
def relatorio_resumo_geral(usuario_atual):
    """
    Endpoint para o gerente obter um resumo geral do sistema
    """
    total_funcionarios = Usuario.query.filter_by(tipo=TipoUsuario.FUNCIONARIO.value).count()
    total_supervisores = Usuario.query.filter_by(tipo=TipoUsuario.SUPERVISOR.value).count()
    total_tarefas = Tarefa.query.count()
    total_tarefas_pendentes = Tarefa.query.filter_by(status=StatusTarefa.PENDENTE.value).count()
    total_tarefas_concluidas = Tarefa.query.filter_by(status=StatusTarefa.CONCLUIDA.value).count()
    
    # Calcular taxa de conclusão
    taxa_conclusao = 0
    if total_tarefas > 0:
        taxa_conclusao = (total_tarefas_concluidas / total_tarefas) * 100
    
    return jsonify({
        'total_funcionarios': total_funcionarios,
        'total_supervisores': total_supervisores,
        'total_tarefas': total_tarefas,
        'total_tarefas_pendentes': total_tarefas_pendentes,
        'total_tarefas_concluidas': total_tarefas_concluidas,
        'taxa_conclusao': f'{taxa_conclusao:.2f}%'
    })

@gerente_bp.route('/usuarios', methods=['GET'])
@tipo_usuario_required('gerente')
def listar_usuarios(usuario_atual):
    """
    Endpoint para o gerente listar todos os usuários do sistema
    """
    # Obter todos os usuários, exceto o próprio gerente logado
    usuarios = Usuario.query.filter(Usuario.id != usuario_atual.id).all()
    
    return jsonify({
        'usuarios': [usuario.to_dict() for usuario in usuarios]
    })

@gerente_bp.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
@tipo_usuario_required('gerente')
def remover_usuario(usuario_atual, usuario_id):
    """
    Endpoint para o gerente remover um usuário do sistema
    """
    # Verificar se o usuário existe
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    # Impedir que um gerente remova outro gerente
    if usuario.tipo == TipoUsuario.GERENTE.value:
        return jsonify({'message': 'Não é permitido remover outro gerente do sistema'}), 403
    
    # Impedir que o gerente remova a si mesmo
    if usuario.id == usuario_atual.id:
        return jsonify({'message': 'Não é permitido remover a si mesmo'}), 403
    
    # Se for um supervisor, verificar se ele tem tarefas associadas
    if usuario.tipo == TipoUsuario.SUPERVISOR.value:
        tarefas_supervisor = Tarefa.query.filter_by(supervisor_id=usuario.id).first()
        if tarefas_supervisor:
            return jsonify({
                'message': 'Este supervisor possui tarefas associadas. Transfira ou remova as tarefas antes de excluir o usuário'
            }), 400
    
    # Se for um funcionário, verificar se ele tem tarefas associadas
    if usuario.tipo == TipoUsuario.FUNCIONARIO.value:
        tarefas_funcionario = Tarefa.query.filter_by(funcionario_id=usuario.id).first()
        if tarefas_funcionario:
            return jsonify({
                'message': 'Este funcionário possui tarefas associadas. Transfira ou remova as tarefas antes de excluir o usuário'
            }), 400
    
    # Remover o usuário
    db.session.delete(usuario)
    db.session.commit()
    
    return jsonify({
        'message': f'Usuário {usuario.nome} removido com sucesso'
    })
