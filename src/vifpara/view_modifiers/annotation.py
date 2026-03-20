import paraview.simple as pv
from ..logging import logger
from ..views import IViewObject


def annotate_time(view_object: IViewObject, font: str = 'Times', font_size: int = 19,
                  window_location: str = 'Upper Left Corner', digits_after_comma: int = 2,
                  unit: str = "s"):
    """
    Add a time annotation overlay to a view.

    :param IViewObject view_object: The view object to annotate with the current simulation time.
    :param str font: Font used for the annotation (e.g., ``"Times"``, ``"Arial"``, ``"Courier"``).
    :param int font_size: Font size of the displayed time label.
    :param str window_location: The location of the time annotation within the view.
        Options include: ``"Upper Left Corner"``, ``"Upper Right Corner"``,
        ``"Upper Center"``, ``"Lower Left Corner"``, ``"Lower Center"``, ``"Lower Right Corner"``.
    :param int digits_after_comma: Number of decimal places to display.
        If ``0``, the time is shown as an integer.
    :param str unit: The time unit appended to the label (e.g., ``"s"``, ``"ms"``, ``"h"``).
    :return: None
    """
    logger.info("Annotating time to view.")
    time_filter = pv.AnnotateTimeFilter(Input=view_object.get_render_object())
    time_filter.Format = 'Time: {time:.' + str(digits_after_comma) + 'f}' + unit
    display = pv.Show(time_filter, view_object.get_render_view(), 'TextSourceRepresentation')
    display.FontSize = font_size
    display.FontFamily = font
    display.WindowLocation = window_location

def annotate_coordinates(view_object: IViewObject, vector, font: str = 'Times', font_size: int = 19,
                         window_location: str = 'Upper Center', digits_after_comma: int = 3):
    """
    Add a coordinate annotation (X, Y, Z) to a view.

    :param IViewObject view_object: The view object to annotate.
    :param Vector3|tuple|list vector: The coordinate triple to annotate. May be a ``Vector3`` or 
        a tuple/list of floats.
    :param str font: Font used for the annotation text.
    :param int font_size: Size of the annotation text.
    :param str window_location: Placement of the annotation inside the render view.
    :param int digits_after_comma: Number of decimal places for formatting the coordinate values.
    :return: None
    """
    logger.info("Annotating coordinates to view.")

    if hasattr(vector, "x"):
        x, y, z = vector.x, vector.y, vector.z
    else:
        x, y, z = vector
    txt = pv.Text()
    txt.Text = f"Origin: ({x:.{digits_after_comma}f}, {y:.{digits_after_comma}f}, {z:.{digits_after_comma}f})"
    disp = pv.Show(txt, view_object.get_render_view(), 'TextSourceRepresentation')
    disp.FontSize = font_size
    disp.FontFamily = font
    disp.WindowLocation = window_location

def annotate_text(view_object: IViewObject, text: str, font: str = 'Times', font_size: int = 19,
                  window_location: str = 'Upper Center'):
    """
    Add an arbitrary text annotation to a view.

    :param IViewObject view_object: The view object to annotate.
    :param str text: The text content to display.
    :param str font: Font used for the annotation text.
    :param int font_size: Size of the annotation text.
    :param str window_location: Placement of the annotation inside the render view.
    :return: None
    """
    logger.info("Annotating text to view.")

    txt = pv.Text()
    txt.Text = text
    disp = pv.Show(txt, view_object.get_render_view(), 'TextSourceRepresentation')
    disp.FontSize = font_size
    disp.FontFamily = font
    disp.WindowLocation = window_location
