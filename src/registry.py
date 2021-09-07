import os
import requests
import json

from requests.models import Response
from models.module import Module
from models.version import Version

from log import Log

TERRAFORM_REGISTRY = os.getenv(
    "TERRAFORM_REGISTRY", "https://app.terraform.io/api/v2/organizations"
)


class Registry:
    def __init__(self, organization: str, token: str) -> None:
        self.organization = organization
        self.endpoint = f"{TERRAFORM_REGISTRY}/{organization}/registry-modules"
        self.token = token

    def _parse_response(self, response: Response) -> bool:
        if response.status_code == 404:
            Log.warning("Not found or user unauthorized to perform action")
        elif response.status_code == 403:
            Log.error("Forbidden - public module curation disabled")
        elif response.status_code == 401:
            Log.error("Unauthorized - you can't perform this action")
        elif response.status_code in [200, 201, 204]:
            return True

        Log.debug(response.status_code)
        Log.debug(response.content)

        return False

    def module_exists(self, name: str, provider: str) -> bool:
        """Checks if a module exists in the registry"""
        if self.get_module(name, provider) is None:
            return False

        return True

    def get_module(self, name: str, provider: str) -> Module:
        """GET a Module"""

        url = f"{self.endpoint}/private/{self.organization}/{name}/{provider}"

        response = requests.get(
            url=url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "Authorization": f"Bearer {self.token}",
            },
        )

        sucess = self._parse_response(response)
        if sucess:
            return Module(json.loads(response.content))
        else:
            return None

    def create_module(self, name: str, provider: str, registry_name: str) -> Module:
        """Creates a new registry module without a backing VCS repository"""

        url = f"{self.endpoint}"

        payload = {
            "data": {
                "type": "registry-modules",
                "attributes": {
                    "name": name,
                    "provider": provider,
                    "registry-name": registry_name,
                },
            }
        }

        response = requests.post(
            url=url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "Authorization": f"Bearer {self.token}",
            },
            data=json.dumps(payload),
        )

        sucess = self._parse_response(response)

        if sucess:
            return Module(json.loads(response.content))
        else:
            return None

    def create_version(self, name: str, provider: str, version: str) -> Version:
        """Creates a new module version"""

        url = f"{self.endpoint}/private/{self.organization}/{name}/{provider}/versions"

        payload = {
            "data": {
                "type": "registry-module-versions",
                "attributes": {"version": version},
            }
        }

        response = requests.post(
            url=url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "Authorization": f"Bearer {self.token}",
            },
            data=json.dumps(payload),
        )

        sucess = self._parse_response(response)
        if sucess:
            Log.debug(f"Module version {version} has been created")
            return Version(json.loads(response.content))
        else:
            return None

    def upload_version(self, upload_link: str, tar_ball: str) -> bool:
        """Uploads a module version"""

        url = upload_link

        with open(tar_ball, "rb") as f:
            module_data = f.read()

        response = requests.put(
            url=url,
            headers={"Content-Type": "application/octet-stream"},
            data=module_data,
        )

        success = self._parse_response(response)

        if success:
            Log.debug("Module has been uploaded")

        return success

    def delete_version(self, name: str, provider: str, version: str) -> bool:
        """Deletes a module version"""

        url = f"{self.endpoint}/private/{self.organization}/{name}/{provider}/{version}"

        response = requests.delete(
            url=url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "Authorization": f"Bearer {self.token}",
            },
        )

        success = self._parse_response(response)
        if success:
            Log.debug("Module version has been deleted")

        return success
