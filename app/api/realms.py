# from pprint import pprint

from flask_restx import Resource

from app.api import realms_api
from app.helpers.api_response import ListRealmsApiResponse

import app.context as ctx
from app.models.boxes import Boxes


@realms_api.route('/all')
class List(Resource):

    def get(self):
        res = ListRealmsApiResponse()
        res.realms = ctx.providers.list_realms()

        return res.make()


@realms_api.route('/<string:box_id>')
class List(Resource):

    def get(self, box_id):
        res = ListRealmsApiResponse()
        box = ctx.db.session.query(Boxes).filter(Boxes.id == box_id).first()
        if not box:
            res.add_error("Unknown box")
            return res.make(), 404

        if box.kind == "dynamic":
            res.realms = ctx.providers.list_dynamic_realms()
        else:
            res.realms = ctx.providers.list_realms_of(box.template)

        return res.make()
