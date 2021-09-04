class Module:
    def __init__(self) -> None:
        self.id = None

    def __init__(self, data):
        self.id = data["id"]
        self.type = data["type"]
        self.name = data["attributes"]["name"]
        self.provider = data["attributes"]["provider"]
        self.namespace = data["attributes"]["namespace"]
        self.status = data["attributes"]["version-statuses"][0]["status"]
        self.version = data["attributes"]["version-statuses"][0]["version"]
