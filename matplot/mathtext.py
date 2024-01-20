"""
Copy from Matplotlib
Change by Asahi Qin

复制自Matplotlib库
Asahi Qin（作者）对此进行了修改，使其支持输出透明背景的图片与预处理一些不能被matplotlib直接渲染的latex
"""

import matplotlib
from matplotlib.mathtext import MathTextParser


def math_to_image(s, filename_or_obj, prop=None, dpi=None, format=None,
                  *, color=None, transparent=None):
    """
    Given a math expression, renders it in a closely-clipped bounding
    box to an image file.

    Parameters
    ----------
    s : str
        A math expression.  The math portion must be enclosed in dollar signs.
    filename_or_obj : str or path-like or file-like
        Where to write the image data.
    prop : `.FontProperties`, optional
        The size and style of the text.
    dpi : float, optional
        The output dpi.  If not set, the dpi is determined as for
        `.Figure.savefig`.
    format : str, optional
        The output format, e.g., 'svg', 'pdf', 'ps' or 'png'.  If not set, the
        format is determined as for `.Figure.savefig`.
    color : str, optional
        Foreground color, defaults to :rc:`text.color`.
    transparent : bool, optional
        Decide the image's background
    """
    from matplotlib import figure
    # 预处理不能渲染的latex关键字（即直接移除）
    s = s.replace(r"\mathopen{}\left",r"\left")
    s = s.replace(r"\mathclose{}\right",r"\right")
    parser = MathTextParser('path')
    width, height, depth, _, _ = parser.parse(s, dpi=72, prop=prop)

    fig = figure.Figure(figsize=(width / 72.0, height / 72.0))
    fig.text(0, depth / height, s, fontproperties=prop, color=color)
    fig.savefig(filename_or_obj, dpi=dpi, format=format, transparent=transparent)
