from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

import app.context


class UsersFlags(app.context.db.Model):
    __tablename__ = "users_flags"

    id = app.context.db.Column(
        app.context.db.String(36),
        primary_key=True,
    )

    user_id = app.context.db.Column(
        app.context.db.String(36),
        app.context.db.ForeignKey('users.id'),
        nullable=False,
    )

    flag_id = app.context.db.Column(
        app.context.db.String(36),
        app.context.db.ForeignKey('flags.id'),
        nullable=False,
    )

    value = app.context.db.Column(
        app.context.db.Text,
        nullable=False,
    )

    valid = app.context.db.Column(
        app.context.db.Boolean,
        default=False
    )

    flagged_at = app.context.db.Column(
        app.context.db.DateTime,
        index=False,
        server_default=func.now()
    )

    flag = relationship('Flags')

    def to_json(self):
        return {
            "id": self.id,
            "users_id": self.user_id,
            "flag_id": self.flag_id,
            "value": self.value,
            "valid": self.valid,
            "flagged_at": str(self.flagged_at),
            "flag": self.flag.to_json()
        }

    def __repr__(self):
        return f"<UsersFlags ({self.user_id} <> {self.flag_id})>"

