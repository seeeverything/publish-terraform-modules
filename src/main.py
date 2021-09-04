import os
import sys
import tarfile
from typing import List
from modules.registry_modules import RegistryModules


def package_module(module_name: str, module_dir: str) -> str:

    file_name = f"{module_name}.tar.gz"

    with tarfile.open(file_name, "w:gz") as tar:
        tar.add(module_dir, arcname=os.path.sep)

    return file_name


def main(args: List) -> str:

    modules_path = args[1]
    provider = args[2]
    namespace = args[3]
    registry_name = args[4]
    token = args[5]
    workdir = os.getenv("GITHUB_WORKSPACE")

    registry = RegistryModules(namespace, token)

    for module_name in os.listdir(modules_path):

        module = registry.get(module_name, provider)

        if module is None:
            print("The module selected does not exists")
            registry.create(module_name, provider)

        module = registry.get(module_name, provider)
        tar_ball = package_module(module_name, os.path.join(modules_path, module_name))
        registry.create_version(module.name, module.provider, module.version, tar_ball)

        os.remove(tar_ball)


if __name__ == "__main__":
    main(sys.argv)
