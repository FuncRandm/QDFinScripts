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

from QDFinConstants import DEFAULT_BASIS_DAYS

from QDFinInterest import simpleInterestRate
from QDFinInterest import complexInterestRate
from QDFinInterest import simpleInterestRateMoneyMarketBasis

# Get the discounted future value based on the present value
def simpleFutureValue(amount, interest, days, daysInYear=DEFAULT_BASIS_DAYS()):
	return amount * (simpleInterestRate(interest, days, daysInYear));

# Get the discounted compounded future value based on present value
def complexFutureValue(amount, interest, years):
	return amount * complexInterestRate(interest, years);

# Get the present value based on the future value
def simplePresentValue(amount, interest, days, daysInYear=DEFAULT_BASIS_DAYS()):
	return amount * (1.0 / simpleInterestRate(interest, days, daysInYear));

# Get the present value based on the compounded future value
def complexPresentValue(amount, interest, years):
	return amount / complexInterestRate(interest, years);

# Get the yield based on the purchase value, sale value and the number of days for the investment
def simpleYield(purchaseValue, saleValue, days, daysInYear=DEFAULT_BASIS_DAYS()):
	return 100.0 * ((saleValue/purchaseValue - 1) * (daysInYear / days));

# Get the compounded yield based on the purchase value, sale value and the number of days for the investment
def complexYield(purchaseValue, saleValue, years):
	return 100.0 * (math.pow(saleValue/purchaseValue, 1/years) - 1);

# Get the compounded yield based on the purchase value, sale value and the number of days for the investment.  
def complexYieldFromDays(purchaseValue, saleValue, days, daysInYear=DEFAULT_BASIS_DAYS()):
	return 100.0 * (math.pow(saleValue/purchaseValue, daysInYear/days) - 1);

# Get the simple discount factor for a time period
def simpleDiscountFactor(interest, days, daysInYear=DEFAULT_BASIS_DAYS()):
	return 1.0 / simpleInterestRate(interest, days, daysInYear);

# Get the complex discount factor for a time period
def complexDiscountFactor(interest, years):
	return 1.0 / complexInterestRate(interest, years);

# Get the simple discount factor for time period, for money market basis
def simpleDiscountFactorMoneyMarketBasis(interest, days):
	return 1.0 / simpleInterestRateMoneyMarketBasis(interest, days);

# Get the continuously compounded discount factor for an interest rate over a number of days
def continuouslyCompoundedDiscountFactor(interest, days):
	return math.exp(-(interest/100) * (days / DEFAULT_BASIS_DAYS()));

# Get the Net Present Value (NPV) for a series of cashfows assuming yearly returns starting at year 1
def netPresentValueOfCashflows(cashflows, interest):
	power = 1;
	npv = 0;
	for item in cashflows:
		npv += complexPresentValue(item, interest, power)
		power += 1;
	return npv;

# Get the Net Present Value (NPV) for a series of cashflows with the year that the cashflow is received
def netPresentValueOfCashflowsWithDates(cashflows, years, interest):
	length = len(cashflows);
	npv = 0;
	for i in range(length):
		cashflow = cashflows[i];
		year =  years[i];
		npv += complexPresentValue(cashflow, interest, year);
	return npv;

# Generate the internal rate of return for a set of cashflows against the initial negative cashflow/investment, assuming yearly returns starting at year 1
# Solution uses secant formula with error correction.  There is no forced break after N iterations as solution of IRR guaranteed after some time.
def internalRateOfReturnOfCashflows(initialInvestment, cashflows):

	prev = 0.25;
	curr = 0.2;
	c = -initialInvestment;

	while not math.isclose(prev, curr, rel_tol=0.0001):
		npvPrev = netPresentValueOfCashflows(cashflows, prev) + c;
		npvCurr = netPresentValueOfCashflows(cashflows, curr) + c;

		a = (curr - prev)/(npvCurr - npvPrev);
		b = 1 - 1.4 * (npvPrev / ( npvPrev - 3 * npvCurr + 2 * c ));
		next = curr - npvCurr * a * b;

		prev = curr;
		curr = next;

		#print("Prev " + str(prev));
		#print("Curr " + str(curr));

	return curr;

# Generate the internal rate of return for a set of cashflows against the initial negative cashflow/investment, with dates for the cashdlows.
# Solution use the secant formula with error correction.  There is no forced break after N iterations as solution of IRR guaranteed after some time.
# FIXME: This should be a single function, with a selector for the version of the NPV calculation.
def internalRateOfReturnOfCashflowsWithDates(initialInvestment, cashflows, years):
	prev = 0.25;
	curr = 0.2;
	c = -initialInvestment;

	while not math.isclose(prev, curr, rel_tol=0.0001):
		npvPrev = netPresentValueOfCashflowsWithDates(cashflows, years, prev) + c;
		npvCurr = netPresentValueOfCashflowsWithDates(cashflows, years, curr) + c;

		a = (curr - prev)/(npvCurr - npvPrev);
		b = 1 - 1.4 * (npvPrev / ( npvPrev - 3 * npvCurr + 2 * c ));
		next = curr - npvCurr * a * b;

		prev = curr;
		curr = next;

	return curr;
