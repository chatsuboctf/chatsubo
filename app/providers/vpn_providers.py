from app.providers.base.vpn import VpnProvider
from app.providers.exc import VpnProviderNotFoundException


class VpnProviders:
    vpns = {}

    def register(self, vpn):
        self.vpns[vpn.realm] = vpn

    def all(self):
        return self.vpns.values()

    # def get_vpns(self):
    #     return self.vpns.values()
    #
    def get_vpn(self, realm, username):
        if not (vpn := self.vpns.get(realm)):
            raise VpnProviderNotFoundException

        return vpn.get_config(username)

    def get_by_realm(self, realm):
        if not (vpn := self.vpns.get(realm)):
            raise VpnProviderNotFoundException

        return vpn

    def load(self, vpn_configs):
        for conf in vpn_configs:
            vpn = VpnProvider.from_config(conf)
            self.register(vpn)
