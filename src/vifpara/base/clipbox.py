import paraview.simple as pv
from ..other import Vector3
from . import Case


class Clipbox:
    def __init__(self, case: Case, position: Vector3 = Vector3(-1.0, -2.0, 0.0),
                 length: Vector3 = Vector3(5.0, 4.0, 3.0)):
        """
        Create a Clipbox to cut a region from a loaded case.

        The Clipbox allows to clip a case to focus on a certain aspect of it.
        It takes a case and can then be used instead of the case when adding to a visualization 3d.

        :param Case case: The loaded VifPara case to apply the clip to.
        :param Vector3 position: The clip box origin in x-, y-, and z-direction.
        :param Vector3 length: The clip box size in x-, y-, and z-direction.
        :return: None
        """
        self._case = case.get_case()
        self._clip_type = 'Box'
        self._position = position
        self._length = length
        self._clip = pv.Clip(Input=self._case)
        self._clip.ClipType = self._clip_type
        self._clip.ClipType.Position = self._position.to_list()
        self._clip.ClipType.Length = self._length.to_list()

    def get_clip(self):
        return self._clip
