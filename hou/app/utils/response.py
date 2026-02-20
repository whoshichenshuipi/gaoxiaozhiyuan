from flask import jsonify

def success_response(data=None, msg="success"):
    return jsonify({
        "code": 200,
        "msg": msg,
        "data": data
    }), 200

def error_response(code=400, msg="error", data=None):
    return jsonify({
        "code": code,
        "msg": msg,
        "data": data
    }), code
