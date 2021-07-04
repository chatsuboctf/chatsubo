import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

import app.context
import bcrypt


class Boxes(app.context.db.Model):
    """Box account model."""

    __tablename__ = 'boxes'
    id = app.context.db.Column(
        app.context.db.String(36),
        primary_key=True,
    )

    name = app.context.db.Column(
        app.context.db.String(100),
        nullable=False,
        unique=True
    )

    description = app.context.db.Column(
        app.context.db.Text,
    )

    difficulty = app.context.db.Column(
        app.context.db.Integer,
    )

    template = app.context.db.Column(
        app.context.db.String(200),
    )

    dockerfile = app.context.db.Column(
        app.context.db.String(200),
        nullable=True
    )

    duration = app.context.db.Column(
        app.context.db.Integer,
    )

    background = app.context.db.Column(
        app.context.db.Text,
    )

    provider = app.context.db.Column(
        app.context.db.Text,
    )

    os = app.context.db.Column(
        app.context.db.Text,
    )

    kind = app.context.db.Column(
        app.context.db.Text,
    )

    deleted = app.context.db.Column(
        app.context.db.Boolean,
        default=False
    )

    released = app.context.db.Column(
        app.context.db.Boolean,
        default=False
    )

    created_at = app.context.db.Column(
        app.context.db.DateTime,
        server_default=app.context.db.func.current_timestamp(),
        nullable=False
    )

    updated_at = app.context.db.Column(
        app.context.db.DateTime,
        server_onupdate=app.context.db.func.current_timestamp()
    )

    category_id = app.context.db.Column(
        app.context.db.String(36),
        app.context.db.ForeignKey('categories.id'),
        nullable=False
    )

    flags = relationship('Flags')
    sessions = relationship('Sessions', backref="box")
    authors = relationship('Users', secondary="users_boxes")

    def to_json(self, public=True, with_flags=False, with_deleted_flags=False):
        parsed_authors = []

        for author in self.authors:
            parsed_authors.append({
                "id": author.id,
                "name": author.username,
                "avatar": author.avatar
            })

        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "authors": parsed_authors,
            "category": self.category.to_json(),
            "category_id": self.category_id,
            "kind": self.kind,
            "duration": self.duration,
            "difficulty": self.difficulty,
            "background": self.background,
            "os": self.os,
            "template": self.template,
            "created_at": str(self.created_at),
            "deleted": self.deleted,
            "released": self.released,
        }

        if with_flags:
            flags = [] if not self.flags else [flag.to_json(public=public) for flag in self.flags]
            flags = [flag for flag in flags if with_deleted_flags or not flag["deleted"]]
            flags.reverse()
            data["flags"] = flags

        if public:
            del data["template"]

        return data

    def __repr__(self):
        return f"<Box {self.name}>"
