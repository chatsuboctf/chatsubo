import hashlib

import docker
import urllib3
from docker.errors import DockerException
from dockerfile_parse import DockerfileParser

from app.helpers.rand import randstr
from app.providers.base.provider import BaseProvider
from app.providers.docker.instance import DockerInstance
from os import path, walk

from app.providers.docker.template import DockerTemplate
from app.providers.exc import BackendConnectionException, MetadataNotFoundException


class DockerProvider(BaseProvider):
    kind = "docker"
    is_dynamic = True

    def __init__(self, name, host, port, client_cert, client_key, ca, dockerfile_root, mem_limit, docker_network, flag_prefix, realms, vpns):

        self.name = name
        self.host = host
        self.port = port
        self.client_cert = client_cert
        self.client_key = client_key
        self.ca = ca
        self.dockerfile_root = dockerfile_root
        self.mem_limit = mem_limit
        self.docker_network = docker_network
        self.flag_prefix = flag_prefix

        try:
            self.client = self.init_client()
        except DockerException as e:
            raise BackendConnectionException(f"{self.kind}/{self.name}", str(e))

        super().__init__(vpn_providers=vpns, kind=self.kind, realms=realms)

    def init_client(self):
        tls_config = docker.tls.TLSConfig(
            client_cert=(self.client_cert, self.client_key),
            verify=self.ca
        )

        return docker.DockerClient(base_url=f"{self.host}:{self.port}", tls=tls_config)

    def list_templates(self):
        templates = []
        # images = self.client.images.list()
        # configs = [img.attrs for img in images if img.labels.get("chatsubo.template")]
        # for config in configs:
        #     templates.append(
        #         DockerTemplate(
        #             config["Config"]["Labels"]["chatsubo.template"],
        #             self.to_json(with_vpns=False),
        #             config["Config"]["Labels"],
        #         ).to_json()
        #     )

        templates.extend([tpl.to_json() for tpl in self.list_dynamic_templates()])

        return templates

    def list_dynamic_templates(self):
        templates = []
        dirnames = []

        try:
            _, dirnames, _ = next(walk(self.dockerfile_root))
        except StopIteration:
            pass

        for template in dirnames:
            dfp = DockerfileParser(path=path.join(self.dockerfile_root, template))
            templates.append(
                DockerTemplate(
                    template,
                    self.to_json(with_vpns=False),
                    dfp.labels,
                    dockerfile=dfp.content,
                    dynamic=True
                )
            )

        return templates

    def list_realms(self):
        realms = self._list_realms()
        realms += [vpn.realm for vpn in self.vpns.values()]

        return realms

    def list_instances(self, realm=None):
        instances = []
        containers = [c.attrs for c in self.client.containers.list() if c.labels.get("chatsubo.template")]

        for c in containers:
            params = {
                "id": c["Id"],
                "meta": c
            }
            try:
                instances.append(DockerInstance(**params))
            except MetadataNotFoundException as e:
                print(e)
                continue

        if realm:
            instances = list(filter(lambda i: i.realm == realm, instances))

        return instances

    def stop_dynamic_instance(self, session_id):
        try:
            container = self.client.containers.get(session_id)
            container.kill()
        except Exception as e:
            print(e)

        # container.remove(force=True)

    def start_dynamic_instance(self, realm, template, session_id):
        # session_id = str(uuid4())
        tag = hashlib.sha1(session_id.encode('utf-8')).hexdigest()
        dockerfile_dir = path.join(self.dockerfile_root, template)
        build_params = {
            "path": dockerfile_dir,
            "dockerfile": path.join(dockerfile_dir, "Dockerfile"),
            "buildargs": {
                "SESSION": session_id,
            },
            "tag": tag,
        }

        for i in range(50):
            build_params["buildargs"][f"FLAG{str(i)}"] = f"{self.flag_prefix}{{{hashlib.sha1(randstr(32).encode('utf-8')).hexdigest()[:35]}}}"
            build_params["buildargs"][f"RNG{str(i)}"] = randstr(8)

        while True:
            try:
                self.client.images.build(**build_params)
            except urllib3.exceptions.SSLError:
                continue
            break

        ports = {}
        dfp = DockerfileParser(path=dockerfile_dir)
        for host_port, container_port in {label: val for label, val in dfp.labels.items() if label.startswith("chatsubo.port")}.items():
            trimed = host_port.replace("chatsubo.port.", "")
            ports[trimed] = container_port

        run_params = {
            "image": tag,
            "ports": ports,
            "detach": True,
            "remove": True,
            "network": self.docker_network,
            "name": session_id,
            "labels": {
                "chatsubo.realm": realm
            },
            "mem_limit": self.mem_limit,
        }

        try:
            self.client.containers.run(**run_params)
        except (docker.errors.ContainerError, docker.errors.ImageNotFound, docker.errors.APIError) as e:
            return str(e)

        return None

    def reset(self, realm, template, session=None):
        container = None
        if session:
            container = self.client.containers.get(session.id)
        else:
            instances = self.list_instances(realm=realm)
            for inst in instances:
                if inst.template == template:
                    container = self.client.containers.get(inst.id)
        if not container:
            return False

        container.restart()
        return True

    @classmethod
    def from_config(cls, name, raw_conf, vpns):
        defaults = {
            "docker_network": "chatsubo-gate",
            "flag_prefix": "FLAG"
        }

        parsed = {
            "name": name,
            "host": raw_conf["api"]["host"],
            "port": raw_conf["api"]["port"],
            "client_cert": raw_conf["api"]["client"]["cert"],
            "client_key": raw_conf["api"]["client"]["key"],
            "ca": raw_conf["api"]["client"]["ca"],
            "dockerfile_root": raw_conf["dynamic"]["local_dockerfile_root"],
            "docker_network": raw_conf.get("docker_network", defaults["docker_network"]),
            "flag_prefix": raw_conf.get("flag_prefix", defaults["flag_prefix"]),
            "mem_limit": raw_conf["limits"]["memory"],
            "realms": raw_conf["realms"],
            "vpns": vpns
        }

        return cls(**parsed)
