from sqlalchemy import func

import app.context


class Sessions(app.context.db.Model):
    __tablename__ = "sessions"

    id = app.context.db.Column(
        app.context.db.String(36),
        nullable=False,
        primary_key=True
    )

    task_id = app.context.db.Column(
        app.context.db.String(36),
    )

    box_id = app.context.db.Column(
        app.context.db.String(36),
        app.context.db.ForeignKey('boxes.id'),
        nullable=False,
    )

    user_id = app.context.db.Column(
        app.context.db.String(36),
        app.context.db.ForeignKey('users.id'),
        nullable=False,
    )

    realm = app.context.db.Column(
        app.context.db.String(200),
        nullable=False,
    )

    state = app.context.db.Column(
        app.context.db.String(200),
        nullable=False,
    )

    started_at = app.context.db.Column(
        app.context.db.DateTime,
        index=False,
    )

    expires_at = app.context.db.Column(
        app.context.db.DateTime,
        index=False,
        default=0
    )

    def to_json(self, public=True, with_deleted_flags=False, filter_passwd=True, with_created_boxes=True, with_flags=True):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "box_id": self.box_id,
            "user_id": self.user_id,
            "owner": self.owner.to_json(filter_passwd=filter_passwd, with_created_boxes=with_created_boxes),
            "box": self.box.to_json(public=public, with_flags=with_flags, with_deleted_flags=with_deleted_flags),
            "realm": self.realm,
            "state": self.state,
            "started_at": str(self.started_at),
            "expires_at": str(self.expires_at)
        }

    def __repr__(self):
        return f"<Sessions ({self.user_id} <> {self.box_id})>"
