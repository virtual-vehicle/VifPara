import paraview.simple as pv
from ..logging import logger



class ColorMap:
    def __init__(self, field: str, legend_title=None, component_title='', legend_font='Times',
                 title_font_size=16, label_font_size=16, legend_format_digits_before=6,
                 legend_format_digits_after=2, legend_format_type='f', orientation='Horizontal',
                 location='Lower Center', size=0.5, preset='Rainbow Desaturated', number_values=0,
                 min_value=None, max_value=None, text_left='', text_right='', text_upper='', text_lower='',
                 text_font_size=16, use_log_scale: bool = False, field_type: str = "POINTS"):
        """
        Initialize a ColorMap configuration used to define color mapping, color bar appearance,
        legend formatting, and optional text annotations.

        The ColorMap can be passed to the constructor of a slice to modify its value range and color representation.

        :param str field: The field used for coloring. Also used as the legend title if no
            ``legend_title`` is provided.
        :param str legend_title: The title to display above the color bar. If ``None``,
            the ``field`` name is used.
        :param str component_title: Optional component name appended to the legend title.
        :param str legend_font: Font used for the legend and annotation text. Options include:
            ``'Arial'``, ``'Courier'``, ``'Times'``.
        :param int title_font_size: Font size of the legend title.
        :param int label_font_size: Font size of the labels along the color bar.
        :param int legend_format_digits_before: Number of digits before the decimal separator.
        :param int legend_format_digits_after: Number of digits after the decimal separator.
        :param str legend_format_type: Number format type:  
            - ``'f'`` → floating point  
            - ``'e'`` → exponential  
            - ``'d'`` → integer  
            - ``'g'`` → floating/exponential  
        :param str orientation: Orientation of the color bar. Options:
            ``'Horizontal'`` or ``'Vertical'``.
        :param str location: Screen placement of the color bar. Options include:
            ``'Lower Center'``, ``'Upper Center'``,  
            ``'Lower Right Corner'``, ``'Lower Left Corner'``,
            ``'Upper Left Corner'``, ``'Upper Right Corner'``.
        :param float size: Relative size of the color bar compared to the render view.
        :param str preset: Predefined ParaView color map preset (e.g., ``'Viridis (matplotlib)'``,
            ``'Turbo'``, ``'Rainbow Desaturated'``).
        :param int number_values: If > 0, the color map is discretized into this many values.
            If 0, a continuous color map is used.
        :param float min_value: Minimum scalar value for the color mapping.
        :param float max_value: Maximum scalar value for the color mapping.
        :param str text_left: Annotation on the left side of the render window.
        :param str text_right: Annotation on the right side.
        :param str text_upper: Annotation at the top.
        :param str text_lower: Annotation at the bottom.
        :param int text_font_size: Font size for annotation text.
        :param bool use_log_scale: Whether the color mapping should use a logarithmic scale.
        :param str field_type: Whether the coloring uses ``"POINTS"`` or ``"CELLS"`` data.
        :return: None
        """
        self._field = field
        self._field_type: str = field_type
        self._legend_title = field if legend_title is None else legend_title
        self._component_title = component_title
        self._legend_font = legend_font
        self._title_font_size = title_font_size
        self._label_font_size = label_font_size

        self._legend_format_digits_before = legend_format_digits_before
        self._legend_format_digits_after = legend_format_digits_after
        self._legend_format_type = legend_format_type

        self._orientation = orientation
        self._location = location
        self._size = size
        self._preset = preset
        self._number_values = number_values

        self._min_value = min_value
        self._max_value = max_value

        self._text_left = text_left
        self._text_right = text_right
        self._text_upper = text_upper
        self._text_lower = text_lower
        self._text_font_size = text_font_size

        self._use_log_scale: bool = use_log_scale

    def apply_to_render_view(self, display: pv.Show, render_view, render=True):
        """
        Apply the color map and configure the color bar in the given render view.

        This method:
        - Applies the scalar coloring to the given display.
        - Sets up the color transfer function (LUT).
        - Applies preset colors, log scaling, min/max ranges, and discretization.
        - Configures the scalar bar (legend) properties such as font, orientation, size, and label format.
        - Shows or hides the color bar depending on the ``render`` flag.
        - Optionally renders annotation text (left, right, upper, lower).

        :param pv.Show display: The geometry representation displayed in the render view.
        :param paraview.simple.RenderView render_view: The render view in which the color bar is shown.
        :param bool render: Whether the color bar should be visible. ``True`` = show, ``False`` = hide.
        :return: None
        """
        if self._legend_format_digits_before < 0:
            logger.warning(
                f"Set digits before of color bar are negative ({self._legend_format_digits_before}). "
                "Please set a non-negative value. Correcting to 0."
            )
            self._legend_format_digits_before = 0
        if self._legend_format_digits_after < 0:
            logger.warning(
                f"Set digits after of color bar are negative ({self._legend_format_digits_after}). "
                "Please set a non-negative value. Correcting to 0."
            )
            self._legend_format_digits_after = 0

        # get color data according to color transfer function
        try:
            pv.ColorBy(display, self._field, separate=True)
        except RuntimeError:
            # This happens when the display has no associated geometry or field.
            pass
        c_lut = pv.GetColorTransferFunction(self._field, display, separate=True)
        c_lut.ScalarRangeInitialized = 1.0

        c_lut.UseLogScale = 1 if self._use_log_scale else 0

        # set color preset
        c_lut.ApplyPreset(self._preset, True)

        # apply color to display
        pv.ColorBy(display, (self._field_type, self._field, self._component_title))

        if self._number_values != 0:
            # discretize color bar
            c_lut.Discretize = 1
            c_lut.NumberOfTableValues = self._number_values

        # Rescale transfer function
        if self._min_value is not None and self._max_value is not None:
            c_lut.RescaleTransferFunction(self._min_value, self._max_value)
        else:
            c_lut.RescaleTransferFunctionToDataRange(True)

        display.LookupTable = c_lut

        # set parameters of scalar bar (font, orientation, position, number format)
        scalar_bar = pv.GetScalarBar(c_lut)
        scalar_bar.SetPropertyWithName('Title', self._legend_title)
        scalar_bar.SetPropertyWithName('ComponentTitle', self._component_title)
        scalar_bar.SetPropertyWithName('TitleFontFamily', self._legend_font)
        scalar_bar.SetPropertyWithName('LabelFontFamily', self._legend_font)
        scalar_bar.SetPropertyWithName('TitleFontSize', self._title_font_size)
        scalar_bar.SetPropertyWithName('LabelFontSize', self._label_font_size)
        scalar_bar.SetPropertyWithName('Orientation', self._orientation)
        scalar_bar.SetPropertyWithName('WindowLocation', self._location)
        label_format_string = (
            '%' + str(self._legend_format_digits_before) + '.' +
            str(self._legend_format_digits_after) + self._legend_format_type
        )
        scalar_bar.SetPropertyWithName('RangeLabelFormat', label_format_string)
        scalar_bar.SetPropertyWithName('ScalarBarLength', self._size)

        # set visibility of color bar
        if not render:
            display.SetScalarBarVisibility(render_view, False)
        else:
            display.SetScalarBarVisibility(render_view, True)

        # define text labels
        # TODO: rewrite text labeling
        if self._text_left != '':
            text = pv.Text(registrationName='description')
            text.Text = self._text_left
            text_display = pv.Show(text, render_view, 'TextSourceRepresentation')
            text_display.SetPropertyWithName('WindowLocation', 'Any Location')
            text_display.Position = [0.05, 0.5]
            text_display.FontFamily = self._legend_font
            text_display.FontSize = self._text_font_size
        if self._text_right != '':
            text = pv.Text(registrationName='description')
            text.Text = self._text_right
            text_display = pv.Show(text, render_view, 'TextSourceRepresentation')
            text_display.SetPropertyWithName('WindowLocation', 'Any Location')
            text_display.Position = [0.9, 0.5]
            text_display.FontFamily = self._legend_font
            text_display.FontSize = self._text_font_size
        if self._text_upper != '':
            text = pv.Text(registrationName='description')
            text.Text = self._text_upper
            text_display = pv.Show(text, render_view, 'TextSourceRepresentation')
            text_display.SetPropertyWithName('WindowLocation', 'Upper Center')
            text_display.FontFamily = self._legend_font
            text_display.FontSize = self._text_font_size
        if self._text_lower != '':
            text = pv.Text(registrationName='description')
            text.Text = self._text_lower
            text_display = pv.Show(text, render_view, 'TextSourceRepresentation')
            text_display.SetPropertyWithName('WindowLocation', 'Lower Center')
            text_display.FontFamily = self._legend_font
            text_display.FontSize = self._text_font_size

    def get_field(self):
        return self._field
