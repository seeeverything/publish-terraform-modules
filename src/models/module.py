class Module:
    def __init__(self, content):

        data = content["data"]

        self.id = data["id"]
        self.type = data["type"]
        self.name = data["attributes"]["name"]
        self.provider = data["attributes"]["provider"]
        self.namespace = data["attributes"]["namespace"]
        self.versions = data["attributes"]["version-statuses"]
        self.last_version = self._get_last_version(
            data["attributes"]["version-statuses"]
        )

        if "links" in data:
            self.links = data["links"]
        else:
            self.links = []

    def has_version(self, version):
        """Checks if a version exists"""

        for item in self.versions:
            if item["version"] == version:
                return True
        return False

    def _get_last_version(self, versions):
        if len(versions) > 0:
            active_versions = [
                version for version in versions if version["status"] == "ok"
            ]
            if len(active_versions) > 0:
                # TODO sort by version number
                return active_versions[0]["version"]
        return None
