#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /studioai/stats/descriptive/categorical.py                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday June 8th 2023 02:56:56 am                                                  #
# Modified   : Wednesday August 23rd 2023 12:43:49 am                                              #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass

import statistics
from typing import Union

import pandas as pd
import numpy as np

from studioai.data.dataclass import DataClass


# ------------------------------------------------------------------------------------------------ #
@dataclass
class CategoricalStats(DataClass):
    name: str  # Name of variable
    length: int  # total  length of variable
    count: int  # number of non-null values
    size: float  # total number of bytes
    mode: Union[int, str]
    unique: int

    @classmethod
    def describe(cls, x: Union[pd.Series, np.ndarray], name: str = None) -> None:
        name = name or cls.get_name(x=x)
        return cls(
            name=name,
            length=len(x),
            count=len(list(filter(None, x))),
            size=x.__sizeof__(),
            mode=statistics.mode(x),
            unique=len(np.unique(x)),
        )
