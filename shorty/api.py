from flask import Blueprint, jsonify


api = Blueprint('api', __name__)


@api.route('/shortlinks', methods=['POST'])
def create_shortlink():
    return jsonify({})
