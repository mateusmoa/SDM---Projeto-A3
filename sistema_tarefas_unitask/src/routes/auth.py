from flask import Blueprint, request, jsonify, session
from src.models.models import db, Usuario, TipoUsuario
from functools import wraps
import os

auth_bp = Blueprint('auth', __name__)

# Decorator para verificar tipo de usuário

def tipo_usuario_required(tipo_usuario):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'usuario_id' not in session:
                return jsonify({'message': 'Usuário não autenticado!'}), 401
            
            usuario_id = session['usuario_id']
            usuario_atual = Usuario.query.filter_by(id=usuario_id).first()
            
            if not usuario_atual:
                 # Isso pode indicar um problema de sessão vs banco de dados
                session.pop('usuario_id', None)
                session.pop('tipo_usuario', None)
                return jsonify({'message': 'Usuário da sessão não encontrado no banco de dados!'}), 401

            if usuario_atual.tipo != tipo_usuario:
                return jsonify({'message': f'Acesso negado. Apenas {tipo_usuario} podem acessar este recurso.'}), 403
            
            # Passa o usuário atual para a função original
            return f(usuario_atual, *args, **kwargs)
        return decorated_function
    return decorator

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('senha'):
        return jsonify({'message': 'Dados de login incompletos!'}), 400
        
    usuario = Usuario.query.filter_by(email=data.get('email')).first()
    
    if not usuario or usuario.senha != data.get('senha'): # Simplificando a verificação de senha (sem hash)
        return jsonify({'message': 'Credenciais inválidas!'}), 401
        
    # Configura a sessão do usuário 
    session['usuario_id'] = usuario.id
    session['tipo_usuario'] = usuario.tipo
    
    return jsonify({
        'message': 'Login bem-sucedido!',
        'usuario': usuario.to_dict()
    })

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Limpa a sessão do usuário
    session.pop('usuario_id', None)
    session.pop('tipo_usuario', None)
    return jsonify({'message': 'Logout bem-sucedido!'})


@auth_bp.route('/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    
    if not data or not data.get('nome') or not data.get('email') or not data.get('senha') or not data.get('tipo'):
        return jsonify({'message': 'Dados de registro incompletos!'}), 400
        
    # Verificar se o email já está em uso
    if Usuario.query.filter_by(email=data.get('email')).first():
        return jsonify({'message': 'Email já cadastrado!'}), 400
        
    # Verificar se o tipo de usuário é válido
    tipo = data.get('tipo')
    if tipo not in [t.value for t in TipoUsuario]:
        return jsonify({'message': 'Tipo de usuário inválido!'}), 400
        
    novo_usuario = Usuario(
        nome=data.get('nome'),
        email=data.get('email'),
        senha=data.get('senha'),  
        tipo=tipo
    )
    
    db.session.add(novo_usuario)
    db.session.commit()
    
    return jsonify({'message': 'Usuário registrado com sucesso!', 'usuario': novo_usuario.to_dict()}), 201

