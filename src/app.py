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
    return jsonify(members), 200

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member is None:
        return jsonify({"error": "Member not found"}), 404
    return jsonify(member), 200

@app.route('/members', methods=['POST'])
def handle_hello2():
    member = request.get_json()
    if "id" in member:
        existing_member = jackson_family.get_member(member["id"])
        if existing_member is not None:
            return jsonify({"error": "ID already in use"}), 400

    if "first_name" not in member or "age" not in member:
        return jsonify({"error": "Missing 'first_name' or 'age'"}), 400

    jackson_family.add_member(member)
    return jsonify(member), 200

@app.route('/members/<int:id>', methods=['DELETE'])
def handle_hello3(id):
    updated_members = jackson_family.delete_member(id)
    if updated_members is None:
        return jsonify({"error": "Member not found"}), 400
    return jsonify({"done": True}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
