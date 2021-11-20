# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2019.3
# Email : muyanru345@163.com
###################################################################

# Import third-party modules
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtSvg import QSvgRenderer
from qtpy.QtWidgets import *
import six


class MCacheDict(object):
    _render = QSvgRenderer()

    def __init__(self, cls):
        super(MCacheDict, self).__init__()
        self.cls = cls
        self._cache_pix_dict = {}

    def _render_svg(self, svg_path, replace_color=None):
        # Import local modules
        from dayu_widgets import dayu_theme

        replace_color = replace_color or dayu_theme.icon_color
        if (self.cls is QIcon) and (replace_color is None):
            return QIcon(svg_path)
        with open(svg_path, "r") as f:
            data_content = f.read()
            if replace_color is not None:
                data_content = data_content.replace("#555555", replace_color)
            self._render.load(QByteArray(six.b(data_content)))
            pix = QPixmap(128, 128)
            pix.fill(Qt.transparent)
            painter = QPainter(pix)
            self._render.render(painter)
            painter.end()
            if self.cls is QPixmap:
                return pix
            else:
                return self.cls(pix)

    def __call__(self, path, color=None):
        # Import local modules
        from dayu_widgets import utils

        full_path = utils.get_static_file(path)
        if full_path is None:
            return self.cls()
        key = "{}{}".format(full_path.lower(), color or "")
        pix_map = self._cache_pix_dict.get(key, None)
        if pix_map is None:
            if full_path.endswith("svg"):
                pix_map = self._render_svg(full_path, color)
            else:
                pix_map = self.cls(full_path)
            self._cache_pix_dict.update({key: pix_map})
        return pix_map


def get_scale_factor():
    standard_dpi = 96.0
    desktop = QApplication.desktop()
    if not desktop:
        return 1.0, 1.0
        # raise WindowsError("Please ensure have instance QApplication.")
    scale_factor_x = desktop.logicalDpiX() / standard_dpi
    scale_factor_y = desktop.logicalDpiY() / standard_dpi
    return scale_factor_x, scale_factor_y


MPixmap = MCacheDict(QPixmap)
MIcon = MCacheDict(QIcon)
