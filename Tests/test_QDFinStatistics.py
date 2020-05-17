#!/usr/bin/env python3
#
#   Copyright 2018 Nic Ho Chee
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

__author__ = "Nic Ho Chee"
__copyright__ = "Copyright 2018 Nic Ho Chee"
__credits__ = ["Nic Ho Chee"]
__license__ = "Apache License 2.0"
__maintainer__ = "Nic Ho Chee"
__twitter__ = "@funcrandm"
__email__ = "dev@bedtimecomics.com"
__status__ = "Development" 
__version__ = "0.1.0"

import unittest
import sys
import os

sys.path.append( os.path.join( os.path.dirname( __file__ ), '..', 'Scripts' ))

from QDFinStatistics import linearInterpolation
from QDFinStatistics import logInterpolation
from QDFinStatistics import mean
from QDFinStatistics import variance
from QDFinStatistics import standardDeviation
from QDFinStatistics import historicVolatility
from QDFinStatistics import correlationCoefficient
from QDFinStatistics import covariance
from QDFinStatistics import fastCovariance
from QDFinStatistics import gaussian

class StatisticsTests(unittest.TestCase):
	def testLinearInterpolationBetween3mAnd5m(self):
		self.assertAlmostEqual(linearInterpolation(5.1, 5.5, 92, 153, 112), 5.2311, 4);

	def testLinearInterpolationPast5m(self):
		self.assertAlmostEqual(linearInterpolation(5.1, 5.5, 92, 153, 163), 5.5656, 4);
	
	def testLogInterpolationBetween3mAnd5m(self):
		self.assertAlmostEqual(logInterpolation(5.1, 5.5, 92, 153, 112), 5.2278, 4);
	
	def testVarianceOf10PositiveNumbers(self):
		self.assertAlmostEqual(variance([110, 32, 85, 99, 100, 92, 93, 99, 34, 70]), 686.04, 2);
	
	def testStandardDeviationOf10PositiveNumbers(self):
		self.assertAlmostEqual(standardDeviation([110, 32, 85, 99, 100, 92, 93, 99, 34, 70]), 26.19, 2);
	
	def testHistoricVolatilityOf10PositiveNumbers(self):
		self.assertAlmostEqual(historicVolatility([1.6520, 1.7342, 1.7490, 1.7640, 1.7850, 1.8890, 1.8980, 1.9230, 1.9450, 1.9540]), 31.0603, 1);
	
	def testCorrelationOf5DataPoints(self):
		self.assertAlmostEqual(correlationCoefficient([150, 155, 148, 147, 157],[25, 30, 24, 23, 32]), 0.9967, 4);
	
	def testCovarianceOf5DataPoints(self):
		self.assertAlmostEqual(covariance([150, 155, 148, 147, 157],[25, 30, 24, 23, 32]), 17.35, 2);
	
	def testCovarianceCalculationsGiveTheSameResult(self):
		self.assertAlmostEqual(covariance([150, 155, 148, 147, 157],[25, 30, 24, 23, 32]), fastCovariance([150, 155, 148, 147, 157],[25, 30, 24, 23, 32]), 2);
	
	def testGaussianCurveGenerator(self):
		inputs = [-4, -3, -2, -1, 0, 1, 2, 3, 4];
		outputs = [0.0001, 0.0044, 0.0540, 0.2420, 0.3989, 0.2420, 0.0540, 0.0044, 0.0001];
		numItems = len(inputs);
		for item in range(numItems):
			self.assertAlmostEqual(gaussian(inputs[item]), outputs[item], 4);

testSuite = unittest.TestLoader().loadTestsFromTestCase(StatisticsTests);

print(testSuite);

unittest.TextTestRunner(verbosity=3).run(testSuite);
