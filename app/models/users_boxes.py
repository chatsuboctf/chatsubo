from sqlalchemy_utils import UUIDType

import app.context


class UsersBoxes(app.context.db.Model):
    __tablename__ = "users_boxes"

    user_id = app.context.db.Column(
        app.context.db.String(36),
        app.context.db.ForeignKey('users.id'),
        nullable=False,
        primary_key=True
    )

    box_id = app.context.db.Column(
        app.context.db.String(36),
        app.context.db.ForeignKey('boxes.id'),
        nullable=False,
        primary_key=True
    )

    def to_json(self):
        return {
            "user_id": self.user_id,
            "box_id": self.box_id,
        }

    def __repr__(self):
        return f"<UsersBoxes ({self.user_id} <> {self.box_id})>"
