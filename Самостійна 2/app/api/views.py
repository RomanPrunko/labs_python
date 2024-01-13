import jwt
from flask import jsonify, request, make_response
from sqlalchemy.exc import IntegrityError
from . import api_bp
from app.todo.models import Todo
from app.authentication.models import User
from datetime import datetime, timedelta
from app import db, basic_auth
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required
from config import Config
from app.telephones.models import Telephone


@api_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({
        "message": "pong"
    })


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return True
    return False


@api_bp.route('/login')
def login():
    auth = request.authorization
        
    user = User.query.filter_by(username=auth.username).first()
    
    if not user:
        return make_response('No such user in database', 401, {'WWW-Authenticate': 'Bearer realm="Authentication Required"'}) 

    if check_password_hash(user.password, auth.password):
        expiry = datetime.utcnow() + timedelta(minutes=30)
        subject = "access"
        secret_key = Config.SECRET_KEY
        
        token = jwt.encode(
            {"sub": subject, "username": user.username, "exp": expiry},
            secret_key, 
            algorithm="HS256"
        )
        
        return jsonify({"token": token})
    
    return make_response('Invalid username or password', 401, {'WWW-Authenticate': 'Bearer realm="Authentication Required"'})


@api_bp.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
    todos = Todo.query.all()
    
    todo_dict = []
    
    for todo in todos:
        item = dict(
            id = todo.id,
            title = todo.title,
            description = todo.description,
            complete = todo.complete
        )
        
        todo_dict.append(item)
        
    return jsonify(todo_dict)


@api_bp.route('/todos', methods=['POST'])
@jwt_required()
def post_todos():
    new_data = request.get_json()
    
    if not new_data:
        return jsonify({"message": "no input data provided"}), 400
    
    if not new_data.get('title') or not new_data.get('description'):
        return jsonify({"message": "not keys"}), 422 
    
    todo = Todo(title=new_data.get('title'), description=new_data.get('description'))
    
    db.session.add(todo)
    db.session.commit()
    
    new_todo = Todo.query.filter_by(id=todo.id).first()
    
    return jsonify({
        #"message": "todo was add"
        "id": new_todo.id,
        "title": new_todo.title
    }), 201
    

@api_bp.route('/todos/<int:id>', methods=['GET'])
@jwt_required()
def get_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    
    if not todo:
        return jsonify({"message": f"todo with id = {id} not found"}), 404
    
    return jsonify({
        "id": todo.id,
        "title": todo.title,
        "description": todo.description
    }), 200
    

@api_bp.route('/todos/<int:id>', methods=['PUT'])
@jwt_required()
def update_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    
    if not todo:
        return jsonify({"message": f"todo with id = {id} not found"}), 404
    
    new_data = request.get_json()
    
    if not new_data:
        return jsonify({"message": "no input data provided"}), 400
    
    if new_data.get('title'):
        todo.title = new_data.get('title')
    
    if new_data.get('description'):
        todo.description = new_data.get('description')
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        
    return jsonify({
        "message": "todo was updated"
    }), 204
    

@api_bp.route('/todos/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_todo(id):
      todo = Todo.query.get(id)
      db.session.delete(todo)
      db.session.commit()
      return jsonify({"message" : "Resource successfully deleted."}), 200

# Telephones API

@api_bp.route('/telephones', methods=['GET'])
@jwt_required()
def get_telephones():
    telephones = Telephone.query.all()
    telephones_list = [{
        'id': telephone.id,
        'name': telephone.name,
        'model': telephone.model,
        'phone_number': telephone.phone_number,
        'release_year': telephone.release_year
    } for telephone in telephones]
    return jsonify({'telephones': telephones_list})

@api_bp.route('/telephones/<int:id>', methods=['GET'])
@jwt_required()
def get_telephone(id):
    telephone = Telephone.query.get_or_404(id)
    return jsonify({
        'id': telephone.id,
        'name': telephone.name,
        'model': telephone.model,
        'phone_number': telephone.phone_number,
        'release_year': telephone.release_year
    })

@api_bp.route('/telephones', methods=['POST'])
@jwt_required()
def create_telephone():
    data = request.json
    try:
        new_telephone = Telephone(
            name=data['name'],
            model=data['model'],
            phone_number=data['phone_number'],
            release_year=data.get('release_year')
        )
        db.session.add(new_telephone)
        db.session.commit()
        return jsonify({'message': 'Telephone created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500
    finally:
        db.session.close()

@api_bp.route('/telephones/<int:id>', methods=['PUT'])
@jwt_required()
def update_telephone(id):
    telephone = Telephone.query.get_or_404(id)
    data = request.json
    telephone.name = data.get('name', telephone.name)
    telephone.model = data.get('model', telephone.model)
    telephone.phone_number = data.get('phone_number', telephone.phone_number)
    telephone.release_year = data.get('release_year', telephone.release_year)
    db.session.commit()
    return jsonify({'message': 'Telephone updated successfully'}), 200

@api_bp.route('/telephones/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_telephone(id):
    telephone = Telephone.query.get_or_404(id)
    db.session.delete(telephone)
    db.session.commit()
    return jsonify({'message': 'Telephone deleted successfully'}), 200