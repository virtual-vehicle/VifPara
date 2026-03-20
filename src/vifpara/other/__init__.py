try:
    import paraview.simple as pv
except ImportError:
    raise ImportError("ParaView dependency not found. Please install first or use the PV_VENV environment variable to link to a pvpython location. And make sure to run your script with 'vifpara' instead of 'python'.")

from .vector3 import Vector3
from .pv_utils import set_palette, PaletteOption
from .utils import is_valid_extension