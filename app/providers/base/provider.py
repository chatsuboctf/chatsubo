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
