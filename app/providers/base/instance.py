from app.providers.exc import MetadataNotFoundException, MalformedMetadataException


class BaseInstance:
    def __init__(self, id, name, realm, template, address, flags=None, creds=None):
        if flags is None:
            flags = []

        self.id = id
        self.name = name
        self.realm = realm
        self.template = template
        self.address = address
        # self.sep = sep
        self.flags = flags
        self.creds = creds

    def _to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "realm": self.realm,
            "template": self.template,
            "address": self.address,
            "flags": self.flags,
            "creds": self.creds,
            # "sep": self.sep,
        }

    def to_json(self):
        return self._to_json()
