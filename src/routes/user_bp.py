from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ..models.user import User
from ..extensions import db

user_bp = Blueprint("user", __name__)

@user_bp.get("/users")
@jwt_required()
def list_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200

@user_bp.get("/users/<int:user_id>")
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.put("/users/<int:user_id>")
@jwt_required()
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)

    db.session.commit()
    return jsonify(user.to_dict())

@user_bp.delete("/users/<int:user_id>")
@jwt_required()
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "Usuário deletado"}), 200
