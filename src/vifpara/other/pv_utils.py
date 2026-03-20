from enum import IntEnum
import paraview.simple as pv
from ..logging import logger


class PaletteOption(IntEnum):
    NONE=0
    WHITE=1
    NEUTRAL_GRAY=2
    BLUE_GRAY=3
    LIGHT_GRAY=4
    BLACK=5
    GRADIENT=6


def set_palette(option: PaletteOption = PaletteOption.WHITE):
    """
    Set the ParaView rendering palette based on a palette option.

    :param PaletteOption option: The palette mode to apply, as defined in the
        ``PaletteOption`` enum.
    :return: None
    """
    if option == 1:
        pv.LoadPalette('WhiteBackground')
    elif option == 2:
        pv.LoadPalette('NeutralGrayBackground')
    elif option == 3:
        pv.LoadPalette('BlueGrayBackground')
    elif option == 4:
        pv.LoadPalette('LightGrayBackground')
    elif option == 5:
        pv.LoadPalette('BlackBackground')
    elif option == 6:
        pv.LoadPalette('GradientBackground')
    else:
        logger.info(f"Invalid palette option provided ({option}).")
