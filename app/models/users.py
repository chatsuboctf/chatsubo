from datetime import datetime, timedelta

from flask import current_app
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

import app.context
import bcrypt


class Users(app.context.db.Model):
    """User account model"""

    __tablename__ = 'users'
    id = app.context.db.Column(
        app.context.db.String(36),
        primary_key=True,
    )

    username = app.context.db.Column(
        app.context.db.String(100),
        nullable=False,
        unique=True
    )

    session = app.context.db.Column(
        app.context.db.String(200),  # 128 bytes encoded in base64 with stripped "="
    )

    email = app.context.db.Column(
        app.context.db.String(60),
        unique=True,
    )

    password = app.context.db.Column(
        app.context.db.String(200),
        nullable=False
    )

    avatar = app.context.db.Column(
        app.context.db.String(200),
        server_default="/static/img/default_avatar.png"
    )

    score = app.context.db.Column(
        app.context.db.Integer,
        default=0,
        nullable=False
    )

    active = app.context.db.Column(
        app.context.db.Boolean,
        default=False
    )

    admin = app.context.db.Column(
        app.context.db.Boolean,
        default=False
    )

    deleted = app.context.db.Column(
        app.context.db.Boolean,
        default=False
    )

    created_at = app.context.db.Column(
        app.context.db.DateTime,
        index=False,
        server_default=func.now()
    )

    last_reset = app.context.db.Column(
        app.context.db.DateTime,
        index=False,
    )

    last_login = app.context.db.Column(
        app.context.db.DateTime,
        index=False,
    )

    team_id = app.context.db.Column(
        app.context.db.String(36),
        app.context.db.ForeignKey('teams.id'),
        default=None
    )

    sessions = relationship('Sessions', backref="owner")
    created_boxes = relationship("Boxes", secondary="users_boxes")
    flags = relationship("Flags", secondary="users_flags")

    def set_password(self, passwd):
        """Create hashed password."""
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(passwd.encode(), salt)

    def check_password(self, passwd):
        """Check hashed password."""
        return bcrypt.checkpw(passwd.encode(), self.password.encode())

    def update_last_login(self):
        self.last_login = func.now()

    def update_last_reset(self):
        self.last_reset = func.now()

    def can_reset(self):
        if not self.last_reset:
            return True

        now = datetime.now()
        if now - timedelta(minutes=current_app.config.get("RESET_DELAY", 30)) <= self.last_reset <= now:
            return False

        return True

    def to_json(self, public=True, filter_passwd=True, with_created_boxes=True, with_flags=True):
        data = {
            "id": self.id,
            "username": self.username,
            "password": self.password if not filter_passwd else "",
            "email": self.email,
            "session": self.session,
            "score": self.score,
            "active": self.active,
            "avatar": self.avatar,
            "admin": self.admin,
            "team": self.team.to_json() if self.team else None,
            "team_id": self.team_id,
            "flags": [] if not self.flags else [flag.to_json(public=public) for flag in self.flags if with_flags],
            "created_boxes": [] if not self.created_boxes else [box.to_json() for box in self.created_boxes if with_created_boxes],
            "created_at": str(self.created_at),
        }

        if not filter_passwd:
            data.update({"password": self.password})

        if public:
            del data["email"]
            del data["session"]
            del data["active"]
            # del data["admin"]

        return data

    def __repr__(self):
        return f"<User {self.username}>"
