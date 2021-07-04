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
        exit(1)

    celery_app = make_celery(app)
    scheduler = sched.scheduler()


def register_socketio(socketio_server):
    global io
    io = socketio_server


def seed_db():
    try:
        with db.engine.connect() as conn:
            admin_username = os.environ.get("CHATSUBO_ADMIN_USERNAME", "Admin")
            passwd = os.environ.get("CHATSUBO_ADMIN_PASSWORD", randstr(32))
            encrypted = bcrypt.hashpw(passwd.encode(), bcrypt.gensalt())
            # Seed admin account
            # conn.execute(f"INSERT INTO users (id, username, password, email, active, admin, score) VALUES('{str(uuid4())}', '{admin_username}', '{encrypted.decode()}', 'null@dev.null', 1, 1, 0)")

            # print(f"Admin account has been created with the following password : {passwd}")
            # Seed the settings with the default values
            conn.execute(f"INSERT INTO settings (app_name) VALUES ('Chatsubo');")

            ## DEV only
            conn.execute(f"INSERT INTO users (id, username, password, email, active, admin, score) VALUES('{str(uuid4())}', 'Admin', '{bcrypt.hashpw('toor'.encode(), bcrypt.gensalt()).decode()}', 'null@dev.null', 1, 1, 0)")
            conn.execute(f"INSERT INTO users (id, username, password, email, active, admin, score) VALUES('{str(uuid4())}', 'aa', '{bcrypt.hashpw('toor'.encode(), bcrypt.gensalt()).decode()}', 'null@dev.nulla', 1, 0, 0)")
            conn.execute(f"INSERT INTO `categories` VALUES ('cb802672-3302-4608-91d0-12570470f9d9','Classic', 'classic', 'Pwn the boxes','mdi-castle',0,NULL,'2021-01-06 15:50:33');")
            descr = "L\\'enquête de l\\'ANSSI révèle qu\\'un serveur de monitoring mis en place en 2018 par un élève a permi aux attaquants de maintenir leur accès au sein de l\\'école.\n\nL\\'élève maintient mordicus que son serveur est impénétrable, pourrez-vous lui prouver qu\\'il se trompe ?"
            # insert_box = f"INSERT INTO `boxes` VALUES ('5e21414d-173c-416c-98b7-a0f49b1920c1','Kazbox #1','{descr}',4,'kazbox-v1','https://source.unsplash.com/random/450x300',NULL,'Linux','dynamic',0,1,'2021-01-06 16:08:23',NULL,'cb802672-3302-4608-91d0-12570470f9d9');"
            insert_box = f"INSERT INTO `boxes` VALUES ('0433dce8-7e9a-4b30-af20-b627efd93219','aa','aa',8,'hello-flag:v2',NULL,0,'aa',NULL,'Linux',NULL,0,0,'2021-01-15 17:20:41',NULL,'cb802672-3302-4608-91d0-12570470f9d9'),('5e21414d-173c-416c-98b7-a0f49b1920c1','Kazbox #1','{descr}',4,'kazbox-v1',NULL,0,'https://source.unsplash.com/random/450x300',NULL,'Linux','classic',0,0,'2021-01-06 16:08:23',NULL,'cb802672-3302-4608-91d0-12570470f9d9'),('88a1a25a-aebf-4e57-896d-ad0839a52925','ee','ee',7,'hello-flag:v2',NULL,60,'aa',NULL,'Linux','dynamic',0,0,'2021-05-02 19:43:38',NULL,'cb802672-3302-4608-91d0-12570470f9d9'),('eaf5e33d-3a95-428c-a377-03bee8c20a22','zz','zz',3,'hello-flag:v2',NULL,0,'zzz',NULL,'Linux',NULL,0,0,'2021-01-15 17:21:46',NULL,'cb802672-3302-4608-91d0-12570470f9d9');"
            conn.execute(insert_box)
            conn.execute("INSERT INTO `boxes` VALUES ('0433dce8-7e9a-4b30-af20-b627efd93219','aa','aa',8,'hello-flag:v2',NULL,0,'aa',NULL,'Linux',NULL,0,0,'2021-01-15 17:20:41',NULL,'cb802672-3302-4608-91d0-12570470f9d9');")
            insert_flag = "INSERT INTO `flags` VALUES ('b9ec564d-6935-473e-98cd-7c100828eb1f',25,'user','mdi-account','User',1,0,0,0,0,'5e21414d-173c-416c-98b7-a0f49b1920c1'),('e387be54-1503-4ef2-acf7-e4fa0baadf9b',50,'root','mdi-pound','Root',0,1,0,0,0,'5e21414d-173c-416c-98b7-a0f49b1920c1');"
            conn.execute(insert_flag)
            ##

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
