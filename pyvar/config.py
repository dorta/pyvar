# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

import os
from pathlib import Path

_cache_root = os.environ.get("XDG_CACHE_HOME")
CACHEDIR = os.path.join(_cache_root if _cache_root else str(Path.home() / ".cache"), "pyvar")
