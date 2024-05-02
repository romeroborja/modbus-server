from flask import Flask
from flask_cors import CORS
from web.config import Config
from web.api import api, routes
from web.wsgi import StandaloneApplication, get_config

import logging

logger = logging.getLogger(__name__)

def create_app(modbus_manager: object) -> object:
  app = Flask(__name__)
    
  CORS(app, resources={r'/*': {'origins': '*', "supports_credentials": True}}, expose_headers=["Content-Type", "X-CSRFToken"])  
  app.config.from_object(Config)

  routes.route_generator(modbus_manager)
  app.register_blueprint(api)

  return app

def run_flask(modbus_manager: object) -> None:    
  app = create_app(modbus_manager)

  if app.config['ENV'] == 'development':
    app.run(host=app.config['IP'], port=app.config['PORT'])
  else:
    host = app.config['IP']
    port = app.config['PORT']
    app.logger.info(f'Starting Flask app on {host}:{port}')  
    StandaloneApplication(app, get_config(host=host, port=port)).run()