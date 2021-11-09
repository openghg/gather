from . import aqmesh, beaco2n, pipeline, utils, handlers
import sys as _sys

__all__ = ["aqmesh", "beaco2n", "utils", "pipeline", "handlers"]

if _sys.version_info.major < 3:
    raise ImportError("openghg requires Python 3.7 minimum")

if _sys.version_info.minor < 7:
    raise ImportError("openghg requires Python 3.7 minimum")
