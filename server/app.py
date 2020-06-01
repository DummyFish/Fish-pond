import os
import sys
import signal
from flask import Flask, request, jsonify, json
from functools import wraps
from flask_cors import CORS
from multiprocessing import Process, Queue
from datetime import datetime, timedelta
import configparser
import jwt

path = os.getcwd()
# print(os.path.abspath(os.path.join(path, os.pardir)))
sys.path.append(os.path.abspath(os.path.join(path, os.pardir)))

from .auth import reset_user_password, authenticate, deactivate_session, activate_session
# from .process_data_cache import latest_date, config_filepath, configs, main_config, service_config, main_process, states
# from .services import reset_config
# from Honeypot.modify_config import reset, get_default, get_config, set_config
# from Honeypot.checkService import Check
# from Honeypot.analysis import check_service_num, get_latest_log

from Honeypot.serverInterface import reset_api, set_config_api, get_logs_api, get_service_stats_api, get_honeypot_config_api, get_service_config_api

# global latest_date
# global configs
# global main_process
# global states
# global main_config
# global service_config

# def init_services(latest_date, configs, config_filepath, main_process, states, main_config, service_config):
#     latest_date = ''
#     print("Start honeypot")
#     config_filepath = "../config.ini"
#     configs = configparser.ConfigParser()
#     configs.read(config_filepath)
#     main_process = None
#     states = Queue()
#     main_config = get_default(config_filepath)
#     service_config = get_config(config_filepath)
#     main_process = Process(target=Check, args=(main_config, service_config, config_filepath, states))
#     print("Start services...")
#     main_process.start()
#     print("Done initialization")

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    deactivate_session('default')
    exit(0)

# def reset_config(main_process, states, configs, config_filepath):
#     main_process = reset(main_process, Check, states, configs, config_filepath)

def create_app():
    signal.signal(signal.SIGINT, keyboardInterruptHandler)
    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # latest_date = ""
    # configs = None
    # config_filepath = "../config.ini"
    # main_process = None
    # states = None
    # main_config = None
    # service_config = None
    # init_services(latest_date, configs, config_filepath, main_process, states, main_config, service_config)

    def require_authenticate(f):
        @wraps(f)
        def verify_token(*args, **kwds):
            # print(args)
            # print(kwds)
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
                # print(data)
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
        # print(request)
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
        logs = get_logs_api()
        return jsonify(logs)
    
    @require_authenticate
    @app.route('/api/stats', methods=['GET'])
    def fetch_stats():
        # data = request.get_json()
        data = get_service_stats_api()
        stats = []
        for key in data:
            stats.append(data[key])
        # print(stats)
        return jsonify(stats)
    
    @require_authenticate
    @app.route('/api/logs', methods=['GET'])
    def fetch_logs():
        logs = get_logs_api()
        return jsonify(logs)

    @require_authenticate
    @app.route('/api/trend', methods=['GET'])
    def fetch_trend():
        data = request.get_json()
        return jsonify({})
    
    @require_authenticate
    @app.route('/api/config', methods=['GET'])
    def fetch_config():
        # data = request.get_json()
        service_config = get_service_config_api()
        # print("Services Config: ", service_config)
        return jsonify(service_config)

    @require_authenticate
    @app.route('/api/config', methods=['POST'])
    def update_config():
        data = request.get_json()
        print(data)
        serviceName = data['index']
        configType = data['type']
        configVal = data['payload']
        set_config_api(serviceName, configType, configVal)
        return jsonify({})

    @require_authenticate
    @app.route('/api/honeypot', methods=['GET'])
    def fetch_honeypot_config():
        main_config = get_honeypot_config_api()
        # print("Honeypot Config: ", main_config)
        return jsonify(main_config)

    @require_authenticate
    @app.route('/api/honeypot', methods=['POST'])
    def update_honeypot_config():
        data = request.get_json()
        # config.set_config(states, configs, config_filepath, "ssh", "port", "2222")
        return jsonify({})
    
    @require_authenticate
    @app.route('/api/reset', methods=['POST'])
    def reset_all():
        reset_user_password('Pas$W0rd')
        reset_api()
        return jsonify({}), 200
    return app


if __name__ == '__main__':
    create_app()
