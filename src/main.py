import os
import sys
import json
import tarfile
from models.module import Module
import utils

from registry import Registry
from config import Config
from semver import SemVer
from log import Log

WORKDIR = os.getenv("GITHUB_WORKSPACE", "")


def main(config: Config) -> str:

    registry = Registry(config.namespace, config.token)

    for module_folder in config.modules_list:

        module_folder = os.path.join(WORKDIR, module_folder)

        if not validate(module_folder):
            Log.warning(
                f"Module folder {module_folder} is not a valid terraform module."
            )
            Log.end_group()
            continue

        module_name = os.path.basename(module_folder)

        Log.start_group(f"Module {module_name}")

        if not registry.module_exists(module_name, config.provider):

            Log.info("The module selected does not exists.")
            registry.create_module(module_name, config.provider, registry_name)
        else:
            Log.info(f"Module {module_name} already exists.")

        module = registry.get_module(module_name, config.provider)

        new_version = bump_module_version(
            module,
            base_version,
            config.autobump_version,
        )

        if module.has_version(new_version):
            Log.warning(f"Module version {new_version} already exists.")
            if config.recreate:
                Log.debug(f"Recreate option enabled, version will be deleted.")
                registry.delete_version(module_name, config.provider, new_version)
            else:
                Log.end_group()
                continue

        tar_ball = package_module(module_name, module_folder)

        module_version = registry.create_version(
            module_name, config.provider, new_version
        )

        if module_version is not None:
            registry.upload_version(module_version.links["upload"], tar_ball)

        os.remove(tar_ball)

        Log.info(f"Module {module_name} with version {new_version} created.")

        Log.end_group()


def bump_module_version(
    module: Module, base_version: str, autobump_version: bool
) -> str:
    """Creates a new version for a module"""

    if not module.last_version is None and autobump_version:
        new_version = SemVer(version=module.last_version).bump_patch()

        Log.info(f"Bumping module version from {module.last_version} -> {new_version}.")
        return new_version
    else:
        Log.warning(
            f"Module has no version or autobump not enabeld. Base version {base_version} will be used."
        )
        return base_version


def package_module(module_name: str, module_dir: str) -> str:
    """Packages the folder content into a tar.gz file"""

    file_name = f"{module_name}.tar.gz"

    with tarfile.open(file_name, "w:gz") as tar:
        tar.add(module_dir, arcname=os.path.sep)

    return file_name


def validate(module_folder: str) -> bool:
    """Checks the module folder exists and it's a terraform module"""

    if not os.path.exists(module_folder):
        return False

    if not os.path.isfile(os.path.join(module_folder, "main.tf")):
        return False

    return True


if __name__ == "__main__":

    modules_list = sys.argv[1]
    provider = sys.argv[2]
    namespace = sys.argv[3]
    registry_name = sys.argv[4]
    token = sys.argv[5]
    recreate = sys.argv[6]
    base_version = sys.argv[7]
    autobump_version = sys.argv[8]

    config = Config(
        modules_list=json.loads(modules_list),
        provider=provider,
        namespace=namespace,
        base_version=base_version,
        token=token,
        registry_name=registry_name,
        autobump_version=utils.str_to_bool(autobump_version, False),
        recreate=utils.str_to_bool(recreate, False),
    )

    main(config)
