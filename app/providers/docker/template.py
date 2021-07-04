from app.providers.base.template import BaseTemplate


class DockerTemplate(BaseTemplate):
    def __init__(self, name, provider, labels, dockerfile="", dynamic=False):
        self.dockerfile = dockerfile

        super().__init__(name, provider, labels=labels, dynamic=dynamic)

    def to_json(self):
        data = self._to_json()

        data.update({
            "labels": self.labels,
            "dockerfile": self.dockerfile,
        })

        return data
