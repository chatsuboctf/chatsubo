import re
import traceback

import requests
from proxmoxer import ProxmoxAPI
from urllib3.exceptions import MaxRetryError

from app.providers.base.provider import BaseProvider
from app.providers.base.template import BaseTemplate
from app.providers.exc import VpnProviderNotFoundException, \
    VpnProviderErrorException, BackendConnectionException, MetadataNotFoundException, MalformedMetadataException
from app.providers.pve.instance import PVEInstance


class PVEProvider(BaseProvider):
    kind = "pve"
    is_dynamic = False

    def __init__(self, name, host, user, token_name, token_value, realms, vpns, nodes=None, verify_ssl=False, sep="--"):
        if nodes is None:
            nodes = ["pve"]

        self.name = name
        # self.prefix = prefix
        self.nodes = nodes
        # self.reset_snapshot_name = reset_snapshot_name
        self.sep = sep
        self.client = ProxmoxAPI(host,
                                 user=user,
                                 token_name=token_name,
                                 token_value=token_value,
                                 verify_ssl=verify_ssl
                                 )
        remote_nodes = [node_data["node"] for node_data in self.client.nodes.get()]
        for node in self.nodes:
            if node not in remote_nodes:
                raise BackendConnectionException(f"{self.kind}/{self.name}", f"Node '{node}' not found")

        super().__init__(vpn_providers=vpns, kind=self.kind, realms=realms)

    # def test_client(self):
    #     nodes = self.client.nodes.get()
    #     for node in nodes:
    #         self.client.nodes(node["node"]).status.get()

    def list_templates(self):
        templates = []
        vms = self.list_all()

        try:
            # filtered = list(filter(lambda vm: "chatsubo." in vm["description"] and vm["template"] == 1, vms))
            filtered = list(filter(lambda vm: "chatsubo." in vm["description"], vms))
            rg = re.compile("(chatsubo\..*)=(.*)", re.MULTILINE)

            for config in filtered:
                labels = {}
                matches = rg.findall(config["description"])
                for match in matches:
                    labels[match[0]] = match[1]

                if not (name := labels.get("chatsubo.template")):
                    continue

                templates.append(BaseTemplate(name, self.to_json(), labels=labels).to_json())
        except Exception:
            raise

        return templates

    def list_all(self):
        vms = []
        for node in self.nodes:
            try:
                instances = self.client.nodes(node).qemu.get()
            except (MaxRetryError, requests.exceptions.ConnectionError, ConnectionRefusedError) as e:
                raise BackendConnectionException(f"{self.kind}/{self.name}", str(e))

            for inst in instances:
                inst["description"] = self.client.nodes(node).qemu(inst["vmid"]).config.get().get("description", "")
                inst["node"] = node

            vms += instances

        return vms

    def list_instances(self, realm=None):
        instances = []
        vms = self.list_all()
        raw = list(filter(lambda vm: "chatsubo." in vm["description"] and vm["template"] == "", vms))

        for vm in raw:
            try:
                # instances.append(PVEInstance(vm["vmid"], vm["name"], self.prefix, vm["description"], vm["node"], self.sep))
                instances.append(PVEInstance(vm["vmid"], vm["name"], vm["description"], vm["node"]))
            except (MetadataNotFoundException, MalformedMetadataException):
                pass

        if realm:
            instances = list(filter(lambda i: i.realm == realm, instances))

        return instances

    def reset(self, realm, template, session=None):
        target = None
        instances = self.list_instances(realm=realm)
        for inst in instances:
            if inst.template == template:
                target = inst

        snapshots = self.client.nodes(target.node).qemu.get(f"{target.id}/snapshot")
        last_snap_name = list(filter(lambda x: x.get("running") == 1, snapshots))[0].get("parent")

        if not last_snap_name:
            return False

        self.client.nodes(target.node).qemu.post(f"{target.id}/snapshot/{last_snap_name}/rollback")
        return True

    @classmethod
    def from_config(cls, name, raw_conf, vpns):
        # def __init__(self, host, user, token_name, token_value, prefix, nodes=None, verify_ssl=False, sep="--"):
        parsed = {
            "name": name,
            # "prefix": raw_conf["prefix"],
            # "reset_snapshot_name": raw_conf["reset_snapshot_name"],
            "host": f"{raw_conf['api']['host']}:{raw_conf['api']['port']}",
            "user": raw_conf["api"]["user"],
            "token_name": raw_conf["api"]["token"]["name"],
            "token_value": raw_conf["api"]["token"]["value"],
            "realms": raw_conf["realms"],
            "vpns": vpns
        }

        if nodes := raw_conf.get("nodes"):
            parsed["nodes"] = nodes

        if verif := raw_conf.get("verify_ssl"):
            parsed["verify_ssl"] = verif

        if sep := raw_conf.get("sep"):
            parsed["sep"] = sep

        return cls(**parsed)
