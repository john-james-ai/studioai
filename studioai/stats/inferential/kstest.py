#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /studioai/stats/inferential/kstest.py                                               #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday June 6th 2023 01:45:05 am                                                   #
# Modified   : Friday September 1st 2023 03:36:51 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass
from typing import Union

import numpy as np
from scipy import stats
from dependency_injector.wiring import inject, Provide

from studioai.container import StudioAIContainer
from studioai.visual.seaborn import Visualizer
from studioai.stats.inferential.profile import StatTestProfile
from studioai.stats.inferential.base import (
    StatTestResult,
    StatisticalTest,
)


# ------------------------------------------------------------------------------------------------ #
#                                     TEST RESULT                                                  #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class KSTestResult(StatTestResult):
    """Encapsulates the hypothesis test results."""

    a: np.ndarray = None
    b: Union[np.ndarray, str] = None

    @inject
    def __post_init__(self, visualizer: Visualizer = Provide[StudioAIContainer.seaborn]) -> None:
        self.visualizer = visualizer

    def plot(self) -> None:  # pragma: no cover
        self.visualizer.kstestplot(
            statistic=self.value, n=len(self.a), result=self.result, alpha=self.alpha
        )


# ------------------------------------------------------------------------------------------------ #
#                                          TEST                                                    #
# ------------------------------------------------------------------------------------------------ #
class KSTest(StatisticalTest):
    """Performs the (one-sample or two-sample) Kolmogorov-Smirnov test for goodness of fit.

    The one-sample test compares the underlying distribution F(x) of a sample against a given
    distribution G(x). The two-sample test compares the underlying distributions of
    two independent samples. Both tests are valid only for continuous distributions.

    Args:
        a (np.ndarray): 1D Numpy array of data to be tested.
        b (Union[str, np.ndarray]): A 1-D array, or a string containing the name of the
            reference distribution from the scipy list of Continuous Distributions
            at https://docs.scipy.org/doc/scipy/reference/stats.html
        a_name (str): The name of the sample distribution. Optional.
        b_name (str): The name of the sample 2 distribution, if two-sample test. Optional.

    """

    __id = "kstest"

    def __init__(
        self,
        a: np.ndarray,
        b: Union[str, np.ndarray],
        alpha: float = 0.05,
    ) -> None:
        super().__init__()
        self._a = a
        self._b = b
        self._alpha = alpha
        self._profile = StatTestProfile.create(self.__id)
        self._result = None

    @property
    def profile(self) -> StatTestProfile:
        """Returns the statistical test profile."""
        return self._profile

    @property
    def result(self) -> StatTestResult:
        """Returns a Statistical Test Result object."""
        return self._result

    def run(self) -> None:
        """Performs the statistical test and creates a result object."""

        n = len(self._a)

        # Conduct the two-sided ks test
        try:
            result = stats.kstest(rvs=self._a, cdf=self._b, alternative="two-sided")
        except (
            AttributeError
        ) as e:  # pragma: no cover - actually pytest-coverage not picking this up.
            msg = f"Distribution {self._reference_distribution} is not supported.\n{e}"
            self._logger.exception(msg)
            raise

        inference = self._infer(pvalue=result.pvalue)

        interpretation = None
        if len(self._a) < 50:
            interpretation = "Note: The Kolmogorov-Smirnov Test requires a sample size N > 50. For smaller sample sizes, the Shapiro-Wilk test should be considered."
        if len(self._a) > 1000:
            interpretation = "Note: The Kolmogorov-Smirnov Test on large sample sizes may lead to rejections of the null hypothesis that are statistically significant, yet practically insignificant."

        # Create the result object.
        self._result = KSTestResult(
            test=self._profile.name,
            H0=self._profile.H0,
            statistic=self._profile.statistic,
            hypothesis=self._profile.hypothesis,
            value=result.statistic,
            pvalue=result.pvalue,
            result=self._report_results(n=n, statistic=result.statistic, pvalue=result.pvalue),
            a=self._a,
            b=self._b,
            inference=inference,
            interpretation=interpretation,
            alpha=self._alpha,
        )

    def _infer(self, pvalue: float) -> str:  # pragma: no cover
        """Formats the inference for the hypothesis based upon whether it is one or two sample"""
        if isinstance(self._b, str):
            if pvalue > self._alpha:
                inference = f"The pvalue {round(pvalue,2)} is greater than level of significance {int(self._alpha*100)}%; therefore, the null hypothesis is not rejected. The evidence against the data being drawn from the {self._b} is not significant."
            else:
                inference = f"The pvalue {round(pvalue,2)} is less than level of significance {int(self._alpha*100)}%; therefore, the null hypothesis is rejected. The evidence against the data being drawn from the {self._b} is significant."
        else:
            if pvalue > self._alpha:
                inference = f"The pvalue {round(pvalue,2)} is greater than level of significance {int(self._alpha*100)}%; therefore, the null hypothesis is not rejected. The evidence against the data being drawn from the same distribution is not significant."
            else:
                inference = f"The pvalue {round(pvalue,2)} is less than level of significance {int(self._alpha*100)}%; therefore, the null hypothesis is rejected. The evidence against the data being drawn from the same distribution is significant."
        return inference

    def _report_results(self, n: int, statistic: float, pvalue: float) -> str:
        """Reports the result in APA style."""
        result = (
            f"Kolmogorov-Smirnov Goodness of Fit\nD({n})={round(statistic,4)}, p={round(pvalue,3)}"
        )
        return result
