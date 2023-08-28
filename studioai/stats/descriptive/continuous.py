#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /studioai/stats/descriptive/continuous.py                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday June 8th 2023 02:56:56 am                                                  #
# Modified   : Saturday August 26th 2023 11:03:56 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass
from typing import Union
import logging

import pandas as pd
import numpy as np
from scipy import stats

from studioai.data.dataclass import DataClass

# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------------------------ #
@dataclass
class ContinuousStats(DataClass):
    name: str  # Name of the variable
    length: int  # total  length of variable
    count: int  # number of non-null values
    size: int  # total number of bytes
    min: float
    q25: float
    mean: float
    median: float
    q75: float
    max: float
    range: float
    std: float
    var: float
    skew: float
    kurtosis: float

    @classmethod
    def describe(cls, x: Union[pd.Series, np.ndarray], name: str = None) -> None:
        return cls(
            name=name,
            length=len(x),
            count=len(list(filter(None, x))),
            size=x.__sizeof__(),
            mean=np.mean(x),
            std=np.std(x),
            var=np.var(x),
            min=np.min(x),
            q25=np.percentile(x, q=25),
            median=np.median(x),
            q75=np.percentile(x, q=75),
            max=np.max(x),
            range=np.max(x) - np.min(x),
            skew=stats.skew(x),
            kurtosis=stats.kurtosis(x, bias=False),
        )
