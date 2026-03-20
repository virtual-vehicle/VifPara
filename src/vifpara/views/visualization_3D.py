import paraview.simple as pv

import numpy as np
from scipy.spatial.transform import Rotation as R
import scipy as sp
import warnings

from ..logging import logger
from ..other import Vector3
from ..base import Layout, Clipbox, Case
from . import IViewObject, Slice

import random


class Visualization3D(IViewObject):
    def __init__(self, case: Case, cam_position: Vector3, cam_up: Vector3 = Vector3(0, 0, 1),
                 focal_point: Vector3 = Vector3(0, 0, 0), width: int = 900, height: int = 720,
                 zoom: float = 1.0, show_orientation_axis: bool = False, show_color_bar: bool = True):
        """
        Initialize a 3D visualization view for displaying slice planes and geometry.

        The 3D visualization renders the case or clipbox as is into a layout cell.
        Slices can additionally be added to render their position on the case.
        This allows for an "overview" of your the slices you defined.

        :param Case case: The loaded visualization case.
        :param Vector3 cam_position: The world‑space position of the camera.
        :param Vector3 cam_up: The camera's up vector. Defaults to ``(0, 0, 1)``.
        :param Vector3 focal_point: The point the camera looks at. Defaults to ``(0, 0, 0)``.
        :param int width: The width of the 3D render view in pixels.
        :param int height: The height of the 3D render view in pixels.
        :param float zoom: Zoom factor for the camera.  
            ``2.0`` → twice the size, ``0.5`` → half the size.
        :param bool show_orientation_axis: Whether to show the ParaView orientation axis.
        :param bool show_color_bar: Whether to show a color bar in the 3D view.
        :return: None
        """
        super().__init__(case, width, height, show_orientation_axis)
        self._cam_position: Vector3 = cam_position
        self._cam_up: Vector3 = cam_up
        self._camera_scale: float = 1.0 / zoom
        self._show_color_bar: bool = show_color_bar

        self._render_view.CameraFocalPoint = focal_point.to_list()
        self._render_view.CameraPosition = self._cam_position.to_list()
        self._render_view.CameraViewUp = self._cam_up.to_list()
        self._render_view.CameraParallelProjection = 1
        self._render_view.CameraParallelScale = self._camera_scale

        pv.SetActiveView(None)
        pv.SetActiveView(self._render_view)
    
    def add_case_or_clip_to_view(self, case: Case, color_map=None, opacity=1.0, representation_type='Surface',
                                gaussian_radius=0.0012, field_type='Points',
                                representation_point_size: float = 1.0):
        """
        Add a Case or Clipbox object to the 3D visualization.

        This function:
        - Shows the case or clip object in the 3D render view.
        - Applies an optional color map.
        - Sets the representation, opacity, point size, and additional rendering options.
        - Supports both point-based and cell-based field data.
        - Can render Gaussian-point representations when using ``'Point Gaussian'``.

        :param Case case: The Case or Clipbox instance to visualize.
        :param ColorMap color_map: The color map applied to the object. If ``None``, the object is shown in gray.
        :param float opacity: The opacity of the displayed object (0.0–1.0).
        :param str representation_type: The data representation (e.g. ``"Surface"``, ``"Points"``,
            ``"Point Gaussian"``).
        :param float gaussian_radius: Radius used for Gaussian point rendering (only relevant for
            ``"Point Gaussian"`` representation).
        :param str field_type: Field data type. Set to ``"Cells"`` for cell-only datasets, otherwise ``"Points"``.
        :param float representation_point_size: Size of points when using point-based representations.
        :return: None
        """
        logger.info(f"Adding case {case} to 3D Visualization.")

        if representation_point_size <= 0.0:
            logger.error(f"Invalid representation point size given ({representation_point_size}). "
                        f"Must be larger than 0.0.")
            return

        environment = None
        if isinstance(case, Clipbox):
            environment = case.get_clip()
        elif isinstance(case, Case):
            environment = case.get_case()
        else:
            raise TypeError(
                f"Invalid object of type {type(case).__name__} provided to add_case_or_clip_to_view(). "
                f"Must be of type Case or Clipbox."
            )

        # activate render view
        pv.SetActiveView(None)
        pv.SetActiveView(self._render_view)

        # show object in render_view
        self._display = pv.Show(environment, self._render_view)

        # add color map to render_view
        if color_map is not None:
            color_map.apply_to_render_view(self._display, self._render_view, render=self._show_color_bar)
        else:
            pv.ColorBy(self._display, None)

        # set display opacity and representation
        self._display.Opacity = opacity
        self._display.SetRepresentationType(representation_type)
        self._display.PointSize = representation_point_size

        # set color array name if no point data is available
        if field_type == 'Cells' and color_map is not None:
            self._display.ColorArrayName = ['CELLS', color_map.get_field()]

        # define gaussian radius for particles
        if representation_type == 'Point Gaussian':
            self._display.GaussianRadius = gaussian_radius

    def add_slice_to_view(self, slice: Slice, text='', opacity=0.4, text_position=None, flip_y_label=False,
                        text_scale: float = 0.05, slice_scale: float = 1.0):
        """
        Add a slice plane and optional text annotation to the 3D view.

        This method:
        - Positions a slice plane in the 3D view according to its geometric definition.
        - Applies opacity and scaling.
        - Optionally adds a 3D text label aligned with slice orientation and camera direction.
        - Automatically computes transform, rotation, and placement of text.

        :param Slice slice: The slice whose geometric plane should be added to the 3D view.
        :param str text: Optional annotation text displayed near the slice. If empty, no text is shown.
        :param float opacity: Opacity of the slice plane (0.0–1.0).
        :param tuple|list|None text_position: Optional 3‑component position where the text should appear.
        :param bool flip_y_label: Whether the text’s y‑orientation should be flipped. Useful when the camera’s
            up‑vector is aligned along the y‑axis.
        :param float text_scale: Scale factor for the 3D text annotation.
        :param float slice_scale: Scaling factor applied to the slice plane geometry.
        :return: None
        """
        logger.info(f"Adding slice {slice} to 3D Visualization.")

        pv.SetActiveView(None)
        pv.SetActiveView(self._render_view)

        plane: pv.Plane = self._slice_to_plane(slice, slice_scale)

        display = pv.Show(plane, self._render_view)

        # set display opacity
        display.Opacity = opacity

        if text != '':
            # create and set text
            text_3D = pv.a3DText(registrationName='3DText')
            text_3D.Text = text

            # create transform
            transform = pv.Transform(registrationName='Transform', Input=text_3D)
            transform.Transform = 'Transform'

            # compute translation and rotation for text alignment
            transform.Transform.Translate = self._compute_translation(text_position, slice)
            transform.Transform.Rotate = self._compute_euler_angles_rotation(slice, flip_y_label)
            transform.Transform.Scale = (text_scale, text_scale, text_scale)

            # display transformed text in 3D view
            text_display = pv.Show(transform, self._render_view, 'GeometryRepresentation')
            text_display.AmbientColor = [0.0, 0.0, 0.0]
            text_display.DiffuseColor = [0.0, 0.0, 0.0]
            text_display.Opacity = 1.0

    def _render_inside(self, layout: Layout, row: int=0, col: int=0):
        """
        Renders the visualization 3D into a cell in the layout.

        Parameters:
        ----------
        layout: Layout
            The layout to render the visualization in.
        row: int
            The row to render the visualization in.
        col: int
            The col in the given row to render the visualization in.
        """
        logger.info(f"Rendering Visualization 3D to <{row}|{col}>.")

        layout.add_render_view(row, col, self)

        # create slice based on origin, normal and type
        pv.SetActiveView(None)
        pv.SetActiveView(self._render_view)

    def get_render_object(self):
        return None

    def get_cam_up(self):
        return self._cam_up

    def _slice_to_plane(self, slice: Slice, plane_scale: float = 1.0) -> pv.Plane:
        """Create a ParaView plane that spans the bounding box of the slice object."""

        # Get slice properties
        plane_normal = np.array(slice.get_normal().to_list())
        # slice_origin = np.array(slice.get_origin().to_list())

        # Get bounding box of the object
        (x_min, x_max, y_min, y_max, z_min, z_max) = slice.get_render_object().GetDataInformation().GetBounds()

        # Compute bounding box center and extents
        center = np.array([
            0.5 * (x_min + x_max),
            0.5 * (y_min + y_max),
            0.5 * (z_min + z_max),
        ])
        extent = np.array([
            (x_max - x_min),
            (y_max - y_min),
            (z_max - z_min),
        ])

        # Find a vector that's not parallel to the normal
        if abs(plane_normal[0]) < 0.9:
            temp_vector = np.array([1, 0, 0])
        else:
            temp_vector = np.array([0, 1, 0])

        # Create perpendicular basis
        perp_vector1 = np.cross(plane_normal, temp_vector)
        perp_vector1 /= np.linalg.norm(perp_vector1)

        perp_vector2 = np.cross(plane_normal, perp_vector1)
        perp_vector2 /= np.linalg.norm(perp_vector2)

        # Project the bounding box extents onto perp vectors
        size1 = np.dot(extent, np.abs(perp_vector1)) * plane_scale
        size2 = np.dot(extent, np.abs(perp_vector2)) * plane_scale

        # Define the plane spanning the bounding box in slice coordinates
        plane = pv.Plane(registrationName=f"Plane_{random.randint(0, 1000)}")
        plane_origin = (center - 0.5 * size1 * perp_vector1 - 0.5 * size2 * perp_vector2).tolist()
        plane.Origin = plane_origin
        plane.Point1 = (np.array(plane_origin) + size1 * perp_vector1).tolist()
        plane.Point2 = (np.array(plane_origin) + size2 * perp_vector2).tolist()

        return plane

    # private function _compute_euler_angles_rotation
    # computes text rotation in euler angles
    # returns euler angles in x,y,z format
    def _compute_euler_angles_rotation(self, obj, flip_y_label):
        text_normal = np.array([0, 0, 1])  # default creation value
        text_up = np.array([0, 1, 0])  # default creation value
        slice_normal = np.array(obj.get_normal().to_list())

        up_vector1 = self._cam_up.to_list()
        up_vector2 = text_up

        norm_vector1 = [0, 0, 0]
        norm_vector2 = text_normal

        # check if camera up and slice normal are equal
        if np.array_equal(self._cam_up.to_list(), slice_normal):
            # set text normal facing to camera
            norm_vector1 = np.array(self._cam_position.to_list()) - np.array(self._render_view.CameraFocalPoint)
            norm_vector1 = np.rint(norm_vector1 / np.linalg.norm(norm_vector1)).astype(int)
        else:
            # check if slice normal is facing the camera, otherwise transform
            if np.dot(self._render_view.CameraFocalPoint - np.array(self._cam_position.to_list()), slice_normal) > 0:
                slice_normal = slice_normal * -1

            # set text normal to slice normal
            norm_vector1 = slice_normal

        # define transformation pairs,  vec_pair1 is camera up vector and final text normal,
        #                               vec_pair2 is text up and text normal
        vec_pair1 = [up_vector1, norm_vector1]
        vec_pair2 = [up_vector2, norm_vector2]

        # compute rotation to align transformation pairs
        rot, rmsd = R.align_vectors(a=vec_pair1, b=vec_pair2)

        rot_final = np.array([0, 0, 0])

        sp.special.seterr(all='raise')
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            try:
                rot_final = rot.as_euler('xyz', degrees=True)
            except UserWarning:
                if np.array_equal(self._cam_up, [1, 0, 0]):
                    logger.warning("Catched gimbal lock")
                    rot_final = rot.as_euler('zyz', degrees=True)
                    if flip_y_label:
                        rot_final = np.array([0, -rot_final[1], rot_final[0] + rot_final[2]])
                    else:
                        rot_final = np.array([0, rot_final[1], rot_final[0] + rot_final[2]])
                else:
                    warnings.simplefilter("ignore")
                    rot_final = rot.as_euler('xyz', degrees=True)

            warnings.simplefilter("ignore")
        rot_final = np.rint(rot_final / 90.0) * 90.0

        return rot_final

    # private function _compute_translation
    # computes translation for text alignment in 3D view
    # returns translation
    def _compute_translation(self, translation, obj):
        # check if translation was set by user
        if translation is None:
            (x_min, x_max, y_min, y_max, z_min, z_max) = obj.get_render_object().GetDataInformation().GetBounds()
            translation = np.array([0.0, 0.0, 0.0])

            # compute nearest corner of slice bounds to camera
            if np.abs(self._cam_position[0] - x_min) > np.abs(self._cam_position[0] - x_max):
                translation += np.array([x_max, 0.0, 0.0])
            else:
                translation += np.array([x_min, 0.0, 0.0])

            if np.abs(self._cam_position[1] - y_min) > np.abs(self._cam_position[1] - y_max):
                translation += np.array([0.0, y_max, 0.0])
            else:
                translation += np.array([0.0, y_min, 0.0])

            if np.abs(self._cam_position[2] - z_min) > np.abs(self._cam_position[2] - z_max):
                translation += np.array([0.0, 0.0, z_max])
            else:
                translation += np.array([0.0, 0.0, z_min])

        return translation
