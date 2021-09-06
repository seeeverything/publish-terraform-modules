class Version:
    def __init__(self, content):

        data = content["data"]

        self.id = data["id"]
        self.type = data["type"]
        self.source = data["attributes"]["source"]
        self.status = data["attributes"]["status"]
        self.version = data["attributes"]["version"]

        if "links" in data:
            self.links = data["links"]
        else:
            self.links = []
