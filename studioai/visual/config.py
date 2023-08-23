#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /studioai/visual/config.py                                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday August 22nd 2023 06:53:54 pm                                                #
# Modified   : Wednesday August 23rd 2023 09:53:26 am                                              #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import math
from dataclasses import dataclass, field
from typing import List, Union, Tuple

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns

from studioai.data.dataclass import DataClass
from studioai.visual.base import Canvas as BaseCanvas


# ------------------------------------------------------------------------------------------------ #
#                                           COLORS                                                 #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class Colors(DataClass):
    cool_black: str = "#002B5B"
    police_blue: str = "#2B4865"
    teal_blue: str = "#256D85"
    pale_robin_egg_blue: str = "#8FE3CF"
    russian_violet: str = "#231955"
    dark_cornflower_blue: str = "#1F4690"
    meat_brown: str = "#E8AA42"
    peach: str = "#FFE5B4"
    dark_blue: str = "#002B5B"
    blue: str = "#1F4690"
    orange: str = "#E8AA42"
    crimson: str = "#BA0020"

    def __post_init__(self) -> None:
        return


# ------------------------------------------------------------------------------------------------ #
#                                            PALETTES                                              #
# ------------------------------------------------------------------------------------------------ #
SEABORN_PALETTES = {
    "darkblue": sns.dark_palette("#69d", reverse=False, as_cmap=False),
    "darkblue_r": sns.dark_palette("#69d", reverse=True, as_cmap=False),
    "winter_blue": sns.color_palette(
        [Colors.cool_black, Colors.police_blue, Colors.teal_blue, Colors.pale_robin_egg_blue],
        as_cmap=True,
    ),
    "blue_orange": sns.color_palette(
        [Colors.russian_violet, Colors.dark_cornflower_blue, Colors.meat_brown, Colors.peach],
        as_cmap=True,
    ),
}


@dataclass
class Palettes(DataClass):
    blues: str = "Blues"
    blues_r: str = "Blues_r"
    mako: str = "mako"
    bluegreen: str = "crest"
    paired: str = "Paired"
    dark: str = "dark"
    colorblind: str = "colorblind"
    seaborn_palettes: dict = field(default_factory=dict)


# ------------------------------------------------------------------------------------------------ #
#                                            CANVAS                                                #
# ------------------------------------------------------------------------------------------------ #


@dataclass
class Canvas(BaseCanvas):
    """SeabornCanvas class encapsulating figure level configuration."""

    width: int = 12  # The maximum width of the canvas
    height: int = 4  # The height of a single row.
    maxcols: int = 2  # The maximum number of columns in a multi-plot visualization.
    palette: str = "Blues_r"  # Seaborn palette or matplotlib colormap
    style: str = "whitegrid"  # A Seaborn aesthetic
    saturation: float = 0.5
    fontsize: int = 10
    fontsize_title: int = 12
    colors: Colors = Colors()
    palettes: Palettes = Palettes()

    def get_figaxes(
        self, nplots: int = 1, figsize: tuple = None
    ) -> Tuple[plt.Figure, Union[plt.Axes, List[plt.Axes]]]:  # pragma no cover
        """Configures the figure and axes objects.

        Args:
            nplots (int): The number of plots to be rendered on the canvas.
            figsize (tuple[int,int]): Plot width and row height.
        """
        figsize = figsize or (self.width, self.height)

        if nplots == 1:
            fig, axes = plt.subplots(figsize=figsize)
        else:
            nrows = math.ceil(nplots / self.maxcols)
            ncols = min(self.maxcols, nplots)

            fig = plt.figure(layout="constrained", figsize=figsize)
            gs = GridSpec(nrows=nrows, ncols=ncols, figure=fig)

            axes = []
            for idx in range(nplots):
                row = int(idx / ncols)
                col = idx % ncols

                if idx < nplots - 1:
                    ax = fig.add_subplot(gs[row, col])
                else:
                    ax = fig.add_subplot(gs[row, col:])
                axes.append(ax)

        return fig, axes
