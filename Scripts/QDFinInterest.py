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

import math

from QDFinConstants import DAYS_IN_YEAR
from QDFinConstants import ACT365_DAYS_IN_YEAR
from QDFinConstants import ACT360_DAYS_IN_YEAR
from QDFinConstants import DEFAULT_BASIS_DAYS

# Normal elements for interest rate:
# 1. Period investment/loan runs for... 6m,1y,2y etc.
# 2. Absolute period for the quoted interest rate... usually a single year to allow IRs to be compared, but a 5 year term would compound the yearly figure and pay interest as a single lump at the end of the 5 years.
# 3. Frequency of interest payments.

# Get the simple interest rate for n days
def simpleInterestRate(interest, days, daysInYear=DEFAULT_BASIS_DAYS()):
	return 1.0 + (interest / 100.0) * (days / daysInYear);

# Get the simple interest rate for n days, in money market basis
def simpleInterestRateMoneyMarketBasis(interest, days):
	return  1.0 + (interest / 100.0) * (days / ACT360_DAYS_IN_YEAR());

# Get the complex interest rate for n years
def complexInterestRate(interest, years):
	return math.pow(1.0 + (interest / 100.0), years);

# Get the final amount after applying compounded interest over a number of years.
def complexInterest(initialAmount, interest, years):
	return initialAmount * complexInterestRate(interest, years);

# Get the final amount after applying a simple interest rate for n days.
def simpleInterest(initialAmount, interest, days, daysInYear=DEFAULT_BASIS_DAYS()):
	return initialAmount * (simpleInterestRate(interest, days, daysInYear));

# This gives the equivalment annual rate to an interest rate with n payments a year.
def effectiveRate(interest, numPayments):
	return (math.pow(1.0 + ((interest / 100.0) / numPayments), numPayments) - 1.0) * 100;

# This gives the equivalent annual rate given some initial amount and the final proceeds from any cashflows
def effectiveRateProceeds(initialAmount, totalProceeds, days, daysInYear=DEFAULT_BASIS_DAYS()):
	return (math.pow(totalProceeds/initialAmount, daysInYear/days)  - 1) * 100;

# This gives the effective annual rate for a sub-yearly interest rate, with a single coupon paid at maturity.
#	The coupon rate is compounded up to an actual year, rather than bond/market basis.
def effectiveRateCouponAtMaturity(interest, days, daysInYear=DEFAULT_BASIS_DAYS()):
	return (math.pow(1.0 + (interest / 100.0) * (days/daysInYear), DAYS_IN_YEAR() / days) - 1.0) * 100;

# This gives the effective annual rate for sub-yearly interest rate, where a ratio of proceeds is already known.
def effectiveRateRatioAtMaturity(ratio, days, daysInYear=DEFAULT_BASIS_DAYS()):
	return (math.pow(1.0 + (ratio / 100.0), daysInYear / days) - 1.0) * 100;

# This gives the daily equivalent rate to an interest rate r received on a known day.
def dailyEffectiveRate(interest, days, daysInYear=DEFAULT_BASIS_DAYS()):
	return (math.pow(1.0 + ((interest / 100.0) / (daysInYear/days)), 1.0/days) - 1.0) * daysInYear * 100;

# This gives the nominal rate of interest charged across n payments for the equivalent yearly effective rate.
def nominalRate(interest, numPayments):
	return ((math.pow(1.0 + (interest/100), 1.0 / numPayments) - 1.0) * numPayments) * 100;

# This gives the continuously compounded interest rate 
def continuouslyCompoundedRate(interest, days, daysInYear=DEFAULT_BASIS_DAYS()):
	return (daysInYear/days) * math.log(simpleInterestRate(interest, days)) * 100;

# This gives the effective (yearly) rate from a continually compounded rate
def effectiveRateFromContinuallyCompoundedRate(interest):
	return (math.exp(interest / 100.0) - 1.0) * 100.0;

# Convert ACT/365 basis to ACT360 basis
def convertRateToMoneyMarketBasis(interest):
	return interest * (ACT360_DAYS_IN_YEAR() / ACT365_DAYS_IN_YEAR());

# Convert ACT/360 basis to ACT/365 basis
def convertRateToBondMarketBasis(interest):
	return interest * (ACT365_DAYS_IN_YEAR() / ACT360_DAYS_IN_YEAR());

# Convert simple ratio to interest rate
def convertRatioToRate(ratio):
	return (ratio - 1.0) * 100;

