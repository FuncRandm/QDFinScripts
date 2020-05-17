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
import math
import sys
import os

sys.path.append( os.path.join( os.path.dirname( __file__ ), '..', 'Scripts' ))

from QDFinConstants import DAYS_IN_YEAR
from QDFinConstants import ACT365_DAYS_IN_YEAR

from QDFinInterest import simpleInterest
from QDFinInterest import complexInterest
from QDFinInterest import complexInterestRate
from QDFinInterest import effectiveRate
from QDFinInterest import dailyEffectiveRate
from QDFinInterest import effectiveRateRatioAtMaturity
from QDFinInterest import nominalRate
from QDFinInterest import continuouslyCompoundedRate
from QDFinInterest import effectiveRateFromContinuallyCompoundedRate
from QDFinInterest import convertRateToBondMarketBasis
from QDFinInterest import convertRateToMoneyMarketBasis
from QDFinInterest import convertRatioToRate

class InterestTests(unittest.TestCase):
	def testGetSimpleInterestAt5PercentOver123Days(self):
		self.assertAlmostEqual(simpleInterest(100.0, 5, 123), 101.68, 2);

	def testGetSimpleInterestAt5PercentOver1Day(self):
		self.assertAlmostEqual(simpleInterest(100.0, 5, 1), 100.01, 2);
	
	def testGetComplexInterestAt5PercentOver5Years(self):
		self.assertAlmostEqual(complexInterest(100.0, 5, 5), 127.63, 2);
	
	def testGetComplexInterestAt5PercentOverOneYear(self):
		self.assertAlmostEqual(complexInterest(100.0, 5, 1), 105.0, 2);
	
	def testGetComplexInterestAt5PercentOverZeroYears(self):
		self.assertAlmostEqual(complexInterest(100.0, 5, 0), 100.0, 2);
	
	def testGetEffectiveRateAt5PercentForOneYearQuarterlyInterest(self):
		self.assertAlmostEqual(effectiveRate(5, 4), 5.0945, 4);
	
	def testGetNominalRateAt5PercentYearlyInterestForASingleQuarter(self):
		self.assertAlmostEqual(nominalRate(5,4), 4.9089, 4);
	
	def testGetEffectiveRateFor123DayInvestment(self):
		self.assertAlmostEqual(effectiveRate(5.8, DAYS_IN_YEAR()/123),  5.9122, 4);
	
	def testGetDailyEffectiveRateFor123DayInvestment(self):
		self.assertAlmostEqual(dailyEffectiveRate(5.8, 123), 5.7445, 4);
	
	def testGetContinuouslyCompoundedRateFor123DayInvestment(self):
		self.assertAlmostEqual(continuouslyCompoundedRate(5.8, 123), 5.7440, 4);
	
	def testGetEffectiveRateFromContinuouslyCompoundedRateOf5Point8(self):
		self.assertAlmostEqual(effectiveRateFromContinuallyCompoundedRate(5.8), 5.9715, 4);
	
	def testGetMoneyMarketBasisFromBondMarketBasis(self):
		self.assertAlmostEqual(convertRateToMoneyMarketBasis(8.1111), 8.0, 4);
	
	def testGetBondMarketBasisFromMoneyMarketBasis(self):
		self.assertAlmostEqual(convertRateToBondMarketBasis(8.0), 8.1111, 4);
	
	def testGetEffectiveRateInMoneyMarketBasis(self):
		rate = effectiveRateRatioAtMaturity(convertRatioToRate(100/95), 123);
		self.assertAlmostEqual(convertRateToMoneyMarketBasis(rate), 16.2155, 4);
	
testSuite = unittest.TestLoader().loadTestsFromTestCase(InterestTests);

print(testSuite);

unittest.TextTestRunner(verbosity=3).run(testSuite);
