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

sys.path.append('Tests') # noqa: E703

from test_QDFinInterest import InterestTests
from test_QDFinInterestRateInstruments import InterestRateInstrumentsTests
from test_QDFinMoneyMarket import MoneyMarketTests
from test_QDFinStatistics import StatisticsTests
from test_QDFinTimeValueMoney import TimeValueOfMoneyTests

testSuite = unittest.TestLoader().loadTestsFromTestCase(InterestTests)
testSuite.addTest(unittest.TestLoader().loadTestsFromTestCase(InterestRateInstrumentsTests))
testSuite.addTest(unittest.TestLoader().loadTestsFromTestCase(MoneyMarketTests))
testSuite.addTest(unittest.TestLoader().loadTestsFromTestCase(StatisticsTests))
testSuite.addTest(unittest.TestLoader().loadTestsFromTestCase(TimeValueOfMoneyTests))

print(testSuite)

unittest.TextTestRunner(verbosity=3).run(testSuite)
