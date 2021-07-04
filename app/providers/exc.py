class MissingProviderConfigException(Exception):
    pass


class MissingVPNConfigException(Exception):
    def __init__(self, key):
        super(MissingVPNConfigException, self).__init__(f"missing VPN config : '{key}'")


class MetadataNotFoundException(Exception):
    pass


class MalformedMetadataException(Exception):
    pass


class MissingBoxException(Exception):
    pass


class VpnProviderNotFoundException(Exception):
    pass


class VpnProviderErrorException(Exception):
    pass


class BackendConnectionException(Exception):
    def __init__(self, pv_name="", error=""):
        super(BackendConnectionException, self).__init__(error)
        self.pv_name = pv_name
        self.error = error
