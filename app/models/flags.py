import sqlalchemy
from uuid import uuid4

from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

import app.context


class Flags(app.context.db.Model):
    __tablename__ = "flags"

    id = app.context.db.Column(
        app.context.db.String(36),
        primary_key=True,
    )

    points = app.context.db.Column(
        app.context.db.Integer,
        default=0
    )

    value = app.context.db.Column(
        app.context.db.String(200),
        nullable=False
    )

    icon = app.context.db.Column(
        app.context.db.String(200),
        nullable=False,
        server_default="mdi-flag-variant"
    )

    name = app.context.db.Column(
        app.context.db.String(200),
        nullable=False
    )

    user = app.context.db.Column(
        app.context.db.Boolean,
        default=False
    )

    root = app.context.db.Column(
        app.context.db.Boolean,
        default=False
    )

    case_insensitive = app.context.db.Column(
        app.context.db.Boolean,
        default=False
    )

    dynamic = app.context.db.Column(
        app.context.db.Boolean,
        default=False
    )

    deleted = app.context.db.Column(
        app.context.db.Boolean,
        default=False
    )

    box_id = app.context.db.Column(
        app.context.db.String(36),
        app.context.db.ForeignKey('boxes.id'),
        nullable=False
    )

    def to_json(self, public=True):
        data = {
            "id": self.id,
            "points": self.points,
            "name": self.name,
            "value": self.value,
            "icon": self.icon,
            "dynamic": self.dynamic,
            "user": self.user,
            "root": self.root,
            "case_insensitive": self.case_insensitive,
            "deleted": self.deleted,
            "box_id": self.box_id,
        }

        if public:
            del data["value"]

        return data

    def __repr__(self):
        return f"<Flag {self.value}>"
