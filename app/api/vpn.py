from flask_restx import Resource

from app.api import vpn_api
from app.helpers.api_response import VpnAccessApiResponse

import app.context as ctx
from app.providers.exc import VpnProviderNotFoundException, VpnProviderErrorException


@vpn_api.route('/get/<string:realm>/<string:username>')
class List(Resource):

    def get(self, realm, username):
        res = VpnAccessApiResponse()
        if not ctx.providers.check_realm(realm):
            res.add_error("Unknown realm")
            return res.make(), 404

        try:
            res.config = ctx.vpns.get_vpn(realm, username)
        except VpnProviderNotFoundException as e:
            res.add_error(f"VPN provider not found for realm '{str(e)}'")
            return res.make(), 404
        except VpnProviderErrorException as e:
            res.add_error(f"Failed to get vpn config : '{str(e)}'")
            return res.make(), 500

        return res.make()
