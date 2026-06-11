from flask import Flask, render_template, request, jsonify, current_app, session, redirect, url_for, Blueprint
import os
from config import Config
from auth_service import validate_credentials

app = Flask(__name__, template_folder='../frontend')
app.config.from_object(Config)
app.secret_key = os.getenv('SECRET_KEY', 'chave-secreta-fallback')

USUARIOS = {'admin': 'admin123', 'estudante': 'senha123'}

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return "Sistema de Login funcionando!"

@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('index.html')

    data = request.get_json(silent=True) or {}
    username = data.get("usuario") or data.get("username")
    password = data.get("senha") or data.get("password")

    if not username or not password:
        return jsonify({"ok": False, "message": "Usuário e senha são obrigatórios."}), 400

    if validate_credentials(
        username,
        password,
        current_app.config["VALID_USERNAME"],
        current_app.config["VALID_PASSWORD"],
    ) or (username in USUARIOS and USUARIOS[username] == password):
        session['usuario'] = username
        return jsonify({"ok": True, "message": "Login validado com sucesso."}), 200

    return jsonify({"ok": False, "message": "Usuário ou senha inválidos."}), 401

app.register_blueprint(main_bp)

@app.route('/register', methods=['GET', 'POST'])
def register():
    erro = None
    if request.method == 'POST':
        u = request.form.get('username')
        s = request.form.get('password')
        if not u or not s:
            erro = "Usuário e senha são obrigatórios!"
        elif u in USUARIOS:
            erro = 'Este usuário já existe!'
        else:
            USUARIOS[u] = s
            session['usuario'] = u
            return redirect(url_for('sucesso'))
    return render_template('cadastro.html', erro=erro)

@app.route('/sucesso')
def sucesso():
    if 'usuario' in session:
        return render_template('sucesso.html', usuario=session['usuario'])
    return redirect(url_for('main.login'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('main.login'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
