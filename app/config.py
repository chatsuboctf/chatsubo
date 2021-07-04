"""
Global Flask Application Setting

See `.flaskenv` for default settings.
 """

import os


class Config(object):
    # If not set fall back to production for safety
    ENV = os.getenv('ENV', 'production')
    FLASK_ENV = ENV
    # Set FLASK_SECRET on your production Environment
    SECRET_KEY = os.getenv('FLASK_SECRET', 'changeme')
    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)
    DIST_DIR = os.path.join(ROOT_DIR, f"front/{'dist' if ENV == 'production' else 'public'}")
    UPLOAD_FOLDER = os.path.join(DIST_DIR, "static/uploads")
    AVATARS_FOLDER = os.path.join(UPLOAD_FOLDER, "avatars")
    LOGO_IMG_PATH = os.path.join(UPLOAD_FOLDER, "logo", "logo.png")
    TEAMS_AVATARS_FOLDER = os.path.join(UPLOAD_FOLDER, "teams")
    BOXES_AVATARS_FOLDER = os.path.join(UPLOAD_FOLDER, "boxes")
    SQLALCHEMY_DATABASE_URI = os.getenv("CHATSUBO_DATABASE_URL", "mysql://chatsubo:chatsubo@localhost/chatsubo")
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    RESET_DELAY = 30  # minutes

    if not os.path.exists(DIST_DIR):
        raise Exception(
            'DIST_DIR not found: {}'.format(DIST_DIR))


START_BOX_POOL_WORKERS = 10
STOP_BOX_POOL_WORKERS = 5
