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
# Modified   : Monday May 20th 2024 03:49:49 am                                                    #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging
from dataclasses import dataclass
from datetime import datetime

import numpy as np
import pandas as pd
import pytest
from pyspark.sql import SparkSession

from studioai import DataClass

# ------------------------------------------------------------------------------------------------ #
logging.getLogger("matplotlib").setLevel(logging.WARNING)
# ------------------------------------------------------------------------------------------------ #
CREDIT_FP = "data/Credit Score Classification Dataset.csv"
CASES_FP = "data/calc_cases.csv"

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
#                                         CREDIT DATA                                              #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="function", autouse=False)
def credit():
    df = pd.read_csv(CREDIT_FP, index_col=None)
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
@pytest.fixture(scope="function", autouse=False)
def cases():
    return pd.read_csv(CASES_FP, index_col=None)


# ------------------------------------------------------------------------------------------------ #
#                                     DATACLASS                                                    #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def dataklass():
    return TestDataClass()


# ------------------------------------------------------------------------------------------------ #
#                                       SPARK SESSION                                              #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def spark():
    spark = SparkSession.builder \
    .appName("AppInsight") \
    .master("local[*]") \
    .config("spark.driver.memory", "16G") \
    .config("spark.executor.memory", "16G") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.kryoserializer.buffer.max", "2000M") \
    .config("spark.driver.maxResultSize", "0") \
    .config("spark.jars.packages", "com.johnsnowlabs.nlp:spark-nlp_2.12:5.3.3") \
    .config("spark.sql.legacy.parquet.nanosAsLong", "true") \
    .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark