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

from QDFinConstants import ACT365_DAYS_IN_YEAR
from QDFinConstants import ACT360_DAYS_IN_YEAR
from QDFinConstants import ACTACT_DAYS_IN_YEAR

from QDFinTimeValueMoney import internalRateOfReturnOfCashflowsWithDates

from QDFinInterestRateInstruments import forwardForwardRate
from QDFinInterestRateInstruments import forwardRateAgreementSettlementPrice
from QDFinInterestRateInstruments import forwardRateAgreementSettlementPriceFromFuturePrice
from QDFinInterestRateInstruments import interestRateStrip
from QDFinInterestRateInstruments import interestRateFuturePriceChange
from QDFinInterestRateInstruments import interestRateFutureNumberContracts
from QDFinInterestRateInstruments import forwardForwardRateFromInterpolation
from QDFinInterestRateInstruments import interestRateFutureNumberContractsFromInterpolation
from QDFinInterestRateInstruments import dirtyBondPrice
from QDFinInterestRateInstruments import dirtyBondPriceForCalculators
from QDFinInterestRateInstruments import bondAccruedInterest
from QDFinInterestRateInstruments import cleanBondPrice
from QDFinInterestRateInstruments import cleanBondPriceExDividend
from QDFinInterestRateInstruments import bondCurrentYield
from QDFinInterestRateInstruments import bondSimpleYieldToMaturity
from QDFinInterestRateInstruments import bondYieldToMaturity
from QDFinInterestRateInstruments import bondComplexYieldFromFinalCoupon
from QDFinInterestRateInstruments import bondSimpleYieldFromFinalCoupon
from QDFinInterestRateInstruments import bondPriceUsingMoneyMarketYield
from QDFinInterestRateInstruments import bondPriceUsingMoneyMarketYieldForCalculators
from QDFinInterestRateInstruments import bondMoneyMarketYield
from QDFinInterestRateInstruments import bondPriceUsingMoosmullerYield
from QDFinInterestRateInstruments import bondPriceStrippedCoupon
from QDFinInterestRateInstruments import bondDuration
from QDFinInterestRateInstruments import bondModifiedDuration
from QDFinInterestRateInstruments import bondConvexity
from QDFinInterestRateInstruments import bondPriceChange
from QDFinInterestRateInstruments import bondPriceChangeUsingConvexity
from QDFinInterestRateInstruments import bondHedgeUsingModifiedDuration
from QDFinInterestRateInstruments import bondFuturesPrice
from QDFinInterestRateInstruments import bondFuturesHedgeNotional
from QDFinInterestRateInstruments import bondImpliedRepoRate
from QDFinInterestRateInstruments import bondCashAndCarryArbitrage
from QDFinInterestRateInstruments import bondYieldZeroCoupon

class InterestRateInstrumentsTests(unittest.TestCase):
	def testForwardForwardRate(self):
		self.assertAlmostEqual(forwardForwardRate(10, 12, 30, 90), 12.8940, 4);

	def testFRASettlementPrice(self):
		self.assertAlmostEqual(forwardRateAgreementSettlementPrice(1000000, 3, 1.5, 100, ACT360_DAYS_IN_YEAR()), 4149.38, 2);
	
	def testFRASettlementPriceFromFuture(self):
		self.assertAlmostEqual(forwardRateAgreementSettlementPriceFromFuturePrice(1000000, 95.25, 6.5, 100, ACT360_DAYS_IN_YEAR()), -4774.90, 2);
	
	def testBondAccruedCoupon(self):
		self.assertAlmostEqual(bondAccruedInterest(100, 6, 260, ACT360_DAYS_IN_YEAR()), 4.3333, 4);
	
	def testCleanBondPrice(self):
		self.assertAlmostEqual(cleanBondPrice(100, 6, 3, 1, 9, 260, 100, ACT360_DAYS_IN_YEAR(), ACT360_DAYS_IN_YEAR()), 121.69, 2);
	
	def testCleanBondPriceNoAccrued(self):
		self.assertAlmostEqual(cleanBondPrice(100, 6, 3, 1, 9, 0, 100, ACT360_DAYS_IN_YEAR()), dirtyBondPrice(100, 6, 3, 1, 9, 100, ACT360_DAYS_IN_YEAR()), 2);
	
	def testCleanBondPriceExDividend(self):
		self.assertAlmostEqual(cleanBondPriceExDividend(100, 6, 3, 1, 9, 4, ACT360_DAYS_IN_YEAR()), 127.08, 2);
	
	def testDirtyBondPrice(self):
		self.assertAlmostEqual(dirtyBondPrice(100, 6, 3, 1, 9, 100, ACT360_DAYS_IN_YEAR()), 126.0201, 4);
	
	def testDirtyBondPriceFormulationResults(self):
		self.assertAlmostEqual(dirtyBondPrice(100, 6, 3, 1, 9, 100, ACT360_DAYS_IN_YEAR()), dirtyBondPriceForCalculators(100, 6, 3, 1, 9, 100, ACT360_DAYS_IN_YEAR()), 4);
	
	def testInterestRateStrip(self):
		self.assertAlmostEqual(interestRateStrip([3.5, 3.8, 4.2], [31, 31, 30]), 3.8417, 4);
	
	def testPriceChangeForInterestRateFuture(self):
		self.assertAlmostEqual(interestRateFuturePriceChange(3000000, 1, 0.005, 3), 37.50, 2);
	
	def testNumberOfInterestRateFutureContractsRequiredForHedge(self):
		self.assertAlmostEqual(interestRateFutureNumberContracts(3000000, 1000000, 6.5, 100, 90, ACT360_DAYS_IN_YEAR()), 3, 0);
	
	def testForwardForwardRateFromInterpoliation(self):
		self.assertAlmostEqual(forwardForwardRateFromInterpolation(6.5, 6.8, 90, 100, 95), 6.65, 4);
	
	def testNumberOfInterestRateFutureContractsRequiredForHedge(self):
		contracts = interestRateFutureNumberContractsFromInterpolation(10, 10, 90, 120, 110);
		self.assertTrue(len(contracts) == 2);
		self.assertAlmostEqual(contracts[0], 10, 1);
		self.assertAlmostEqual(contracts[1], 6.7, 1);
	
	def testSimpleYieldToMaturityForBond(self):
		self.assertAlmostEqual(bondYieldToMaturity(100, 90, 6, 9), 7.57, 2);
	
	def testCurrentYieldForBond(self):
		self.assertAlmostEqual(bondCurrentYield(90, 6), 6.67, 2);
	
	def testYieldToMaturityFromBondPricePaid(self):
		self.assertAlmostEqual(bondSimpleYieldToMaturity(100, 90, 6, 9), 7.90, 2);
	
	def testComplexYieldFromFinalCoupon(self):
		couponFrequency = 2;
		couponPeriod = ACTACT_DAYS_IN_YEAR() / couponFrequency;
		daysToMaturity = 100;
		self.assertAlmostEqual(bondComplexYieldFromFinalCoupon(100, 102, 6, 1, couponPeriod - daysToMaturity, daysToMaturity, ACTACT_DAYS_IN_YEAR()), 9.67, 2);
	
	def testSimpleYieldFromFinalCoupon(self):
		couponFrequency = 2;
		couponPeriod = ACTACT_DAYS_IN_YEAR() / couponFrequency;
		daysToMaturity = 100;
		self.assertAlmostEqual(bondSimpleYieldFromFinalCoupon(100, 102, 6, 1, couponPeriod - daysToMaturity, daysToMaturity, ACTACT_DAYS_IN_YEAR()), 9.35, 2);
	
	def testBondPriceUsingSimpleInterest(self):
		self.assertAlmostEqual(bondPriceUsingMoneyMarketYield(100, 6, 5.4, 1, 9, 100, ACT360_DAYS_IN_YEAR(), ACT365_DAYS_IN_YEAR()), 107.7133, 4);
	
	def testBondPriceUsingSimpleInterestForCalculator(self):
		self.assertAlmostEqual(bondPriceUsingMoneyMarketYieldForCalculators(100, 6, 5.4, 1, 9, 100, ACT360_DAYS_IN_YEAR(), ACT365_DAYS_IN_YEAR()), 107.7133, 4);
	
	def testMoneyMarketYieldForBond(self):
		self.assertAlmostEqual(bondMoneyMarketYield(100, 107.7133, 6, 1, 9, 100, ACT360_DAYS_IN_YEAR(), ACT365_DAYS_IN_YEAR()), 5.4, 4);
	
	def testMoosmullerYieldForBond(self):
		self.assertAlmostEqual(bondPriceUsingMoosmullerYield(100, 6, 5.4, 1, 9, 100, ACT360_DAYS_IN_YEAR()), 108.1931, 4);
	
	def testBondPriceStrippedCoupon(self):
		self.assertAlmostEqual(bondPriceStrippedCoupon(100, 6, 2, 9, 100, 182), 77.6692, 4);
	
	def testBondDuration(self):
		self.assertAlmostEqual(bondDuration(5.4, [6, 6, 6, 6, 6, 6, 6, 6, 106], [1, 2, 3, 4, 5, 6, 7, 8, 9]), 7.2510, 4);
	
	def testBondModifiedDuration(self):
		self.assertAlmostEqual(bondModifiedDuration(bondDuration(5.4, [6, 6, 6, 6, 6, 6, 6, 6, 106], [1, 2, 3, 4, 5, 6, 7, 8, 9]), 11.063, 1),  6.5288, 4);
	
	def testBondConvexity(self):
		self.assertAlmostEqual(bondConvexity(100, 5.4, 1, [6, 6, 6, 6, 6, 6, 6, 6, 106], [1, 2, 3, 4, 5, 6, 7, 8, 9]), 62.8629, 4);
	
	def testBondChangeInPriceUsingConvexity(self):
		self.assertAlmostEqual(bondPriceChangeUsingConvexity(100, 5.4, 1, 1, [6, 6, 6, 6, 6, 6, 6, 6, 106], [1, 2, 3, 4, 5, 6, 7, 8, 9]), -6.5652, 4);
	
	def testBondChangeInPriceUsingModifiedDuration(self):
		self.assertAlmostEqual(bondPriceChange(100, 5.4, 1, 1, [6, 6, 6, 6, 6, 6, 6, 6, 106], [1, 2, 3, 4, 5, 6, 7, 8, 9]), -6.8795, 1);
	
	def testBondHedgeUsingModifiedDuration(self):
		self.assertAlmostEqual(bondHedgeUsingModifiedDuration(105.39, 8.25, [1000000, 3000000, 5000000], [109.20, 95.30, 102.80], [6.03, 9.20, 5.09]), 6791531.60, 2);
	
	def testBondFuturesPrice(self):
		self.assertAlmostEqual(bondFuturesPrice(105, 6, 5.4, 2, 1.0087, 23, 100, 184, ACT360_DAYS_IN_YEAR()), 104.04, 2);
	
	def testBondFuturesHedgeNotional(self):
		self.assertAlmostEqual(bondFuturesHedgeNotional(1000000, 5.4, 1.0087, 100, ACT360_DAYS_IN_YEAR()), 993793.10, 2);
	
	def testBondImpliedRepoRate(self):
		self.assertAlmostEqual(bondImpliedRepoRate(105, 104, 2.1, 2.8, 0, 1.034, 100, ACT360_DAYS_IN_YEAR()), 10.8773, 4);
	
	def testBondCashAndCarryArbitrage(self):
		self.assertAlmostEqual(bondCashAndCarryArbitrage(100000, 105, 104, 10.2, 2.1, 2.8, 1.034, 100, ACT360_DAYS_IN_YEAR()), 194.87, 2);
	
	def test(self):
		self.assertAlmostEqual(bondYieldZeroCoupon(100, 65.48, 2, 16, 69, 184), 5.5845, 2);

testSuite = unittest.TestLoader().loadTestsFromTestCase(InterestRateInstrumentsTests);

print(testSuite);

unittest.TextTestRunner(verbosity=3).run(testSuite);
