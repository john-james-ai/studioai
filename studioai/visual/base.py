#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /studioai/visual/base.py                                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday May 28th 2023 06:23:03 pm                                                    #
# Modified   : Wednesday August 23rd 2023 11:36:59 am                                              #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from abc import ABC, abstractmethod, abstractclassmethod
from dataclasses import dataclass

from dependency_injector.wiring import inject, Provide
import numpy as np

from studioai.data.dataclass import DataClass


# ------------------------------------------------------------------------------------------------ #
#                                           CANVAS                                                 #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class Canvas(DataClass):  # pragma: no
    """Namespace for Canvas configuration subclasses"""

    @abstractclassmethod
    def create(cls, nplots: int = 1, size: tuple = {12, 4}) -> Canvas:
        """Creates a Canvas instance"""


# ------------------------------------------------------------------------------------------------ #
#                                       VISUALIZER                                                 #
# ------------------------------------------------------------------------------------------------ #
class Visualizer(ABC):  # pragma: no cover
    """Defines blueprint for vendor-based visualization subclasses.


    Args:
        canvas (Canvas): A dataclass containing the configuration of the canvas
            for the visualization.
    """

    @abstractmethod
    def __init__(self, canvas: Canvas, *args, **kwargs) -> None:  # pragma: no cover
        """Defines the construction requirement for Visualizers"""

    @abstractmethod
    def lineplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def boxplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def kdeplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def ecdfplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def histogram(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def scatterplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def barplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""


# ------------------------------------------------------------------------------------------------ #
#                                          PLOT                                                    #
# ------------------------------------------------------------------------------------------------ #
class Plot(ABC):
    """Abstract Plotizations Class"""

    def __init__(self) -> None:
        self._canvas = None

    def set_or_canvas(self, canvas: Canvas = None) -> None:
        """Sets the canvas or creates the canvas upon which the plot is rendered.

        Args:
            canvas (Canvas): Canvas object.
        """
        self._canvas = canvas or Canvas.create()

    @abstractmethod
    def plot(self, *args, **kwargs) -> None:
        """Renders the plot"""

    def add_fill(
        self,
        x: np.ndarray,
        y1: float,
        y2: np.ndarray,
        color: str = None,
        where: np.ndarray = None,
    ) -> None:



# ------------------------------------------------------------------------------------------------ #
#                                       PLOTBUILDER                                                #
# ------------------------------------------------------------------------------------------------ #
class PlotBuilder(ABC):
    @inject
    def __init__(self, canvas: Canvas = Provide[VisualContainer.canvas]) -> None:
        self._canvas = canvas
        self._plot = None
        self._reset()

    @property
    @abstractmethod
    def plot(self) -> Plot:
        """Returns the plot object"""

    @abstractmethod
    def reset(self) -> None:
        """Instantiates a fresh plot blank plot object"""

    @abstractmethod
    def build_canvas(self, size: tuple = (12, 4), **kwargs) -> None:
        """Installs the canvas upon which the plot will be rendered into the plot."""

    @abstractmethod
    def build_plot(self, *args, **kwargs) -> None:
        """Constructs the core plot."""

    def add_fill(
        self,
        x: np.ndarray,
        y1: float,
        y2: np.ndarray,
        color: str = None,
        where: np.ndarray = None,
        **kwargs,
    ) -> None:
        """Adds a fill region to the plot

        Args:
            x (np.ndarray): The x coordinates of the nodes defining the curves.
            y1 (Union[int,float,np.ndarray]): Scaler or the y coordinates of the points defining the first curve
            y2 (Union[int,float,np.ndarray]): Scaler or the y coordinates of the points defining the second curve.
            where (np.ndarray): Boolean mask indicating horizontal (x) regions that should be included/excluded from being filled.
            color (Union[str, tuple]): Fill color.
            **kwargs: Additional kwargs

        """
        self._plot.add_fill(x=x, y1=y1, y2=y2, where=where, color=color, ax=self._ax, **kwargs)

    def add_annotation(
        self,
        text: str,
        xy: tuple(float, float),
        xytext: tuple(float, float),
        textcoords: str = "offset_points",
        ha: str = "center",
        **kwargs,
    ) -> None:
        """Adds an annotation object to the plot

        Args:
            text (str): The text for the annotation
            xy (tuple(float,float)): Tuple containing the coordinates for the annotation, relative to data
            xytext (tuple(float,float)): Tuple containing the coordinates for the text
            textcoords (str): Whether the xytext is measurement of points or pixels.
            **kwargs: Additional kwargs

        """
        self._plot.add_annotate(
            text=text, xy=xy, xytext=xytext, textcoords=textcoords, ha=ha, ax=self._ax, **kwargs
        )

    def add_text(
        self,
        x: float,
        y: float,
        text: str,
        fontsize: float = None,
        ha: str = "center",
        va: str = "center",
        **kwargs,
    ) -> None:
        """Adds text to the plot

        Args:
            x (float): Position of text on the x dimension in data coordinates.
            y (float): Position of text on the y dimension in data coordinates.
            text (str): The text string
            ha (str): Horizontal alignment of text relative to its position.
            va (str): Vertical alignment of text relative to its position.
            **kwargs: Additional kwargs
        """
        self._plot.add_text(x=x, y=y, s=text, ha=ha, va=va, ax=self._ax, **kwargs)

    def add_point(self, x: float, y: float, size: float = 100, color: str = None, **kwargs) -> None:
        """Adds a point to the plot

        Args:
            x (float): Position of the point on the x dimension in data coordinates.
            y (float): Position of the point on the y dimension in data coordinates.
            size (float): Size of point in pixels
            color (str): Color of the point.

        """
        self._plot.add_point(x, x, size=size, color=color, ax=self._ax, **kwargs)

    def add_title(self, title: str, fontsize: float = None, **kwargs) -> None:
        """Adds a title to the plot.

        Args:
            title (str): The title
            fontsize (float): Size of font.
        """
        self._plot.add_title(title=title, fontsize=fontsize, ax=self._ax, **kwargs)
