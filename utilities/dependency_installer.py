import os
import subprocess
import importlib.metadata


# The following is V2 of the dependency installer. If it doesn't work, try V1 commented out below.
def install_dependency(dependency: str, silent: bool = False) -> bool:
    """Install a dependency if it is not already installed.

    Args:
        dependency (str):
            The name of the dependency to install.
        silent (bool, optional):
            Whether to print output.
            Defaults to False.

    Returns:
        bool: True if the dependency was already installed.
    """
    try:
        importlib.metadata.distribution(dependency)
        if not silent:
            print(f"{dependency} is installed.")
        return True
    except importlib.metadata.PackageNotFoundError:
        if not silent:
            print(f"{dependency} is not installed. Installing...")
        subprocess.run(['pip', 'install', dependency], check=True)
        if not silent:
            print(f"{dependency} has been installed.")
        return False


def _install_dependency_v1(dependency: str, silent: bool = False) -> bool:
    """Install a dependency if it is not already installed.

    Args:
        dependency (str):
            The name of the dependency to install.
        silent (bool, optional):
            Whether to print output.
            Defaults to False.

    Returns:
        bool: True if the dependency was already installed.
    """
    import pkg_resources

    # Checks to see if the dependency is installed. If not, installs it.
    if not silent:
        try:
            print(f"Checking for {dependency}")
            pkg_resources.require(dependency)
            print(f"{dependency} is installed.")
            return True
        except pkg_resources.DistributionNotFound:
            print(f"{dependency} is not installed. Installing...")
            os.system(f'pip install {dependency} --quiet')
            os.system(f'python -m pip install {dependency} --quiet')
            os.system(f'python3 -m pip install {dependency} --quiet')
            os.system(f'py -m pip install {dependency} --quiet')
            print(f"{dependency} has been installed.")
            return False
    else:
        try:
            pkg_resources.require(dependency)
            return True
        except pkg_resources.DistributionNotFound:
            os.system(f'pip install {dependency} --quiet')
            os.system(f'python -m pip install {dependency} --quiet')
            os.system(f'python3 -m pip install {dependency} --quiet')
            os.system(f'py -m pip install {dependency} --quiet')
            return False
