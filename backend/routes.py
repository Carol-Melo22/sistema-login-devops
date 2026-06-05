from flask import Blueprint, current_app, jsonify, request

from auth_service import validate_credentials


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return "Sistema de Login funcionando!"


@main_bp.route("/login", methods=["POST"])
def login():
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
    ):
        return jsonify({"ok": True, "message": "Login validado com sucesso."}), 200

    return jsonify({"ok": False, "message": "Usuário ou senha inválidos."}), 401