import re

from app.providers.exc import MetadataNotFoundException, MalformedMetadataException
from app.providers.base.instance import BaseInstance
from app.providers.labels import parse_flags, parse_creds


class PVEInstance(BaseInstance):
    def __init__(self, id, name, description, node="pve"):
        self.node = node

        try:
            template, realm, address, flags, creds = self.parse_meta(description)
        except (MetadataNotFoundException, MalformedMetadataException):
            raise

        super(PVEInstance, self).__init__(id, name, realm, template, address, flags=flags, creds=creds)

    def parse_meta(self, raw):
        """
        Parse and extract the template, realm, flags, foothold creds and IP address from the metadata field of the instance

        Args:
            raw (str): string holding the metadata info
        Returns:
            Returns the template name, the realm holding this instance and its IP address
        """

        raw = raw.lower()

        if not any(f"chatsubo.{key}" in raw for key in ["template", "realm", "address"]):
            raise MalformedMetadataException

        labels = {}
        rg = re.compile("(chatsubo\..*)=(.*)", re.MULTILINE)
        matches = rg.findall(raw)
        for match in matches:
            labels[match[0]] = match[1]

        template = labels.get("chatsubo.template")
        realm = labels.get("chatsubo.realm")
        address = labels.get("chatsubo.address")
        creds = parse_creds(labels)
        flags = parse_flags(labels)

        return template, realm, address, flags, creds

    def to_json(self):
        data = self._to_json()
        data.update({
            "node": self.node,
        })

        return data
