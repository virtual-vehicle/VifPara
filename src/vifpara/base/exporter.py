import paraview.simple as pv

import numpy as np
from ..other import Vector3, is_valid_extension
from ..logging import logger
from . import Layout, Config


class Exporter:
    def __init__(self, layout: Layout, config: Config):
        """
        Initialize an exporter responsible for creating images and videos from a layout.

        The exporter takes a layout and saves images and animations to the set plots path inside a config instance.

        :param Layout layout: The layout object to export.
        :param Config config: The configuration object containing the output directories
            for saving exported images and videos.
        :return: None
        :raises TypeError: If the provided layout is not a ``Layout`` instance or the
            config is not a ``Config`` instance.
        """
        self.layout = layout
        self.config = config

        if not isinstance(layout, Layout):
            raise TypeError(f"Provided a {type(layout).__name__} instead of a layout to an Exporter. Please provide a Layout object.")

        if not isinstance(config, Config):
            raise TypeError(f"Provided a {type(config).__name__} instead of a config to an Exporter. Please provide a Config object.")

    def save_snapshot(self, filename: str):
        """
        Save a single screenshot of the layout at the first timestep.

        :param str filename: The base filename (without extension) for the exported image.
        :return: None
        """
        logger.info(f"Exporting snapshot of layout to {self.config.get_plot_path()}{filename}.png.")
        self.layout.prepare_export()
        pv.SaveScreenshot(self.config.get_plot_path() + filename + ".png", self.layout.get_layout())

    def save_at_timesteps(self, filename: str, timesteps: list[float]):
        """
        Save the layout as PNG images at the specified timesteps.

        This behaves like ``save_animation`` in image mode (e.g., PNG export),
        but uses explicit timestep values rather than frame indices.

        :param str filename: The base filename (without extension) for exported images.
        :param list[float] timesteps: The list of timesteps at which images should be saved.
        :return: None
        """
        logger.info(f"Exporting snapshot at {len(timesteps)} timesteps to {self.config.get_plot_path()}{filename}.")

        self.layout.prepare_export()
        animation_scene = pv.GetAnimationScene()
        prev_timestep: float = animation_scene.AnimationTime

        for i in range(0, len(timesteps)):
            animation_scene.AnimationTime = timesteps[i]
            self.save_snapshot(filename=filename + "_" + str(timesteps[i]))
        animation_scene.AnimationTime = prev_timestep

    def save_at_all_timesteps(self, filename: str):
        """
        Save the layout as PNG images at all available timesteps.

        This behaves like ``save_animation`` in image mode (PNG export),
        but saves frames at actual timestep values instead of frame indices.

        :param str filename: The base filename (without extension) for exported images.
        :return: None
        """
        animation_scene = pv.GetAnimationScene()
        timesteps = animation_scene.TimeKeeper.TimestepValues
        self.save_at_timesteps(filename, timesteps)

    def save_animation(self, filename: str, start_frame: int = 0, end_frame: int = -1,
                    framerate: int = 30, format: str = ".ogv"):
        """
        Save an animation of the layout.

        This method exports either a video (e.g., ``.ogv``) or a sequence of image frames
        (e.g., ``.png`` or ``.jpg``), depending on the file extension provided.

        :param str filename: The base filename (without extension) for the animation export.
        :param int start_frame: The index of the first frame to render (must be ≥ 0).
        :param int end_frame: The index of the last frame to render. If ``-1`` or greater than
            the number of frames, it is automatically clamped to the maximum available frame.
        :param int framerate: The framerate of the exported video.
        :param str format: The output format (e.g., ``".png"``, ``".jpg"``, ``".jpeg"``, ``".ogv"``).
        :return: None
        """
        logger.info(f"Exporting animation to {self.config.get_plot_path()}{filename}{format}.")
        if not is_valid_extension(format, [".png", ".jpg", ".jpeg", ".ogv"]):
            return
        if start_frame < 0:
            logger.error(f"Cannot export animation where start frame ({start_frame}) is negative.")
            return

        animation_scene = pv.GetAnimationScene()
        animation_scene.UpdateAnimationUsingDataTimeSteps()
        max_frames: int = len(animation_scene.TimeKeeper.TimestepValues)
        if end_frame == -1 or end_frame > max_frames:
            end_frame = max_frames
        if end_frame <= start_frame:
            logger.error(f"Cannot export animation where end frame ({end_frame}) is before start frame ({start_frame}).")
            return

        logger.info(f"Exporting frames {start_frame} to {end_frame}.")

        self.layout.prepare_export()
        pv.SaveAnimation(
            self.config.get_plot_path() + filename + format,
            self.layout.get_layout(),
            FrameWindow=[start_frame, end_frame + 1],
            FrameRate=framerate
        )

    def save_camera_orbit_animation(self, orbiting_visualization: "Visualization3D", filename: str,
                                    start_time: int, end_time: int, nr_frames: int, framerate: int,
                                    format: str = ".ogv"):
        """
        Save an animation of a camera orbiting around a focal point in a 3D visualization.

        This creates a camera animation path (orbit) and renders frames along the path.
        The output can be an image sequence or a video depending on the file extension.

        :param Visualization3D orbiting_visualization: The 3D visualization whose camera should orbit.
        :param str filename: The base filename (without extension) for the exported animation.
        :param int start_time: The starting timestep of the animation.
        :param int end_time: The ending timestep of the animation.
        :param int nr_frames: The number of frames to generate between the start and end time.
        :param int framerate: The framerate for exported video formats.
        :param str format: The output format (e.g. ``".png"``, ``".jpg"``, ``".ogv"``).
        :return: None
        """
        logger.info(f"Exporting camera orbit animation to {self.config.get_plot_path()}{filename}{format}.")
        if not is_valid_extension(format, [".png", ".jpg", ".jpeg", ".ogv"]):
            return

        self.layout.prepare_export()

        # configure animation scene
        animation_scene = self._configure_animation_scene(start_time=start_time, end_time=end_time,
                                                        nr_frames=nr_frames, framerate=framerate)
        animation_scene.UpdateAnimationUsingDataTimeSteps()

        render_view = orbiting_visualization.get_render_view()

        # compute camera orbit points
        points = self._compute_points_on_circle(
            Vector3.from_list(render_view.CameraFocalPoint),
            orbiting_visualization.get_cam_up()
        )

        camera_animation_cue = pv.GetCameraTrack(view=render_view)

        # create start key frame
        key_frame_start = pv.CameraKeyFrame()
        key_frame_start.Position = [points[0], points[1], points[2]]
        key_frame_start.FocalPoint = render_view.CameraFocalPoint
        key_frame_start.ViewUp = render_view.CameraViewUp
        key_frame_start.ParallelScale = render_view.CameraParallelScale
        key_frame_start.PositionPathPoints = points
        key_frame_start.FocalPathPoints = render_view.CameraFocalPoint
        key_frame_start.ClosedPositionPath = 1

        # create end key frame
        key_frame_end = pv.CameraKeyFrame()
        key_frame_end.KeyTime = 1.0
        key_frame_end.Position = key_frame_start.Position
        key_frame_end.FocalPoint = render_view.CameraFocalPoint
        key_frame_end.ViewUp = render_view.CameraViewUp
        key_frame_end.ParallelScale = render_view.CameraParallelScale

        # configure animation scene
        camera_animation_cue.Mode = 'Path-based'
        camera_animation_cue.KeyFrames = [key_frame_start, key_frame_end]

        # play animation
        animation_scene.Play()
        pv.SaveAnimation(
            self.config.get_plot_path() + filename + format,
            self.layout.get_layout(),
            FrameWindow=[0, nr_frames - 1],
            FrameRate=framerate
        )

    # private function to configure the animation scene
    def _configure_animation_scene(self, start_time, end_time, nr_frames, framerate):
        animation_scene = pv.GetAnimationScene()
        animation_scene.StartTime = start_time
        animation_scene.EndTime = end_time
        animation_scene.NumberOfFrames = nr_frames
        animation_scene.FramesPerTimestep = framerate
        return animation_scene


    # private function to compute the camera positions of an orbiting camera around an origin
    # returns the computed camera positions
    def _compute_points_on_circle(self, origin: Vector3, cam_up: Vector3):
        points = np.empty(10 * 3)

        # transform cam up vector
        cam_up = cam_up - 1
        cam_up = cam_up * -1

        # calculate points of circle in plane
        for i in range(0, 10 * 3, 3):
            points[i] = origin.x + cam_up.x * np.cos(2 * np.pi * i / 10)
            points[i + 1] = origin.y + cam_up.y * np.sin(2 * np.pi * i / 10)

            if points[i] == origin.x:
                points[i + 2] = origin.z + cam_up.z * np.cos(2 * np.pi * i / 10)
            else:
                points[i + 2] = origin.z + cam_up.z * np.sin(2 * np.pi * i / 10)

        return points