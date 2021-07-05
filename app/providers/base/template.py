from app.providers.labels import parse_flags, parse_creds


class BaseTemplate:
    def __init__(self, name, provider, labels=None, dynamic=False):
        if labels is None:
            labels = []

        self.provider = provider
        self.name = name
        self.dynamic = dynamic
        self.flags = parse_flags(labels)
        self.creds = parse_creds(labels)
        self.labels = labels

    def to_json(self):
        return self._to_json()

    def _to_json(self):
        return {
            "provider": self.provider,
            "name": self.name,
            "flags": self.flags,
            "creds": self.creds,
            "labels": self.labels,
            "dynamic": self.dynamic,
        }
