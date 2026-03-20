import paraview.simple as pv
import random
from typing import Tuple
from ..logging import logger
from ..other import Vector3
from ..views import IViewObject, ColorMap
from . import IViewObjectModifier


class StreamTracer(IViewObjectModifier):
    def __init__(self, vectors: Tuple,
                 seed_point_1: Vector3 = Vector3(-5.0, -4.0, 0.0),
                 seed_point_2: Vector3 = Vector3(15.0, 4.0, 8.0),
                 color_array_name: Tuple = ("POINTS", "No color array"),
                 representation_type: str = "Surface", max_stream_length: float = 20.0,
                 resolution: int = 1000, direction: str = "BOTH"):
        """
        Initialize a StreamTracer modifier used to visualize vector fields as streamlines.

        The StreamTracer renders streamlines by integrating a vector field starting from
        user-defined seed geometry. The resulting streamline geometry is rendered on top
        of an existing 2D or 3D visualization.

        :param tuple[str, str] vectors: The vector field used for streamline integration.
            Typically ``('POINTS', <field_name>)``.
        :param Vector3 seed_point_1: First point defining the line seed geometry.
        :param Vector3 seed_point_2: Second point defining the line seed geometry.
        :param tuple[str, str] color_array_name: The array used to color the streamlines.
            Typically ``('POINTS', <field_name>)``. Use ``("POINTS", "No color array")`` to
            disable scalar coloring and apply a uniform color.
        :param str representation_type: The representation used to display the streamlines.
            Common options include ``"Wireframe"``, ``"Surface"``, and ``"3D Glyphs"``.
        :param float max_stream_length: The maximum length of the generated streamlines.
        :param int resolution: The number of streamlines to render.
        :param str direction: The direction the streams should be spawned from the seed line.
            Can be ``"BOTH"``, ``"FORWARD"``, or ``"BACKWARD"``.
        :return: None
        """
        self._vectors = vectors
        self._seed_point_1 = seed_point_1
        self._seed_point_2 = seed_point_2
        self._color_array_name = color_array_name
        self._representation_type = representation_type
        self._max_stream_length = max_stream_length
        self._resolution = resolution
        self._direction = direction

    def render_callback(self, view_object: IViewObject, display: pv.Show):
        """
        Render streamlines onto an existing view object.

        This callback:
        - Creates a ParaView StreamTracer filter using the view object's render data as input.
        - Uses a line seed defined by ``seed_point_1`` and ``seed_point_2``.
        - Displays the resulting streamlines in the same render view as the base visualization.
        - Applies either scalar-based coloring or a uniform diffuse color.

        :param IViewObject view_object: The view object onto which the streamlines should be overlaid.
        :param pv.Show display: The existing display of the view object (unused but part of the callback signature).
        :return: None
        """
        # Create glyph object
        logger.info(f"Attaching stream tracer to {view_object}.")
        random_name = random.randint(0, 10000)
        stream_obj = pv.StreamTracer(registrationName=f"StreamTracer_{random_name}", Input=view_object.get_case().get_case(),
                                     SeedType="Line")
        stream_obj.Vectors = self._vectors
        stream_obj.SeedType.Point1 = self._seed_point_1.to_list()
        stream_obj.SeedType.Point2 = self._seed_point_2.to_list()
        stream_obj.SeedType.Resolution = self._resolution
        stream_obj.MaximumStreamlineLength = self._max_stream_length
        stream_obj.IntegrationDirection = self._direction

        # Add glyph object to render view
        stream_display = pv.Show(stream_obj, view_object.get_render_view(), 'GeometryRepresentation')
        stream_display.Representation = self._representation_type
        stream_display.Opacity = 1.0
        stream_display.ScaleFactor = 1.0

        # Attach color to glyph display
        if "No color array" in self._color_array_name:
            pv.ColorBy(stream_display, None)
            # Set uniform glyph color
            stream_display.DiffuseColor = Vector3(80.0, 0.0, 0.0).to_list()
        else:
            pv.ColorBy(stream_display, self._color_array_name)

