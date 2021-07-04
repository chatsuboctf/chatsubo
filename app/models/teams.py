import bcrypt
from sqlalchemy.orm import relationship

import app.context


class Teams(app.context.db.Model):
    __tablename__ = "teams"

    id = app.context.db.Column(
        app.context.db.String(36),
        primary_key=True,
    )

    name = app.context.db.Column(
        app.context.db.String(200),
        nullable=False,
        unique=True
    )

    password = app.context.db.Column(
        app.context.db.String(200),
        nullable=False,
        unique=True
    )

    avatar = app.context.db.Column(
        app.context.db.Text,
        server_default="/static/img/default_avatar.png"
    )

    owner = app.context.db.Column(
        app.context.db.String(36),
        primary_key=True,
    )

    deleted = app.context.db.Column(
        app.context.db.Boolean,
        default=False
    )

    created = app.context.db.Column(
        app.context.db.DateTime,
        server_default=app.context.db.func.current_timestamp(),
        nullable=False
    )

    users = relationship("Users", backref="team")

    def __repr__(self):
        return f"<Teams {self.name}>"

    def set_password(self, passwd):
        """Create hashed password."""
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(passwd.encode(), salt)

    def check_password(self, passwd):
        """Check hashed password."""
        return bcrypt.checkpw(passwd.encode(), self.password.encode())

    def to_json(self, with_deleted_users=False, with_users=False, public=True, filter_passwd=True, with_created_boxes=True, with_flags=True):
        return {
            "id": self.id,
            "name": self.name,
            "avatar": self.avatar,
            "owner": self.owner,
            "deleted": self.deleted,
            "created": self.created.isoformat(),
            "users": [] if not self.users else [user.to_json(public=public, filter_passwd=filter_passwd, with_created_boxes=with_created_boxes, with_flags=with_flags) for user in self.users if with_users and (not user.deleted or with_deleted_users)]
        }
