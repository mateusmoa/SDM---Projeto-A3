import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, jsonify
from src.models.models import db, Usuario, Tarefa, StatusTarefa, TipoUsuario
from src.routes.funcionario import funcionario_bp
from src.routes.supervisor import supervisor_bp
from src.routes.gerente import gerente_bp
from src.routes.auth import auth_bp
from src.routes.web import web_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'chave-secreta-temporaria')

# Inicializar o banco de dados
db.init_app(app)

# Registrar blueprints da API
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(funcionario_bp, url_prefix='/api/funcionario')
app.register_blueprint(supervisor_bp, url_prefix='/api/supervisor')
app.register_blueprint(gerente_bp, url_prefix='/api/gerente')

# Registrar blueprint web
app.register_blueprint(web_bp)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500

# Criar tabelas do banco de dados
with app.app_context():
    db.create_all()
    
    # Criar usuários iniciais para teste se não existirem
    if not Usuario.query.filter_by(email='funcionario@teste.com').first():
        funcionario = Usuario(
            nome='Funcionário Teste',
            email='funcionario@teste.com',
            senha='123456',
            tipo='funcionario'
        )
        db.session.add(funcionario)
        
    if not Usuario.query.filter_by(email='supervisor@teste.com').first():
        supervisor = Usuario(
            nome='Supervisor Teste',
            email='supervisor@teste.com',
            senha='123456',
            tipo='supervisor'
        )
        db.session.add(supervisor)
        
    if not Usuario.query.filter_by(email='gerente@teste.com').first():
        gerente = Usuario(
            nome='Gerente Teste',
            email='gerente@teste.com',
            senha='123456',
            tipo='gerente'
        )
        db.session.add(gerente)
        
    db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
