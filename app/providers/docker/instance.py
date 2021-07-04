from app.providers.exc import MetadataNotFoundException, MalformedMetadataException
from app.providers.base.instance import BaseInstance
from app.providers.labels import parse_flags, parse_creds


class DockerInstance(BaseInstance):
    def __init__(self, id, meta):
        try:
            session, template, realm, address, flags, creds = self.parse_meta(meta)
        except (MetadataNotFoundException, MalformedMetadataException):
            raise

        self.session = session

        super(DockerInstance, self).__init__(id, meta["Id"], realm, template, address, flags=flags, creds=creds)

    def parse_meta(self, meta):
        """
        Parse and extract the template, realm, flags, foothold creds and IP address from the metadata field of the instance

        Args:
            raw (str): string holding the metadata info
        Returns:
            Returns the template name, the realm holding this instance and its IP address
        """

        labels = meta["Config"]["Labels"]
        flags = parse_flags(labels)
        creds = parse_creds(labels)
        template = labels.get("chatsubo.template")
        session = labels.get("chatsubo.session")
        realm = labels.get("chatsubo.realm")
        for label in ["template", "session", "realm"]:
            if not label:
                raise MetadataNotFoundException(f"Missing metadata : 'template={template}', session='{session}', realm='{realm}'")

        network = meta["NetworkSettings"]["Networks"].get("chatsubo-gate", None)
        if not network:
            raise MetadataNotFoundException("NetworkSettings for Networks['chatsubo-gate']")

        address = network.get("IPAddress")
        if not network:
            raise MetadataNotFoundException("IPAddress")

        return session, template, realm, address, flags, creds
