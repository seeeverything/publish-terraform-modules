import sys


class Log:
    @classmethod
    def info(self, message: str) -> None:
        print(f"::debug::{message}")

    @classmethod
    def debug(self, message: str) -> None:
        print(f"::debug::{message}")

    @classmethod
    def error(self, message: str) -> None:
        print(f"::error::{message}")
        sys.exit(1)

    @classmethod
    def warning(self, message: str) -> None:
        print(f"::warning::{message}")

    @classmethod
    def start_group(self, name: str) -> None:
        print(f"::group::{name}")

    @classmethod
    def end_group(self) -> None:
        print(f"::endgroup::")
