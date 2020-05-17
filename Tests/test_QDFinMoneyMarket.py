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

from QDFinMoneyMarket import annuityDue
from QDFinMoneyMarket import annuityDeferred
from QDFinMoneyMarket import annuityDueInitialCost
from QDFinMoneyMarket import annuityDeferredInitialCost
from QDFinMoneyMarket import annuityPerpetual
from QDFinMoneyMarket import annuityPerpetualInitialCost
from QDFinMoneyMarket import certificateOfDepositMaturityProceeds
from QDFinMoneyMarket import certificateOfDepositSecondaryMarketPrice
from QDFinMoneyMarket import certificateOfDepositSimpleYield
from QDFinMoneyMarket import discountInstrumentPriceUsingYield
from QDFinMoneyMarket import discountInstrumentDiscount
from QDFinMoneyMarket import discountInstrumentPriceUsingDiscountRate
from QDFinMoneyMarket import discountInstrumentYieldFromDiscountRate
from QDFinMoneyMarket import certificateOfDepositMultiCouponPrice
from QDFinMoneyMarket import discountInstrumentBondEquivalentYield

class MoneyMarketTests(unittest.TestCase):
	def testInitialCostAnnuityDeferred5YearYield8(self):
		self.assertAlmostEqual(annuityDeferredInitialCost(5000, 8, 5), 19963.55, 2);

	def testAnnuityDeferred5YearsYield8(self):
		self.assertAlmostEqual(annuityDeferred(50000, 8, 5), 12522.82, 2);

	def testInitialCostAnnuityDue5YearsYield8(self):
		self.assertAlmostEqual(annuityDueInitialCost(5000, 8, 5), 21560.63, 2);

	def testAnnuityDue5YearsYield8(self):
		self.assertAlmostEqual(annuityDue(50000, 8, 5), 11595.21, 2);

	def testInitialCostAnnuityPerpetualYield8(self):
		self.assertAlmostEqual(annuityPerpetualInitialCost(5000, 8), 62500.00, 2);

	def testAnnuityPerpetualYield8(self):
		self.assertAlmostEqual(annuityPerpetual(50000, 8), 4000.0, 2);

	def testCertificateOfDepositMaturityProceedsAt100Days(self):
		self.assertAlmostEqual(certificateOfDepositMaturityProceeds(1000000, 8, 100), 1022222.22, 2);

	def testCertificateOfDepositSecondaryMarketAt25Days(self):
		maturity = 100;
		currentDay = 25;
		proceeds = certificateOfDepositMaturityProceeds(1000000, 8, maturity)
		daysToMaturity = maturity - currentDay;
		self.assertAlmostEqual(certificateOfDepositSecondaryMarketPrice(proceeds, 7, daysToMaturity), 1007529.09, 2);

	def testCertificateOfDepositReturnHolding25Days(self):
		self.assertAlmostEqual(certificateOfDepositSimpleYield(7, 6, 75, 25), 8.9256, 4);

	def testSecondaryMarketCostOfDiscountInstrumentUsingMarketYieldWith100DayMaturity(self):
		self.assertAlmostEqual(discountInstrumentPriceUsingYield(1000000, 8, 100), 978260.87, 2);

	def testInitialCostDiscountInstrumentQuotedUsingDiscountRateWith100DayMaturity(self):
		self.assertAlmostEqual(discountInstrumentPriceUsingDiscountRate(1000000, 8, 100), 977777.78, 2);

	def testDiscountForDiscountInstrumentQuotedUsingDiscountRateWith100DayMaturity(self):
		self.assertAlmostEqual(discountInstrumentDiscount(1000000, 8, 100), 22222.22, 2);

	def testEquivalentYieldFromDiscountRateWith100DayMaturity(self):
		self.assertAlmostEqual(discountInstrumentYieldFromDiscountRate(8, 100), 8.1818, 4);

	def testCertificateOfDepositMultipleCouponPrice(self):
		self.assertAlmostEqual(certificateOfDepositMultiCouponPrice(1000000, 8, 7, 40, [92, 81, 91, 92]), 1019603.36, 2);

	def testBondEquivalentYieldForMaturityUnder182Days(self):
		self.assertAlmostEqual(discountInstrumentBondEquivalentYield(8, 100, ACT360_DAYS_IN_YEAR(), ACT365_DAYS_IN_YEAR()), 8.2955, 4);

	def testBondEquivalentYieldForMaturityOver182Days(self):
		self.assertAlmostEqual(discountInstrumentBondEquivalentYield(8, 182, ACT360_DAYS_IN_YEAR(), ACT365_DAYS_IN_YEAR()), 8.4530, 4);
		self.assertAlmostEqual(discountInstrumentBondEquivalentYield(8, 183, ACT360_DAYS_IN_YEAR(), ACT365_DAYS_IN_YEAR()), 8.4540, 2);

testSuite = unittest.TestLoader().loadTestsFromTestCase(MoneyMarketTests);

print(testSuite);

unittest.TextTestRunner(verbosity=3).run(testSuite);
