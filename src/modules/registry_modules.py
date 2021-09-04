import sys
from typing import NamedTuple
import requests
import json

from types import SimpleNamespace
from models.module import Module

TERRAFORM_REGISTRY = "https://app.terraform.io/api/v2/organizations"


class RegistryModules:
    def __init__(self, organization, token) -> None:
        self.organization = organization
        self.endpoint = f"{TERRAFORM_REGISTRY}/{organization}/registry-modules"
        self.token = token

    def _parse_response(self, response):
        if response.status_code == 404:
            print(f"Not found or user unauthorized to perform action")
        elif response.status_code == 403:
            print(f"Forbidden - public module curation disabled")
        elif response.status_code == 401:
            print(f"Unauthorized - you can't perform this action")
        elif response.status_code == 200:
            print(f"The request was successful")
            return True
        else:
            print("Oops something bad happened")
            print(response.content)

        return False

    def get(self, name, provider):
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
            return Module(json.loads(response.content)["data"])
        else:
            return None

    def create(self, name, provider):
        """Create a Module"""

    def create_version(self, name, provider, version, tar_ball):
        """Uploads a new version"""
