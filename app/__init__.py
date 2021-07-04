import os

from flask import Flask, current_app, send_file
from flask_socketio import SocketIO

from app.config import Config

import app.context as ctx

# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

server = Flask(__name__, static_folder="../front/dist/static")
server.config.from_object('app.config.Config')

ctx.init(server)

from app.models.sessions import Sessions
from app.models.teams import Teams
from app.models.users import Users
from app.models.boxes import Boxes
from app.models.flags import Flags
from app.models.categories import Categories
from app.models.users_flags import UsersFlags
from app.models.users_boxes import UsersBoxes
from app.models.settings import Settings

ctx.db.create_all()
ctx.seed_db()
ctx.collect_expired()

from app.api import teams_bp
from app.api import auth_bp
from app.api import flags_bp
from app.api import boxes_bp
from app.api import users_bp
from app.api import providers_bp
from app.api import categories_bp
from app.api import realms_bp
from app.api import vpn_bp
from app.api import settings_bp
from app.api import queue_bp

server.register_blueprint(teams_bp)
server.register_blueprint(flags_bp)
server.register_blueprint(auth_bp)
server.register_blueprint(boxes_bp)
server.register_blueprint(users_bp)
server.register_blueprint(providers_bp)
server.register_blueprint(categories_bp)
server.register_blueprint(realms_bp)
server.register_blueprint(vpn_bp)
server.register_blueprint(settings_bp)
server.register_blueprint(queue_bp)

server.logger.info('>>> {}'.format(Config.FLASK_ENV))

server.logger.info(server.url_map)


@server.route('/', defaults={'path': ''})
@server.route('/<path:path>')
def catch_all(path):
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)


socketio_server = SocketIO(server, cors_allowed_origins="*")
ctx.register_socketio(socketio_server)
