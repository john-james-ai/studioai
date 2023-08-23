#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /conftest.py                                                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday May 26th 2023 11:12:03 pm                                                    #
# Modified   : Wednesday August 23rd 2023 07:24:33 am                                              #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import pytest
import pandas as pd
from datetime import datetime
import logging
from dataclasses import dataclass

import numpy as np

from studioai.data.dataclass import DataClass

# ------------------------------------------------------------------------------------------------ #
logging.getLogger("matplotlib").setLevel(logging.WARNING)
# ------------------------------------------------------------------------------------------------ #
DATAFILE = "data/Credit Score Classification Dataset.csv"

# ------------------------------------------------------------------------------------------------ #
collect_ignore_glob = []


# ------------------------------------------------------------------------------------------------ #
#                                      DATACLASS                                                   #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class TestDataClass(DataClass):
    name: str = "test"
    size: int = 8329
    length: float = 920932.98
    dt: datetime = datetime.now()


# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="function", autouse=False)
def dataset():
    df = pd.read_csv(DATAFILE, index_col=None)
    df = df.astype(
        {
            "Gender": "category",
            "Age": np.int64,
            "Income": np.int64,
            "Children": np.int64,
            "Marital Status": "object",
            "Credit Rating": "category",
            "Education": "category",
        }
    )
    return df


# ------------------------------------------------------------------------------------------------ #
#                                     DATACLASS                                                    #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def dataklass():
    return TestDataClass()
