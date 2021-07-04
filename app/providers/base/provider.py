from app.providers.exc import VpnProviderNotFoundException


class BaseProvider:
    name = "MISSING"
    is_dynamic = False

    def __init__(self, realms, vpn_providers, kind="MISSING"):
        self.kind = kind
        self.vpns = {}
        self.register_vpns(realms, vpn_providers)

    def register_vpns(self, realms, vpn_providers):
        for realm in realms:
            try:
                self.vpns[realm] = vpn_providers.get_by_realm(realm)
            except VpnProviderNotFoundException:
                print(f"Failed to find a VPN provider for realm '{realm}'")
    #
    # def register_vpn(self, conf):
    #     default_endpoints = {
    #         "config": "/api/vpn/get/:username",
    #         "check": "/api/check"
    #     }
    #
    #     try:
    #         if raw_endpoints := conf.get("endpoints"):
    #             endpoints = {
    #                 "config": raw_endpoints.get("config", "/api/vpn/get/:username"),
    #                 "check": raw_endpoints.get("check", "/api/check")
    #             }
    #         else:
    #             endpoints = default_endpoints
    #
    #         parsed = {
    #             "endpoints": endpoints,
    #             "realm": conf.get("realm"),
    #             "url": conf.get("url"),
    #             "token": conf.get("token"),
    #             "header": conf.get("header", "X-Chatsubo-Token")
    #         }
    #
    #         for key, val in parsed.items():
    #             if not val:
    #                 raise MissingVPNConfigException(key)
    #
    #         self.vpns.append(VpnProvider(**parsed))
    #         self.vpns[parsed["realm"]] = VpnProvider(**parsed)
    #     except Exception as e:
    #         raise BackendConnectionException(f"{self.kind}/{self.name}", str(e))

    # def register_session(self, session):
    #     self.sessions.append(session)
    #
    # def remove_session(self, session):
    #     self.sessions.pop(session)

    def list_templates(self):
        return []

    def start_dynamic_instance(self, realm, template, session_id):
        return None

    def stop_dynamic_instance(self, session):
        return None

    def _list_realms(self):
        instances = self.list_instances()
        realms = set()

        for inst in instances:
            realms.add(inst.realm)

        return list(realms)

    def list_realms(self):
        return self._list_realms()

    def list_instances(self, realm=None):
        return []

    # def get_vpn_for(self, realm, username):
    #     realm_vpn_pv = next((vpn for vpn in self.vpns if vpn.realm == realm), None)
    #     if not realm_vpn_pv:
    #         raise VpnProviderNotFoundException(realm)
    #
    #     try:
    #         config = realm_vpn_pv.get_config(username)
    #     except VpnProviderErrorException:
    #         raise
    #
    #     return config

    # def get_vpn_for(self, realm, username):
    #     if not (realm_vpn_pv := self.vpns.get(realm)):
    #         raise VpnProviderNotFoundException(realm)
    #
    #     try:
    #         config = realm_vpn_pv.get_config(username)
    #     except VpnProviderErrorException:
    #         raise
    #
    #     return config

    def reset(self, realm, box):
        pass

    def to_json(self, with_vpns=True):
        data = {
            "name": self.name,
            "kind": self.kind,
            "is_dynamic": self.is_dynamic,
            "vpns": self.vpns
        }

        if not with_vpns:
            del data["vpns"]

        return data
