#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /studioai/stats/inferential/base.py                                                 #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday August 22nd 2023 07:44:59 pm                                                #
# Modified   : Tuesday August 22nd 2023 08:28:51 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Base classes used throughout the inferential package."""
from __future__ import annotations
from abc import ABC, abstractmethod
import logging
from dataclasses import dataclass
import seaborn as sns

from studioai.stats.inferential.profile import StatTestProfile
from studioai.data.dataclass import DataClass
from studioai.service.io import IOService
from studioai.visual import Canvas

# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
ANALYSIS_TYPES = {
    "univariate": "Univariate",
    "bivariate": "Bivariate",
    "multivariate": "Multivariate",
}


# ------------------------------------------------------------------------------------------------ #
@dataclass
class StatTestResult(DataClass):
    test: str = None
    hypothesis: str = None
    H0: str = None
    statistic: str = None
    value: float = 0
    pvalue: float = 0
    inference: str = None
    alpha: float = 0.05
    result: str = None
    interpretation: str = None

    def __post_init__(self, canvas: Canvas) -> None:
        self._canvas = canvas
        sns.set_style(self._canvas.style)
        sns.set_palette(self._canvas.palette)

    @abstractmethod
    def plot(self, *args, **kwargs) -> None:
        """Renders plots of test statistics, pdf, cdf, data, etc..."""


# ------------------------------------------------------------------------------------------------ #
class StatisticalTest(ABC):
    """Base class for Statistical Tests"""

    def __init__(self, io: IOService = IOService, *args, **kwargs) -> None:
        self._io = io
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    @abstractmethod
    def profile(self) -> StatTestProfile:
        """Returns the statistical test profile."""

    @property
    @abstractmethod
    def result(self) -> StatTestResult:
        """Returns a Statistical Test Result object."""

    @abstractmethod
    def run(self) -> None:
        """Performs the statistical test and creates a result object."""

    def _report_pvalue(self, pvalue: float) -> str:
        """Rounds the pvalue in accordance with the APA Style Guide 7th Edition"""
        if pvalue < 0.001:
            return "p<.001"
        else:
            return "p=" + str(round(pvalue, 4))

    def _report_alpha(self) -> str:
        a = int(self._alpha * 100)
        return f"significant at {a}%."