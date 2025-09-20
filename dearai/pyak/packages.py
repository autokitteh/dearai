import re
import sys
from subprocess import run
from shutil import which


def install(*packages):
    """Install Python packages using pip.

    A package can be either a package requirement specifier
    (see https://pip.pypa.io/en/stable/reference/requirement-specifiers/)
    or a tuple of (package specifier, import name) in case the import name differs from
    the package name (e.g. Package `pillow` import imported as `PIL`).

    Please refrain from using this function in production code, specify your dependencies in requirements.txt instead.

    Examples:
    >>> install('requests', 'numpy')
    >>> install('requests ~= 2.32', 'numpy == 2.0.0')
    >>> install(['pillow ~= 10.4', 'PIL'])
    """
    ...
