"""Config.

Provides configuration for the application.
"""

import os
import sys
import logging
from dataclasses import dataclass

LOGGER = logging.getLogger()


@dataclass
class Config:
    modules_list: list
    provider: str
    namespace: str
    base_version: str
    token: str
    registry_name: str = "private"
    recreate: bool = False
    autobump_version: bool = False
