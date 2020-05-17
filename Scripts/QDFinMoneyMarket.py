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

from QDFinInterest import complexInterestRate
from QDFinInterest import simpleInterestRate
from QDFinInterest import effectiveRateProceeds
from QDFinInterest import convertRateToBondMarketBasis

from QDFinTimeValueMoney import simpleDiscountFactorMoneyMarketBasis

from QDFinConstants import ACT360_DAYS_IN_YEAR
from QDFinConstants import ACT365_DAYS_IN_YEAR
from QDFinConstants import DAYS_IN_YEAR

#	Instruments which we know are quoted on a discount rate...
#	USA: T-bills, BA, CP
#	UK: T-bills (gilts), BA
#	T-bills: discount instrument, non-USA and UK are quoted as yield, USA and UK as discount.
#	ACT/365: international and domestic markets in GBP, HKD, SGD, Malaysian Ringgit, Taiwan Dollar, Thai Baht, SAR.
#				domestic but not international markets in JPY, CAD, AUD, NZD.

# The annuity is received at the end, rather than the beginning of a year, and the lump sum/initial cost has interest applied after each coupon payment is taken.
def annuityDeferred(initialCost, interest, years):
	a = initialCost * (interest/100.0);
	b = 1 - (1 / complexInterestRate(interest, years));
	return a / b;

# Annuity received at the end of the year, initial cost is calculated from the complete cashflows for removing the annual amount, discounted for the entire period.
# This gives the same result as calculating the NPV of N cashflows with an expected yield.
def annuityDeferredInitialCost(annuity, interest, years):
	a = annuity / (interest / 100.0);
	b = 1 - (1 / complexInterestRate(interest, years));
	return a * b;

def annuityDue(initialCost, interest, years):
	a = initialCost * (interest/100.0);
	b = 1 + (interest/100.0) - (1 / complexInterestRate(interest, years-1));
	return a / b;

# Annuity received at the beginning of the year, initial cost is calculated from the complete cashflows for removing the annual amount, discounted for the entire period.
# This gives a similar result as calculating the NPV of N cashflows with an expected yield, but the first amount 
def annuityDueInitialCost(annuity, interest, years):
	a = annuity / (interest / 100.0);
	b = 1 + (interest/100.0) - (1 / complexInterestRate(interest, years-1));
	return a * b;a

# For the given initial cost we are calculating the amount you will get for perpetuity for a given yield.
def annuityPerpetual(initialCost, interest):
	return initialCost * (interest / 100.0);

# If we want a perpetual annuity paying x with a given yield, this is the cost.  The yield is applied as interest, then payment of the annuity would occur.
def annuityPerpetualInitialCost(annuity, interest):
	return annuity / (interest / 100.0);

# Generate the initial return for a CD given a face value, coupon interest, and number of days held.
def certificateOfDepositMaturityProceeds(faceValue, interest, days, daysInYear=ACT360_DAYS_IN_YEAR()):
	return faceValue * simpleInterestRate(interest, days, daysInYear);

# Generate the secondary market price for CD. CD could have a variable rate, or be tied to a changing benchmark.
# The current risk free yield, or bank interest rate could also be different, making the return more or less.
# In general:
#		Yield goes up, the price of the instrument goes down.
# 		Yield goes down, the price of the instrument goes up.
# The secondary market price, is the amount that for a given yield, gives the maturity proceeds of the CD.
def certificateOfDepositSecondaryMarketPrice(proceeds, marketYield, daysToMaturity, daysInYear=ACT360_DAYS_IN_YEAR()):
	return proceeds / simpleInterestRate(marketYield, daysToMaturity, daysInYear);

# Generate the return on investment for hold a CD for a length of time. The maturity proceeds are fixed, as the yield reduces, 
#	returns increase...
def certificateOfDepositSimpleYield(interest, saleInterest, initialMaturity, daysHeld, daysInYear=ACT360_DAYS_IN_YEAR()):
	daysToMaturity = initialMaturity - daysHeld;
	cdYield = simpleInterestRate(interest, initialMaturity, daysInYear);
	marketYield = simpleInterestRate(saleInterest, daysToMaturity, daysInYear);
	return  ((cdYield / marketYield) - 1) * (daysInYear/daysHeld) * 100;

# Given a purchase yield/interest and days to maturity, what is the target yield we should sell the CD at which
#	will give us an overall target yield for the investment.  Solve:
#	val = [(1 + i * a/y) / (td/y + 1) - 1] * y/b, where
#		t is target return
#		y is days in a year
#		d is days CD is held
#		i is purchase yield
#		a is days till maturity at purchase
#		b is days till maturity at sale
def certificateOfDepositSimpleYieldWhichReturnsTargetYield(targetYield, interest, initialMaturity, daysHeld, daysInYear=ACT360_DAYS_IN_YEAR()):
	interest = interest / 100;
	targetYield = targetYield / 100;

	daysToMaturity = initialMaturity - daysHeld;
	initialYield = (1 + interest * (initialMaturity / daysInYear));
	discount = (targetYield * daysHeld) / daysInYear + 1;

	simpleYield = (initialYield / discount - 1) * (daysInYear/daysToMaturity);

	return simpleYield * 100;

# Generate the yield on a CD given a purchase yield, sale yield and days held.  As the yield falls, the price goes up as 
#	the total proceeds are fixed, so for the same return, the initial value/price must go up to deliver the same proceeds at maturity.
#	The maturity proceeds are fixed, as the yield reduces, the price will increase...
def certificateOfDepositComplexYield(purchaseYield, saleYield, daysPurchaseToMaturity, daysSaleToMaturity, daysInYear=ACT360_DAYS_IN_YEAR()):
	purchaseTotal = 1 + purchaseYield * 0.01 * (daysPurchaseToMaturity/daysInYear);
	saleTotal = 1 + saleYield * 0.01 * (daysSaleToMaturity/daysInYear);
	days = daysPurchaseToMaturity - daysSaleToMaturity
	print("p s d " + str(purchaseTotal) + " " + str(saleTotal) + " " + str(days));
	return effectiveRateProceeds(saleTotal, purchaseTotal, days, daysInYear);

# Generate the present value of a CD with multiple coupons left to pay, with a given coupon rate, and current market yield.
#	We need the date between the purchase date and the next coupon coming up, and the number of days between each of the coupons
#	going forward till the maturity date.
def certificateOfDepositMultiCouponPrice(faceValue, interest, marketYield, daysBetweenPurchaseAndNextCoupon, daysToNextCoupons, daysInYear=ACT360_DAYS_IN_YEAR()):
	interest = interest / 100;
	marketYield = marketYield / 100;
	
	discountedDays = 0;
	discountedFaceValue = 0;
	discountedCoupons = 0;
	count = len(daysToNextCoupons);

	for i in range(count):
		# For each coupon period, we need to aggregate all the discounts that affect it, do give us the present value
		#	of all of the coupons.
		days = daysToNextCoupons[i]/daysInYear;
		discount = 1;
		for j in range(i+1):
			discountDays = daysToNextCoupons[j];
			if j == 0:
				discountDays = daysBetweenPurchaseAndNextCoupon;
			couponDiscount = 1 + marketYield * (discountDays/daysInYear);
			discount *= couponDiscount;
		discount = 1.0 / discount;
		discountedCoupons += (faceValue * interest * days * discount);

		# We've generated a discount covering the entire coupon range, we can get the present value of the face value
		if i == count - 1:
			discountedFaceValue = faceValue * discount;

	return discountedFaceValue + discountedCoupons;

# The maturity proceeds of a discount instrument is just the face value of the instrument.
def discountInstrumentMaturityProceeds(faceValue):
	return faceValue;

# The secondary market price is the present value of the instrument... essentially the discounted price.
def discountInstrumentPriceUsingYield(faceValue, marketYield, daysToMaturity, daysInYear=ACT360_DAYS_IN_YEAR()):
	return discountInstrumentMaturityProceeds(faceValue) / simpleInterestRate(marketYield, daysToMaturity, daysInYear);

# Generate the discount rate, used by instruments quoted on a discount rate.
#	Instruments which we know are quoted on a discount rate...
#	USA: T-bills, BA, CP
#	UK: T-bills (gilts), BA
def discountInstrumentDiscountRate(discountRate, daysToMaturity, daysInYear=ACT360_DAYS_IN_YEAR()):
	return ((discountRate / 100) * (daysToMaturity / daysInYear)) * 100;

# Generate hte discount rate from the price and face value.  Solve:
#	rate = [1 - p/f] * y/d, where
#		p is price
#		f is face value
#		y is days in year
#		d is days to maturity
def discountInstrumentDiscountRateFromPriceAndFaceValue(faceValue, price, daysToMaturity, daysInYear=ACT360_DAYS_IN_YEAR()):
	return  (1 - price/faceValue) * (daysInYear/daysToMaturity) * 100;

# For instruments quoted on a discount rate, what is the discount.  Rate scaled by days remaining, scaled by the face value.
def discountInstrumentDiscount(faceValue, discountRate, daysToMaturity, daysInYear=ACT360_DAYS_IN_YEAR()):
	return faceValue * discountInstrumentDiscountRate(discountRate, daysToMaturity, daysInYear) * 0.01;

# For instruments quoted on a discount rate, what is the initial cost.
def discountInstrumentPriceUsingDiscountRate(faceValue, discountRate, daysToMaturity, daysInYear=ACT360_DAYS_IN_YEAR()):
	return faceValue * (1 - discountInstrumentDiscountRate(discountRate, daysToMaturity, daysInYear)  *  0.01);

# Generate the return on investment for hold a Discount Instrument for a length of time. 
#	The total proceeds are divided through by the inital amount... 
def discountInstrumentSimpleYield(discountRate, saleDiscountRate, initialMaturity, daysHeld, daysInYear=ACT360_DAYS_IN_YEAR(), basis=DAYS_IN_YEAR()):
	daysToMaturity = initialMaturity - daysHeld;
	purchaseDiscount = 1 - discountRate*0.01 * (initialMaturity/daysInYear);
	saleDiscount = 1 - saleDiscountRate*0.01 * (daysToMaturity/daysInYear);
	return  ((saleDiscount / purchaseDiscount) - 1) * (basis/daysHeld) * 100;

# You can generate the equivalent discount factor from the yield by calculating the present value of the yield.
#	This makes some logical sense, since the discount factor is received at the beginning of a period, and the yield,
#	at the end.  You can also go from first principals, since:
#	P = F x (1 - D x (days/year)); price = face value x (1 - discount factor x (days/year))... and
# 	P = F x (1 + i x (days/year)); if we wanted the price which multiplied by yield, gives us the face value.
#	...subst for P and rebalance to get in terms of D = i / (1 + i x (days/year))
def discountInstrumentDiscountRateFromYield(marketYield, daysToMaturity, daysInYear=ACT360_DAYS_IN_YEAR()):
	my = marketYield / 100;
	return (my / (1 + my * (daysToMaturity / daysInYear))) * 100.0;

# Conversely then, discount rate can give us the yield...
def discountInstrumentYieldFromDiscountRate(discountRate, daysToMaturity, daysInYear=ACT360_DAYS_IN_YEAR()):
	dr = discountRate * 0.01;
	return (dr / (1 - dr * (daysToMaturity / daysInYear))) * 100.0;

# Generate the equivalent yield in the case that we want to match a bond with one or two coupons left to pay with a treasury bill or similar.
def discountInstrumentBondEquivalentYield(discountRate, daysToMaturity, daysInYear=ACT360_DAYS_IN_YEAR(), bondDaysInYear=ACT365_DAYS_IN_YEAR()):

	if daysToMaturity <= 182:
		return convertRateToBondMarketBasis(discountInstrumentYieldFromDiscountRate(discountRate, daysToMaturity, daysInYear));

	discountRate *= 0.01;

	daysInMoneyMarketBasis = daysToMaturity/daysInYear;
	daysInBondMarketBasis = daysToMaturity/bondDaysInYear;

	a = (daysToMaturity/bondDaysInYear - 0.5);
	b = (2 * daysToMaturity) / bondDaysInYear;
	c = 2 * (1 - (1/ (1 - discountRate * (daysToMaturity/daysInYear))));

	quadratic = (-b + pow(b*b - 4*a*c, 0.5))/ (2*a); 

	return quadratic * 100;

# Generate the equivalent discount rate from a bond equivalent yield.  We want to match a bond with one or two coupons left to pay with a treasury bill or similar.
def discountInstrumentRateFromBondEquivalentYield(marketYield, daysToMaturity, daysInYear=ACT360_DAYS_IN_YEAR(), bondDaysInYear=ACT365_DAYS_IN_YEAR()):

	if daysToMaturity <= 182:
		return convertRateToBondMarketBasis(discountInstrumentDiscountRateFromYield(marketYield, daysToMaturity, daysInYear))

	marketYield *= 0.01;

	daysInMoneyMarketBasis = daysToMaturity/daysInYear;
	daysInBondMarketBasis = daysToMaturity/bondDaysInYear;

	a = (daysToMaturity/daysInYear - 0.5);
	b = (2 * daysToMaturity) / daysInYear;
	c = 2 * (1 - (1/ (1 + marketYield * (daysToMaturity/bondDaysInYear))));

	quadratic = (-b + pow(b*b - 4*a*c, 0.5))/ (2*a); 

	return abs(quadratic) * 100;


	