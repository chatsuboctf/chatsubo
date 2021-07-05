import os
import random
import sched
import string
from datetime import datetime
from uuid import uuid4

import sqlalchemy
import yaml

import bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.exc import ProgrammingError, IntegrityError, OperationalError

from app import config
from app.providers.exc import MissingProviderConfigException, BackendConnectionException, VpnProviderErrorException
from app.providers.providers import Providers
from app.providers.vpn_providers import VpnProviders
from app.queue import make_celery

providers = Providers()
vpns = VpnProviders()
db = None
io = None
scheduler = None
celery_app = None


def init(app):
    global db
    global providers
    global vpns
    global scheduler
    global celery_app

    with open("config/chatsubo.yml", 'r') as f:
        try:
            app.config.update(yaml.safe_load(f))
        except yaml.YAMLError as exc:
            print(exc)

    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI")

    try:
        if not database_exists(db_uri):
            create_database(db_uri)
    except sqlalchemy.exc.OperationalError as e:
        print(f"Failed to start db instance : {e}")
        exit(1)

    # The MySQL URI is defined in the Flask's config file
    db = SQLAlchemy(app)

    pv_configs = app.config.get("providers")
    if not pv_configs:
        print("No providers config found")
        exit(1)

    vpn_configs = app.config.get("vpns")
    if not vpn_configs:
        print("No VPN config found")
        exit(1)

    try:
        vpns.load(vpn_configs)
    except (MissingProviderConfigException, VpnProviderErrorException) as e:
        print(f"Failed to load VPN config : {e}")
        exit(1)

    try:
        providers.load(pv_configs, vpns)
    except (MissingProviderConfigException, BackendConnectionException, VpnProviderErrorException) as e:
        print(f"Failed to load provider '{e.pv_name}' : {str(e.error)}")

    celery_app = make_celery(app)
    scheduler = sched.scheduler()


def register_socketio(socketio_server):
    global io
    io = socketio_server


def seed_db():
    try:
        with db.engine.connect() as conn:
            # Seed the settings with the default values
            conn.execute(f"INSERT INTO settings (app_name) VALUES ('Chatsubo');")

            if os.environ.get("ENV", "production") == "development":
                ## DEV only
                conn.execute(f"INSERT INTO users (id, username, password, email, active, admin, score) VALUES('{str(uuid4())}', 'Admin', '{bcrypt.hashpw('toor'.encode(), bcrypt.gensalt()).decode()}', 'null@dev.null', 1, 1, 0)")
                conn.execute(f"INSERT INTO users (id, username, password, email, active, admin, score) VALUES('{str(uuid4())}', 'test', '{bcrypt.hashpw('toor'.encode(), bcrypt.gensalt()).decode()}', 'test@dev.null', 1, 0, 0)")
                conn.execute(f"INSERT INTO `categories` VALUES ('cb802672-3302-4608-91d0-12570470f9d9','Classic', 'classic', 'Pwn the boxes','mdi-castle',0,NULL,'2021-01-06 15:50:33');")
                ##
            else:
                admin_username = os.environ.get("CHATSUBO_ADMIN_USERNAME", "admin")
                passwd = os.environ.get("CHATSUBO_ADMIN_PASSWORD", randstr(32))
                encrypted = bcrypt.hashpw(passwd.encode(), bcrypt.gensalt())

                # Seed admin account
                conn.execute(f"INSERT INTO users (id, username, password, active, admin, score) VALUES('{str(uuid4())}', '{admin_username}', '{encrypted.decode()}', 1, 1, 0)")
                print(f"Admin account has been created with the following password : {passwd}")

    except ProgrammingError as e:
        print(e)
    except IntegrityError:
        pass  # Admin account already created
    except OperationalError as e:
        print(e)
        pass  # Admin account already created
    except Exception as e:
        print("Unknown exception")
        print(e)


def collect_expired():
    from app.models.sessions import Sessions
    global db

    sessions = db.session.query(Sessions).all()
    if not sessions:
        return

    now = datetime.now()

    for sess in sessions:
        if not sess.expires_at or now > sess.expires_at:
            print(f"Found expired session : {sess.id}")
            print("Cleaning...")
            try:
                providers.stop_dynamic_instance(sess.realm, sess.id)
                print("Session removed")
                db.session.delete(sess)
                db.session.commit()
            except Exception as e:
                print(e)


def randstr(length=8):
    """
    Generates a random password having the specified length
    :length -> length of password to be generated. Defaults to 8
        if nothing is specified.
    :returns string <class 'str'>
    """

    LETTERS = string.ascii_letters
    NUMBERS = string.digits
    PUNCTUATION = string.punctuation

    # create alphanumerical from string constants
    printable = f'{LETTERS}{NUMBERS}{PUNCTUATION}'

    # convert printable from string to list and shuffle
    printable = list(printable)
    random.shuffle(printable)

    # generate random password and convert to string
    blob = random.choices(printable, k=length)
    blob = ''.join(blob)
    return blob
