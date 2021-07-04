# from pprint import pprint
from docker.errors import BuildError
from urllib3.exceptions import MaxRetryError

from app.providers.docker.provider import DockerProvider
from app.providers.exc import MissingProviderConfigException, VpnProviderErrorException, BackendConnectionException
from app.providers.pve.provider import PVEProvider

# from traceback import print_tb


class Providers:
    providers = {}

    def register(self, pv):
        # pv.check()
        self.providers[pv.name] = pv

    def all(self):
        return self.providers.values()

    def get_providers(self):
        return self.providers.values()

    def list_instances(self):
        instances = []

        for pv in self.providers.values():
            instances += pv.list_instances()

        return instances

    def list_instances_of(self, realm, template=None):
        filtered = []
        providers = self.get_providers_of_realm(realm)

        if not providers:
            return []

        instances = []

        for pv in providers:
            instances += pv.list_instances()

        for inst in instances:
            if inst.realm.lower() == realm.lower():
                if template:
                    if inst.template.lower() == template.lower():
                        filtered.append(inst)
                else:
                    filtered.append(inst)

        return filtered

    def list_templates(self):
        templates = []

        for pv in self.get_providers():
            parsed = []
            try:
                pv_templates = pv.list_templates()
            except BackendConnectionException:
                continue
            for tpl in pv_templates:
                parsed.append({"data": tpl})

            templates += parsed

        return templates

    def list_realms(self):
        realms = []

        for pv in self.get_providers():
            realms += [{"name": realm, "provider": {"name": pv.name, "kind": pv.kind}} for realm in pv.list_realms()]

        return realms

    def list_dynamic_realms(self):
        realms = []
        for pv in filter(lambda p: p.is_dynamic, self.get_providers()):
            realms += pv.list_realms()

        return realms

    def list_realms_of(self, box_template):
        instances = self.list_instances()
        filtered_instances = list(filter(lambda i: i.template.lower() == box_template.lower(), instances))
        realms = set()
        for inst in filtered_instances:
            realms.add(inst.realm)

        return list(realms)

    # def get_provider_of_realm(self, realm_target):
    #     pv = None
    #     realms = self.list_realms()
    #     for realm in realms:
    #         if realm_target == realm["name"]:
    #             pv = self.get_provider_by_name(realm["provider"]["name"])
    #             break
    #
    #     return pv

    def get_providers_of_realm(self, realm_target, only_dynamic=False):
        providers = []
        realms = self.list_realms()
        for realm in realms:
            if realm_target == realm["name"]:
                pv = self.get_provider_by_name(realm["provider"]["name"])
                if only_dynamic:
                    if pv.is_dynamic:
                        providers.append(pv)
                else:
                    providers.append(pv)

        return providers

    def get_provider_for(self, realm, template):
        providers = self.get_providers_of_realm(realm)
        providers_w_template = (pv for pv in providers if template in [template["name"] for template in pv.list_templates()])
        pv = None

        try:
            pv = next(providers_w_template, None)
        except StopIteration:
            pass

        return pv

    def get_provider_by_name(self, name):
        pvs = self.get_providers()
        for pv in pvs:
            if pv.name == name:
                return pv

    def reset_box(self, realm, template, session=None):
        pv = self.get_provider_for(realm, template)

        try:
            return pv.reset(realm, template, session=session)
        except:
            import traceback
            print(traceback.format_exc())
            return False

    def start_dynamic_instance(self, realm, template, session_id):
        pv = self.get_provider_for(realm, template)

        if not pv:
            return False

        try:
            return pv.start_dynamic_instance(realm, template, session_id)
        except BuildError:
            return False
        except:
            import traceback
            print(traceback.format_exc())
            return False

    def stop_dynamic_instance(self, realm, session_id):
        found = None
        providers = self.get_providers_of_realm(realm, only_dynamic=True)
        # [provider for provider in providers if provider.is_dynamic]
        for pv in list(filter(lambda p: p.is_dynamic, providers)):
            if session_id in [inst.session for inst in pv.list_instances()]:
                found = pv
                break

        if not found:
            print(f"Provider not found for instance '{realm}/{session_id}'")
            return False

        try:
            return found.stop_dynamic_instance(session_id)
        except:
            import traceback
            print(traceback.format_exc())
            return False

    def check_realm(self, realm):
        return any(realm == r["name"] for r in self.list_realms())

    def get_instances_of(self, realm, template, session=None):
        instances = self.list_instances_of(realm, template=template)
        filtered = list(filter(lambda x: x.template == template, instances))
        if session:
            filtered = list(filter(lambda x: x.session == session, filtered))

        return filtered

    def get_address_of(self, realm, template, session=None):
        instances = self.get_instances_of(realm, template, session)
        return instances[0].address if instances else None

    def get_creds_of(self, realm, template, session=None):
        instances = self.get_instances_of(realm, template, session)
        return instances[0].creds if instances else None

    def get_flags_of(self, realm, template, session=None):
        instances = self.get_instances_of(realm, template, session)
        # pprint(instances[0].to_json())
        return instances[0].flags if instances else None

    def get_flag(self, realm, template, name):
        flags = self.get_flags_of(realm, template)
        flag = ""

        try:
            flag = next((flag for flag in flags if flag.name == name), None)
        except StopIteration:
            pass

        return flag

    def load(self, pvs_config, vpns):
        # Register additional providers here
        providers_mapping = {
            "pve": PVEProvider,
            "docker": DockerProvider
        }

        for pv_kind in providers_mapping.keys():
            if pvs_configs := pvs_config.get(pv_kind):
                for name, conf in pvs_configs.items():
                    if not conf:
                        raise MissingProviderConfigException(pv_kind)

                    provider = providers_mapping[pv_kind]
                    pv = provider.from_config(name, conf, vpns)
                    self.register(pv)
