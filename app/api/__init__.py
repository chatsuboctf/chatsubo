from flask import Blueprint
from flask_restx import Api

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')
teams_bp = Blueprint('teams_bp', __name__, url_prefix='/api/teams')
users_bp = Blueprint('users_bp', __name__, url_prefix='/api/users')
flags_bp = Blueprint('flags_bp', __name__, url_prefix='/api/flags')
boxes_bp = Blueprint('boxes_bp', __name__, url_prefix='/api/boxes')
categories_bp = Blueprint('categories_bp', __name__, url_prefix='/api/categories')
providers_bp = Blueprint('providers_bp', __name__, url_prefix='/api/providers')
realms_bp = Blueprint('realms_bp', __name__, url_prefix='/api/realms')
vpn_bp = Blueprint('vpn_bp', __name__, url_prefix='/api/vpn')
settings_bp = Blueprint('settings_bp', __name__, url_prefix='/api/settings')
queue_bp = Blueprint('queue_bp', __name__, url_prefix='/api/queue')

teams_api = Api(teams_bp)
auth_api = Api(auth_bp)
users_api = Api(users_bp)
flags_api = Api(flags_bp)
boxes_api = Api(boxes_bp)
providers_api = Api(providers_bp)
categories_api = Api(categories_bp)
realms_api = Api(realms_bp)
vpn_api = Api(vpn_bp)
settings_api = Api(settings_bp)
queue_api = Api(queue_bp)

# Import resources to ensure view is registered
from .teams import *
from .auth import *
from .users import *
from .flags import *
from .boxes import *
from .categories import *
from .providers import *
from .vpn import *
from .queue import *
from .settings import *
from .realms import *
