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

from QDFinTimeValueMoney import complexFutureValue
from QDFinTimeValueMoney import simpleFutureValue
from QDFinTimeValueMoney import complexPresentValue
from QDFinTimeValueMoney import simplePresentValue
from QDFinTimeValueMoney import simpleYield
from QDFinTimeValueMoney import complexYield
from QDFinTimeValueMoney import simpleDiscountFactor
from QDFinTimeValueMoney import complexDiscountFactor
from QDFinTimeValueMoney import continuouslyCompoundedDiscountFactor
from QDFinTimeValueMoney import netPresentValueOfCashflows
from QDFinTimeValueMoney import internalRateOfReturnOfCashflows
from QDFinTimeValueMoney import internalRateOfReturnOfCashflowsWithDates
from QDFinInterest import convertRateToMoneyMarketBasis

class TimeValueOfMoneyTests(unittest.TestCase):
	
	def testGetFutureValueIn7YearsAt8PercentPA(self):
		self.assertAlmostEqual(complexFutureValue(120, 8, 7), 205.6589, 2);

	def testGetFutureValueIn123DaysAt9PercentPA(self):
		self.assertAlmostEqual(simpleFutureValue(120, 9, 123), 123.6394, 2);
	
	def testGetPresentValueFrom3YearsAt8PercentPA(self):
		self.assertAlmostEqual(complexPresentValue(240, 8, 3), 190.5197, 2);
	
	def testGetPresentValueFrom321DaysAt9PercentPA(self):
		self.assertAlmostEqual(simplePresentValue(240, 9, 321), 222.3971, 2);
	
	def testGetYieldAt42Days(self):
		self.assertAlmostEqual(simpleYield(100.0, 112.23, 42), 106.2845, 4);
	
	def testGetYieldAt5Years(self):
		self.assertAlmostEqual(complexYield(100.00, 132.23, 5), 5.7465, 4);
	
	def testGetDiscountFactorFor123Days(self):
		self.assertAlmostEqual(simpleDiscountFactor(7.5, 123), 0.9753, 4);
	
	def testGetDiscountFactorFor5Years(self):
		self.assertAlmostEqual(complexDiscountFactor(7.5, 5), 0.6966, 4);
	
	def testGetContinuouslyCompoundedDiscountFactorFor100Days(self):
		self.assertAlmostEqual(continuouslyCompoundedDiscountFactor(9, 47), 0.9885, 4);
	
	def testGetNetPresentValueOfFiveCashflowsWithDiscountingRate5Point8(self):
		self.assertAlmostEqual(netPresentValueOfCashflows([130, 42, -58, 18, -44], 5.8), 92.5945, 4);
	
	def testGetInternalRateOfReturnOfFiveCashflows(self):
		self.assertAlmostEqual(internalRateOfReturnOfCashflows(1300, [100, -200, 1100, 350]), 1.1654, 4);
	
	def testGetInternalRateOfReturnOfFive1yCashflows(self):
		self.assertAlmostEqual(internalRateOfReturnOfCashflowsWithDates(1300, [100, -200, 1100, 350], [1, 2, 3, 4]), 1.1654, 4);
	
	def testGetInternalRateOfReturnOfFive6mCashflows(self):
		self.assertAlmostEqual(internalRateOfReturnOfCashflowsWithDates(1300, [1000, -200, 300, 400], [0.5, 1.0, 1.5, 2.0]), 15.3945, 4);
	
	def testGetSimpleYieldInMoneyMarketBasis(self):
		self.assertAlmostEqual(convertRateToMoneyMarketBasis(simpleYield(36, 39, 123)), 24.3902, 4);

testSuite = unittest.TestLoader().loadTestsFromTestCase(TimeValueOfMoneyTests);

print(testSuite);

unittest.TextTestRunner(verbosity=3).run(testSuite);
