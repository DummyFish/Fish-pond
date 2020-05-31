import os
import sys
import signal

path = os.getcwd()
print(os.path.abspath(os.path.join(path, os.pardir)))
sys.path.append(os.path.abspath(os.path.join(path, os.pardir)))

from flask import Flask, request, jsonify, json
from functools import wraps
from flask_cors import CORS
from datetime import datetime, timedelta
from .auth import reset_user_password, authenticate, deactivate_session, activate_session
from .services import start_services, reset_config
import jwt

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    deactivate_session('default')
    exit(0)

def create_app():
    signal.signal(signal.SIGINT, keyboardInterruptHandler)
    app = Flask(__name__)
    # socketio = SocketIO(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    def require_authenticate(f):
        @wraps(f)
        def verify_token(*args, **kwds):
            print(args)
            print(kwds)
            authHeader = request.headers.get('Authorization', '').split()
            invalid = {
                'message': 'Invalid',
                'authenticated': False
            }
            expired = {
                'message': 'Session Expired',
                'authenticated': False
            }
            if len(authHeader) != 2:
                return jsonify(invalid), 401

            try:
                token = authHeader[1]
                data = jwt.decode(token, 'CD26P7ozg2nfEU4ilkhrQp0ChU6iwlhQ')
                print(data)
                return f(*args, **kwds)
            except jwt.ExpiredSignatureError:
                deactivate_session('default')
                return jsonify(expired), 401
            except (jwt.InvalidTokenError, Exception) as error:
                print(error)
                return jsonify(invalid), 401

        return verify_token

    @app.route('/api/auth/login', methods=['POST'])
    def login():
        # print(request)
        data = request.get_json()
        # print(data)
        user = authenticate(data['username'], data['password'])

        if not user:
            return jsonify({ 'message': 'Invalid credentials', 'authenticated': False }), 401

        # print(user)

        activate_session(user['username'])
        token = jwt.encode({
            'sub': user['username'],
            'iat':datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=2)},
            'CD26P7ozg2nfEU4ilkhrQp0ChU6iwlhQ')
        return jsonify({ 'token': token.decode('UTF-8') })

    @app.route('/api/auth/logout', methods=['DELETE'])
    def logout():
        deactivate_session('default')
        return jsonify({ 'authenticated': False }), 200

    @require_authenticate
    @app.route('/api/auth/user')
    def fetch_current_user():
        print(request)
        return jsonify({ 'authenticated': True }), 200

    @require_authenticate
    @app.route('/api/auth/reset_password', methods=['PATCH'])
    def reset_password():
        # print(request.data)
        data = json.loads(request.data.decode('utf8'))
        # print(data['data'])
        reset_user_password(data['data'])
        return jsonify({ 'authenticated': False }), 200

    @require_authenticate
    @app.route('/api/update', methods=['GET'])
    def fetch_new_logs():
        data = request.get_json()
        return jsonify({})
    
    @require_authenticate
    @app.route('/api/stats', methods=['GET'])
    def fetch_stats():
        data = request.get_json()
        return jsonify({})
    
    @require_authenticate
    @app.route('/api/logs', methods=['GET'])
    def fetch_logs():
        data = request.get_json()
        return jsonify({})

    @require_authenticate
    @app.route('/api/trend', methods=['GET'])
    def fetch_trend():
        data = request.get_json()
        return jsonify({})
    
    @require_authenticate
    @app.route('/api/config', methods=['GET'])
    def fetch_config():
        data = request.get_json()
        return jsonify({})

    @require_authenticate
    @app.route('/api/config', methods=['POST'])
    def update_config():
        data = request.get_json()
        return jsonify({})

    @require_authenticate
    @app.route('/api/honeypot', methods=['GET'])
    def fetch_honeypot_config():
        data = request.get_json()
        return jsonify({})

    @require_authenticate
    @app.route('/api/honeypot', methods=['POST'])
    def update_honeypot_config():
        data = request.get_json()
        return jsonify({})

    return app


if __name__ == '__main__':
    # socketio = None
    # app = create_app(socketio)
    # socketio.run(app)
    start_services()
    create_app()
