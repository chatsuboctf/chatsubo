from urllib.parse import urljoin

import requests

from app.providers.exc import VpnProviderErrorException, MissingVPNConfigException, BackendConnectionException


class VpnProvider:
    def __init__(self, realm, url, token, endpoints, header):
        self.realm = realm
        self.url = url
        self.token = token
        self.header = header
        self.endpoints = endpoints

        self.check()

    def check(self):
        headers = {
            self.header: self.token
        }

        res = requests.get(
            urljoin(self.url, self.endpoints['check']),
            headers=headers
        )

        data = res.json()
        if errs := data.get("errors", []):
            raise VpnProviderErrorException(errs)

    def get_config(self, username):
        headers = {
            self.header: self.token
        }

        res = requests.get(
            urljoin(self.url, self.endpoints['config'].replace(':username', username)),
            headers=headers
        )

        data = res.json()
        if errs := data.get("errors", []):
            raise VpnProviderErrorException(errs)

        return data.get("config", None)

    @classmethod
    def from_config(cls, conf):
        default_endpoints = {
            "config": "/api/vpn/get/:username",
            "check": "/api/check"
        }

        try:
            if raw_endpoints := conf.get("endpoints"):
                endpoints = {
                    "config": raw_endpoints.get("config", "/api/vpn/get/:username"),
                    "check": raw_endpoints.get("check", "/api/check")
                }
            else:
                endpoints = default_endpoints

            parsed = {
                "endpoints": endpoints,
                "realm": conf.get("realm"),
                "url": conf.get("url"),
                "token": conf.get("token"),
                "header": conf.get("header", "X-Chatsubo-Token")
            }

            for key, val in parsed.items():
                if not val:
                    raise MissingVPNConfigException(key)

            return cls(**parsed)
        except Exception as e:
            raise VpnProviderErrorException(f"{conf.get('realm')}", str(e))
