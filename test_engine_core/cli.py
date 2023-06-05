"""Main test engine core CLI."""
import os
import sys

from test_engine_core import __version__


def version_msg():
    """Return the test engine version, location and Python powering it."""
    python_version = sys.version
    location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return f"Test Engine Core - {__version__} from {location} (Python {python_version})"


def main() -> None:
    """
    Print the version of test engine core
    """
    print(version_msg())
