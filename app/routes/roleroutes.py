from flask import Blueprint, request, jsonify, current_app
from models import Role, db
from app.middleware.authmiddleware import verify_token, verify_admin, verify_icer

role = Blueprint('role', __name__)


@role.route('/api/v1/role/add-role', methods=['POST'])
# @verify_token
# @verify_icer
def add_role():
    data = request.get_json()

    if not data or 'role_name' not in data:
        return jsonify({'error': 'Role name are required'}), 400

    existing_role = Role.query.filter_by(role_name=data['role_name']).first()
    if existing_role:
        return jsonify({'error': 'Role already exists'}), 409

    new_role = Role(
        role_name=data['role_name'],
    )

    db.session.add(new_role)
    db.session.commit()

    return jsonify({'message': 'Role registration successful'}), 201

@role.route('/api/v1/role/get-roles', methods=['GET'])
# @verify_token
# @verify_icer
def get_roles():
    roles = Role.query.all()
    role_list = [{'id': role.id, 'role_name': role.role_name} for role in roles]

    return jsonify({'roles': role_list}), 200