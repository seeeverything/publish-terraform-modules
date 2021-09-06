class SemVer:
    major: int
    minor: int
    patch: int

    def __init__(self, version: str) -> None:
        self._parse_version(version)

    @classmethod
    def load(self, major: int, minor: int, patch: int) -> None:
        return SemVer(f"{major}.{minor}.{patch}")

    def _parse_version(self, version: str):
        parts = version.split(".")
        self.major = int(parts[0])
        self.minor = int(parts[1])
        self.patch = int(parts[2])

    def to_string(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def bump_major(self) -> str:
        self.major += 1
        self.minor = 0
        self.patch = 0
        
        return self.to_string()

    def bump_major(self) -> str:
        self.minor += 1
        self.patch = 0

        return self.to_string()

    def bump_patch(self) -> str:
        self.patch += 1

        return self.to_string()
