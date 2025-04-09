"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    response_body = {"family": members}
    return jsonify(response_body), 200

@app.route('/members/<int:member_id>', methods=['GET'])
def handle_hello1(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"error": "Member not found"}), 404
    return jsonify(member), 200

@app.route('/members', methods=['POST'])
def handle_hello2():
    member = request.get_json()
    if "first_name" not in member or "age" not in member:
        return jsonify({"error": "Missing 'first_name' or 'age'"}), 400
    jackson_family.add_member(member)
    return jsonify({"msg": "Member added successfully"}), 200

#Tengo que hacer que se pueda añadir un id concreto, 400 bad request si ya esta definidos
#Tengo que hacer bien el test (creo que tengo que cambiar algunas funciones de nombre)

@app.route('/members/<int:member_id>', methods=['DELETE'])
def handle_hello3(member_id):
    updated_members = jackson_family.delete_member(member_id)
    if updated_members is None:
        return jsonify({"error": "Member not found"}), 400
    return jsonify({"msg": "Member deleted successfully", "family": updated_members}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
