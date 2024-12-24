from flask import Blueprint, jsonify, Response, send_from_directory, request
import os
from httpstatus import HttpStatus

login_bp= Blueprint('/login', __name__)

status = HttpStatus()

@login_bp.route('/sign_up_user', methods=['POST'])
def sign_up_user():
    try:
        data = request.get_json()
        print(data)
        return jsonify(data), 200

    except Exception as e:
        return None, 200

@login_bp.route('/login_user', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        print(data)
        return jsonify(data), 200

    except Exception as e:
        return None, 200