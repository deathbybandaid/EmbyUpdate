#!/usr/bin/env python3
# coding=utf-8
# pylama:ignore=E402

import os
import sys
import pathlib
SCRIPT_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))

"""Install Dependencies at startup."""
from deps import Dependencies
deps = Dependencies(SCRIPT_DIR)

from EmbyUpdate.cli import run

if __name__ == "__main__":
    """Calls EmbyUpdate.cli running methods."""
    sys.exit(run.main(SCRIPT_DIR, deps))
