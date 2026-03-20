import paraview.simple as pv
from ..logging import logger
from ..views import IViewObject

class IViewObjectModifier:
    def __init__(self):
        pass

    def attach(self, view_object: IViewObject):
        """
        Attach this modifier to the given view object.

        This method registers the modifier's ``render_callback`` with the
        provided view object. When the view renders, the callback will be
        invoked, allowing the modifier to alter or extend the rendering
        process.

        :param IViewObject view_object: The view object to which the modifier
            should be attached.
        :return: None
        """
        view_object.add_modifier_callback(self.render_callback)

    def render_callback(self, view_object: IViewObject, display: pv.Show):
        """
        Used to render the view modifier object.
        """
        pass