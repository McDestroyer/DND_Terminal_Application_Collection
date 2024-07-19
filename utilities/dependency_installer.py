import os
import importlib.util


# The following is V2 of the dependency installer. If it doesn't work, try V1 commented out below.
# It didn't work. V1 has now been updated and is now the primary system again.
# def _install_dependency(dependency: str, silent: bool = False) -> bool:
#     """Install a dependency if it is not already installed.
#
#     Args:
#         dependency (str):
#             The _name of the dependency to install.
#         silent (bool, optional):
#             Whether to print output.
#             Defaults to False.
#
#     Returns:
#         bool: True if the dependency was already installed.
#     """
#     try:
#         importlib.metadata.distribution(dependency)
#         if not silent:
#             print(f"{dependency} is installed.")
#         return True
#     except importlib.metadata.PackageNotFoundError:
#         if not silent:
#             print(f"{dependency} is not installed. Installing...")
#         subprocess.run(['pip', 'install', dependency], check=True)
#         if not silent:
#             print(f"{dependency} has been installed.")
#         return False


def install_dependency(dependency: str, silent: bool = False) -> bool:
    """Install a dependency if it is not already installed.

    Args:
        dependency (str):
            The _name of the dependency to install.
        silent (bool, optional):
            Whether to print output.
            Defaults to False.

    Returns:
        bool: True if the dependency was already installed.
    """
    # Checks to see if the dependency is installed. If not, installs it.
    if not silent:
        print(f"Checking for {dependency}")
        spec = importlib.util.find_spec(dependency)
        if spec:
            print(f"{dependency} is installed.")
            return True
        else:
            print(f"{dependency} is not installed. Installing...")
            os.system(f'pip install {dependency}')
            os.system(f'python -m pip install {dependency}')
            os.system(f'python3 -m pip install {dependency}')
            os.system(f'py -m pip install {dependency}')
            print(f"{dependency} has been installed.")
            return False
    else:
        spec = importlib.util.find_spec(dependency)
        if spec:
            return True
        else:
            os.system(f'pip install {dependency} --quiet')
            os.system(f'python -m pip install {dependency} --quiet')
            os.system(f'python3 -m pip install {dependency} --quiet')
            os.system(f'py -m pip install {dependency} --quiet')
            return False