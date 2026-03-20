import paraview.simple as pv
import random
from ..logging import logger
from ..other import Vector3
from ..views import IViewObject
from . import IViewObjectModifier


class Glyph(IViewObjectModifier):
    def __init__(self, orientation_array=('POINTS', 'No orientation array'),
                 scale_array=('Points', 'No scale array'),
                 scale_factor: int = 0.0196,
                 color: Vector3 = Vector3(0.0, 0.0, 0.0),
                 glyph_type: str = "2D Glyph"):
        """
        Initialize a Glyph modifier used to visualize vector fields as glyphs.

        The Glyph allows to render glyphs (vector field directions) on top of a slice or 3d visualization.

        :param tuple[str, str] orientation_array: The array defining glyph orientation.
            Typically ``('POINTS', <field_name>)``.
        :param tuple[str, str] scale_array: The array defining glyph scaling.
            Typically ``('POINTS', <field_name>)``.
        :param int scale_factor: The global scale factor applied when no scale array is used.
        :param Vector3 color: The diffuse color of the glyphs.
        :param str glyph_type: The glyph type determining the glyph geometry.
            Options include: ``"2D Glyph"``, ``"Arrow"``, ``"Cone"``, ``"Box"``,
            ``"Cylinder"``, ``"Line"``, ``"Sphere"``.
        :return: None
        """
        self._orientation_array = orientation_array
        self._scale_array = scale_array
        self._scale_factor = scale_factor
        self._color = color
        self._glyph_type = glyph_type
    
    def render_callback(self, view_object: IViewObject, display: pv.Show):
        """
        Render glyphs onto an existing view object.

        This callback:
        - Creates a ParaView Glyph filter using the configured orientation array, scale array, glyph type, and scale factor.
        - Shows the glyphs in the same render view as the view object.
        - Applies a uniform diffuse color to the glyph geometry.
        - Overlays the glyphs on top of existing visualization elements.

        :param IViewObject view_object: The view object onto which the glyphs should be overlaid.
        :param pv.Show display: The existing display of the view object (unused but part of the callback signature).
        :return: None
        """
        # Create glyph object
        logger.info(f"Attaching glyph to {view_object}.")
        random_name = random.randint(0, 10000)
        glyph_obj = pv.Glyph(registrationName=f"Glyph_{random_name}", Input=view_object.get_render_object(),
                                GlyphType='Arrow')
        glyph_obj.OrientationArray = self._orientation_array
        glyph_obj.ScaleArray = self._scale_array
        glyph_obj.ScaleFactor = self._scale_factor
        glyph_obj.GlyphType = self._glyph_type
        # Add glyph object to render view
        glyph_display = pv.Show(glyph_obj, view_object.get_render_view(), 'GeometryRepresentation')
        # Attach color to glyph display
        pv.ColorBy(glyph_display, None)
        # Set uniform glyph color
        glyph_display.DiffuseColor = self._color.to_list()

