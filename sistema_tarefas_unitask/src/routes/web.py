from flask import render_template, redirect, url_for, request, jsonify, Blueprint
from src.models.models import db, Usuario, Tarefa, TipoUsuario, StatusTarefa
import os

# Blueprint para as rotas web
web_bp = Blueprint("web", __name__)

@web_bp.route("/")
def index():
    # TODO: Verificar se o usuário está logado na sessão e redirecionar
    # para o dashboard apropriado ou para a página de login.
    # Por enquanto, redireciona para login.
    return redirect(url_for("web.login"))

@web_bp.route("/login")
def login():
    return render_template("login.html")

@web_bp.route("/register")
def register():
    return render_template("register.html")

# TODO: Adicionar verificação de sessão (@login_required ou similar)
# antes de renderizar os dashboards para garantir que apenas usuários
# autenticados e com o tipo correto possam acessá-los.

@web_bp.route("/funcionario")
def funcionario_dashboard():
    # Exemplo: verificar se o usuário logado é funcionário
    # if 'tipo_usuario' not in session or session['tipo_usuario'] != TipoUsuario.FUNCIONARIO.value:
    #     return redirect(url_for('web.login'))
    return render_template("funcionario.html")

@web_bp.route("/supervisor")
def supervisor_dashboard():
    # Exemplo: verificar se o usuário logado é supervisor
    # if 'tipo_usuario' not in session or session['tipo_usuario'] != TipoUsuario.SUPERVISOR.value:
    #     return redirect(url_for('web.login'))
    return render_template("supervisor.html")

@web_bp.route("/gerente")
def gerente_dashboard():
    # Exemplo: verificar se o usuário logado é gerente
    # if 'tipo_usuario' not in session or session['tipo_usuario'] != TipoUsuario.GERENTE.value:
    #     return redirect(url_for('web.login'))
    return render_template("gerente.html")

