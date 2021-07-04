from uuid import uuid4

from flask import request
from flask_restx import Resource
from sqlalchemy import exc

from app.api import categories_api
from app.helpers.api_response import ListCategoriesApiResponse, BaseApiResponse
from app.helpers.auth import require_admin, morph_admin
from app.helpers.boxes import upgrade_box_with_stats
from app.models.categories import Categories
import app.context as ctx


@categories_api.route('/list')
class List(Resource):

    @morph_admin
    def get(self, is_admin=False):
        res = ListCategoriesApiResponse()

        categories = ctx.db.session.query(Categories).all()
        if is_admin:
            res.set_categories(categories, with_boxes=True, with_flags=True)
        else:
            categories = list(filter(lambda cat: not cat.deleted, categories))
            res.set_categories(categories, public=True, with_boxes=True, with_flags=True)
            # Remove not released boxes
            for cat in res.categories:
                cat["boxes"] = list(filter(lambda b: b["released"], cat["boxes"]))

        for cat in res.categories:
            for box in cat["boxes"]:
                box = upgrade_box_with_stats(box)

        return res.make()


@categories_api.route('/get/<string:category_slug>')
class Get(Resource):

    def get(self, category_slug):
        res = BaseApiResponse()
        category = ctx.db.session.query(Categories).filter_by(slug=category_slug).first()

        if not category:
            res.add_error("Unknown category")
            return res.make(), 404

        res.data = category.to_json()

        return res.make()


@categories_api.route('/new')
class Create(Resource):

    @require_admin
    def post(self):
        res = BaseApiResponse()
        category = request.get_json()

        entry = Categories(id=uuid4(), name=category["name"], slug=category["slug"], description=category["description"], icon=category["icon"])

        try:
            ctx.db.session.add(entry)
            ctx.db.session.commit()
        except exc.IntegrityError:
            ctx.db.session.rollback()
            cat = Categories.query.filter_by(name=category["name"]).first()

            if cat and cat.deleted:
                res.add_error("A category with this name already exist but is deleted")
                return res.make(), 409
            elif cat:
                res.add_error("A category with this name already exist")
                return res.make(), 409

        return res.make(), 201


@categories_api.route('/delete')
class Delete(Resource):

    @require_admin
    def post(self):
        res = BaseApiResponse()
        category = request.get_json()

        cat = Categories.query.filter_by(id=category["id"]).first()
        if not cat:
            res.add_error("Category not found"), 404

        cat.deleted = True
        ctx.db.session.commit()

        return res.make()


@categories_api.route('/bulk_delete')
class BulkDelete(Resource):

    @require_admin
    def post(self):
        res = BaseApiResponse()
        categories = request.json

        to_update = []
        for cat in categories:
            to_update.append({"id": cat["id"], "deleted": True})

        try:
            ctx.db.session.bulk_update_mappings(Categories, to_update)
            ctx.db.session.commit()
            return res.make()

        except Exception as e:
            res.add_error(f"failed to delete categories in bulk : {str(e)}")
            return res.make(), 500


@categories_api.route('/restore')
class RestoreDeleted(Resource):

    @require_admin
    def post(self):
        res = BaseApiResponse()
        category = request.get_json()

        cat = Categories.query.filter_by(id=category["id"]).first()
        if not cat:
            res.add_error("Category not found")
            return res.make(), 404

        cat.deleted = False
        ctx.db.session.commit()

        return res.make()


@categories_api.route('/edit/<string:category_id>')
class Edit(Resource):

    @require_admin
    def post(self, category_id):
        res = BaseApiResponse()
        new_cat = request.get_json()

        old_cat = Categories.query.filter_by(id=category_id).first()
        if not old_cat:
            res.add_error("Category not found")
            return res.make(), 404

        old_cat.description = new_cat["description"]
        old_cat.icon = new_cat["icon"]
        old_cat.name = new_cat["name"]
        old_cat.slug = new_cat["slug"]

        ctx.db.session.commit()

        return res.make()
