from flask_restx import Resource

from app.api import providers_api
from app.helpers.api_response import ListProvidersApiResponse

import app.context as ctx


@providers_api.route('/list')
class List(Resource):

    def get(self):
        res = ListProvidersApiResponse()
        res.set_providers(ctx.providers.get_providers())

        return res.make()
