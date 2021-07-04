from sqlalchemy.orm import relationship


import app.context


class Categories(app.context.db.Model):
    __tablename__ = "categories"

    id = app.context.db.Column(
        app.context.db.String(36),
        primary_key=True,
    )

    name = app.context.db.Column(
        app.context.db.String(200),
        nullable=False,
        unique=True
    )

    slug = app.context.db.Column(
        app.context.db.String(200),
        nullable=False,
        unique=True
    )

    description = app.context.db.Column(
        app.context.db.Text
    )

    icon = app.context.db.Column(
        app.context.db.String(70)
    )

    deleted = app.context.db.Column(
        app.context.db.Boolean,
        default=False
    )

    updated = app.context.db.Column(
        app.context.db.DateTime,
        server_onupdate=app.context.db.func.current_timestamp()
    )

    created = app.context.db.Column(
        app.context.db.DateTime,
        server_default=app.context.db.func.current_timestamp(),
        nullable=False
    )

    boxes = relationship("Boxes", backref="category")

    def __repr__(self):
        return f"<Categories {self.name}>"

    def to_json(self, with_deleted_boxes=False, with_boxes=False, with_unreleased=False, public=True, with_flags=False, with_deleted_flags=False):
        data = {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "icon": self.icon,
            "deleted": self.deleted,
            "updated": None if not self.updated else self.updated.isoformat(),
            "created": self.created.isoformat(),
            "boxes": []
        }

        if self.boxes and with_boxes:
            for box in self.boxes:
                if (not box.deleted or with_deleted_boxes) \
                   and (with_unreleased or with_unreleased != box.released):
                    data["boxes"].append(box.to_json(public, with_flags, with_deleted_flags))

        return data
