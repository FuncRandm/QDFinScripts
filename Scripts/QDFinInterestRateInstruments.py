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

from QDFinConstants import DAYS_IN_YEAR
from QDFinConstants import DEFAULT_BASIS_DAYS
from QDFinConstants import ACT365_DAYS_IN_YEAR
from QDFinConstants import ACT360_DAYS_IN_YEAR

from QDFinStatistics import timeRatio
from QDFinStatistics import linearInterpolation

from QDFinTimeValueMoney import complexPresentValue
from QDFinTimeValueMoney import simpleYield
from QDFinTimeValueMoney import complexYieldFromDays
from QDFinTimeValueMoney import internalRateOfReturnOfCashflowsWithDates

def forwardForwardRate(interestRateLending, interestRateBorrowing, daysInLending, daysInBorrowing, daysInYear=DEFAULT_BASIS_DAYS()):
	# Deposit/Lend at interest rate for the short period, and borrow at rate for the longer period, which gives rate for Forward Forward borrowing.
	#	this is really just short term lending/borrowing.
	lendingRate = 1 + interestRateLending * 0.01 * (daysInLending/daysInYear);
	borrowingRate = 1 + interestRateBorrowing * 0.01 * (daysInBorrowing/daysInYear);
	return (borrowingRate / lendingRate - 1) * (daysInYear / (daysInBorrowing - daysInLending)) * 100;

def forwardForwardRateFromInterpolation(nearRate, farRate, nearDays, farDays, fraDays):
	# Calculate a forward forward rate by interpolating between a near rate and far rate that have the same starting point...
	return linearInterpolation(nearRate, farRate, nearDays, farDays, fraDays);

def forwardRateAgreementSettlementPrice(notional, fraRate, libor, days, daysInYear=DEFAULT_BASIS_DAYS()):
	# Forward rate settlement price for a given notional principal amount with the agreed FRA rate, and LIBOR on the settlement date... 
	#	Dates for FRAs in GBP are based on today's date.
	#	Dates for FRAs traded internationally in other currencies are generally based on spot.
	timeRatio = days/daysInYear;
	libor = libor * 0.01;
	fraRate = fraRate * 0.01;
	return notional * (((fraRate - libor) * timeRatio) / (1 + libor * timeRatio));

def forwardRateAgreementSettlementPriceFromFuturePrice(notional, futurePrice, libor, days, daysInYear=DEFAULT_BASIS_DAYS()):
	# Generate a forward rate agreement settlement price from futures price
	futureRate = 100 - futurePrice;
	return forwardRateAgreementSettlementPrice(notional, futureRate, libor, days, daysInYear);

def forwardRateYieldFromFuturesPrice(price):
	# Calculate the effective yield from the futures price... a future is priced by 100 - effective yield as a percentage.
	return 100 - price;

def cleanBondPrice(notional, couponRate, marketYield, couponFrequency, numCouponPaymentsRemaining, daysSinceLastCoupon, daysToNextCoupon, daysInYear=DEFAULT_BASIS_DAYS(), accruedDaysInYear=DEFAULT_BASIS_DAYS()):
	# Calculate the clean bond price = dirty price - accrued coupon... we cannot assume that there has always been a single coupon payments, so easier to 
	# 	set the accrued coupon to zero in the case that we have no days since last coupon...
	accruedCoupon = bondAccruedInterest(notional, couponRate, daysSinceLastCoupon, accruedDaysInYear);
	return dirtyBondPrice(notional, couponRate, marketYield, couponFrequency, numCouponPaymentsRemaining, daysToNextCoupon, daysInYear) - accruedCoupon;
	
def cleanBondPriceExDividend(notional, couponRate, marketYield, couponFrequency, numCouponPaymentsRemaining, daysToNextCoupon, daysInYear=DEFAULT_BASIS_DAYS(), accruedDaysInYear=DEFAULT_BASIS_DAYS()):
	# Calculate the clean bond price = dirty price + accrued coupon... in the case of bond sales during the ex-divident period, the
	# 	accrued coupon becomes negative and needs to be paid to the bond purchaser.
	accruedCoupon = bondAccruedInterest(notional, couponRate, daysToNextCoupon, accruedDaysInYear);
	return dirtyBondPrice(notional, couponRate, marketYield, couponFrequency, numCouponPaymentsRemaining, daysToNextCoupon, daysInYear) + accruedCoupon;

def dirtyBondPrice(notional, couponRate, marketYield, couponFrequency, numCouponPaymentsRemaining, daysToNextCoupon, daysInYear=DEFAULT_BASIS_DAYS()):
	# Calculate the bond price, given a coupon rate, number of coupon payments remaining and an expected yield.  This uses
	#	a possibly faster algo based on formulation from Nic for calculating the total coupen return, discounted flow.
	couponRate *= 0.01;
	marketYield *= 0.01;

	yieldScale = 1 + marketYield/couponFrequency;
	yieldDenominator = pow(yieldScale, numCouponPaymentsRemaining-1);

	a = couponRate - couponRate * (yieldDenominator * yieldScale); # a / b gives us the scale factor which is compounded to both give us the complete stream of coupon payments...
	b = -marketYield * yieldDenominator;
	c = 1 / yieldDenominator; # discount redemption payment by the total number of coupon payments minus the first payment
	d = 1 / pow(yieldScale,daysToNextCoupon/daysInYear); # discount by days to next coupon payment
	# print("a b c d rate " +  str(a) + " " + str(b) + " " + str(c) + " " + str(d) + " " + str((couponRate/couponFrequency)*(a/b)));

	return notional * (a/b + c) * d;

def bondYield(notional, dirtyPrice, couponRate, couponFrequency, numCouponPaymentsRemaining, daysToNextCoupon, daysInYear=DEFAULT_BASIS_DAYS(), decimalPlaces = 12):
	# Calculate a yield in the case that we know what the dirty price is, but don't know the yield...

	difference = 1.0 / min(pow(10,decimalPlaces), pow(10,12));

	couponRate *= 0.01;

	a = couponRate
	c = daysInYear;
	x = 0.05; # Start market yield check at 5%
	k = couponFrequency;
	h = numCouponPaymentsRemaining
	i = daysToNextCoupon

	# Using Newton-Raphson approximation to successively approximate the value...
	# d/(dx)((100 (-(a - a (1 + x/k)^h)/(x (1 + x/k)^(h - 1)) + 1/(1 + x/k)^(h - 1)))/(1 + x/k)^(i/c)) = 100 (((x/k + 1)^(1 - h) (a - a (x/k + 1)^h))/x^2 - ((1 - h) (x/k + 1)^(-h) (a - a (x/k + 1)^h))/(k x) + (a h)/(k x) + ((1 - h) (x/k + 1)^(-h))/k) (x/k + 1)^(-i/c) - (100 i ((x/k + 1)^(1 - h) - ((x/k + 1)^(1 - h) (a - a (x/k + 1)^h))/x) (x/k + 1)^(-i/c - 1))/(c k)

	for item in range(1000):

		# Calculate the base function...
		price = dirtyBondPrice(notional, couponRate * 100, x * 100, couponFrequency, numCouponPaymentsRemaining, daysToNextCoupon, daysInYear)
		fx = price - dirtyPrice;

		# Calculate ddx

		xx = x/k + 1;
		ax = (a - a * pow(xx, h));
		
		aa = pow(xx, 1 - h);
		ab = ax;
		ac = x*x;

		ba = (1 - h) * pow(xx, -h);
		bb = ax;
		bc = k * x;

		ca = (a * h) / (k * x);
		cb = ((1 - h) * pow(xx,-h))/k;
		cc = pow(xx, -i/c);

		da = pow(xx, 1-h) - ((pow(xx, 1-h)*ax)/x);
		db = pow(xx, -i/c-1);
		dc = c * k;

		# 100 (((x/k + 1)^(1 - h) (a - a (x/k + 1)^h))/x^2 - ((1 - h) (x/k + 1)^(-h) (a - a (x/k + 1)^h))/(k x) + (a h)/(k x) + ((1 - h) (x/k + 1)^(-h))/k) (x/k + 1)^(-i/c) - (100 i ((x/k + 1)^(1 - h) - ((x/k + 1)^(1 - h) (a - a (x/k + 1)^h))/x) (x/k + 1)^(-i/c - 1))/(c k)

		ddx = notional * (((aa*ab)/ac) - ((ba*bb)/bc) + ca + cb) * cc - ((100*i*da*db)/dc); 

		x1 = x - (fx/ddx);

		#print ("x_n f(x_n) f'(x_n) price " + str(x) + " " + str(fx) + " " + str(ddx) + " " + str(price) + " ")

		if abs(x1 - x) < difference:
			#print ("difference value " + str(difference) + " " + str(abs(x1 - x)));
			break;

		x = x1;

	return x * 100;

def bondPriceUsingMoosmullerYield(notional, couponRate, marketYield, couponFrequency, numCouponPaymentsRemaining, daysToNextCoupon, daysInYear=DEFAULT_BASIS_DAYS()):
	# Get the bond price using Moosmuller yield which is used in some German markets and the US Treasury for yield and prices on new issues.
	#	This uses simple interest for the coupon period between purchase and following coupon, but compound otherwise.]
	couponRate *= 0.01;
	marketYield *= 0.01;

	yieldByFrequency = marketYield/couponFrequency;
	yieldScale = 1 + yieldByFrequency;
	yieldDenominator = pow(yieldScale, numCouponPaymentsRemaining-1);

	a = couponRate - couponRate * (yieldDenominator * yieldScale); # a / b gives us the scale factor which is compounded to both give us the complete stream of coupon payments...
	b = -marketYield * yieldDenominator;
	c = 1 / yieldDenominator; # discount redemption payment by the total number of coupon payments minus the first payment
	d = notional / (1 + yieldByFrequency * (daysToNextCoupon / daysInYear)); # discount by days to next coupon payment
	#print("a b c d " + str(a) + " " + str(b) + " " + str(c) + " " + str(d) + " " );

	return d * (a/b + c);

def bondPriceUsingMoneyMarketYield(notional, couponRate, marketYield, couponFrequency, numCouponPaymentsRemaining, daysToNextCoupon, daysInYear=DEFAULT_BASIS_DAYS(), bondDaysInYear=DEFAULT_BASIS_DAYS()):
	# Get the bond price using simple interest for the near coupon, and we can use a money market basis rather than compound interest... 
	#	but this gives us a different yield than the version that uses the calculator optimised version!
	couponRate *= 0.01;
	marketYield *= 0.01;

	timeScale = bondDaysInYear/daysInYear;
	yieldByFrequency = marketYield/couponFrequency;
	yieldScale = 1 + yieldByFrequency * timeScale;
	yieldDenominator = pow(yieldScale, numCouponPaymentsRemaining-1);

	a = couponRate - couponRate * (yieldDenominator * yieldScale); # a / b gives us the scale factor which is compounded to both give us the complete stream of coupon payments...
	b = -marketYield * timeScale * yieldDenominator;
	c = 1 / yieldDenominator; # discount redemption payment by the total number of coupon payments minus the first payment
	d = notional / (1 + yieldByFrequency * (daysToNextCoupon / daysInYear)); # discount by days to next coupon payment
	#print("a b c d " + str(a) + " " + str(b) + " " + str(c) + " " + str(d) + " " );

	return d * (a/b + c);

def bondPriceStrippedCoupon(notional, marketYield, couponFrequency, numCouponPaymentsRemaining, daysToNextCoupon, daysInYear=DEFAULT_BASIS_DAYS()):
	# Calculate the price of a stripped coupon.  This is generally the same as a bond with zero coupon rate, and with a known day/Year convention.
	#	You need to understand what the quasi-coupon date is to get the daysToNextCoupon...
	#	There is no coupon, so the dirty price and clean price is the same.
	return dirtyBondPrice(notional, 0, marketYield, couponFrequency, numCouponPaymentsRemaining, daysToNextCoupon, daysInYear);

def bondPriceZeroCoupon(notional, marketYield, couponFrequency, numCouponPaymentsRemaining, daysToNextCoupon, daysInYear=DEFAULT_BASIS_DAYS()):
	# Alias to bondPriceStrippedCoupon to make it easier to find/understand.
	return bondPriceStrippedCoupon(notional, marketYield, couponFrequency, numCouponPaymentsRemaining, daysToNextCoupon, daysInYear);

def bondYieldZeroCoupon(notional, dirtyPrice, couponFrequency, numCouponPaymentsRemaining, daysToNextCoupon, daysInYear=DEFAULT_BASIS_DAYS()):
	# Get the yield for a bond with 0 coupon.
	exponent = 1 / (daysToNextCoupon/daysInYear + (numCouponPaymentsRemaining - 1))
	return (pow(notional / dirtyPrice, exponent) - 1) * couponFrequency * 100;

def bondPriceUsingMoneyMarketYieldForCalculators(notional, couponRate, marketYield, couponFrequency, numCouponPaymentsRemaining, daysToNextCoupon, daysInYear=DEFAULT_BASIS_DAYS(), bondDaysInYear=DEFAULT_BASIS_DAYS()):
	# Get the bond price using simple interest rather than compound interest for the near coupon, and use a money market basis rather than
	#	compound interest.
	couponRate *= 0.01;
	marketYield *= 0.01;

	yieldByFrequency = marketYield/couponFrequency;
	yieldScale = 1 + yieldByFrequency * (bondDaysInYear/daysInYear);
	
	a = couponRate * (1 - (1 / pow(yieldScale, numCouponPaymentsRemaining)));
	b = couponFrequency * (1 - (1 / yieldScale));
	c = 1 / pow(yieldScale, numCouponPaymentsRemaining - 1);
	d = notional / (1 + yieldByFrequency * (daysToNextCoupon/daysInYear));
	
	return d * (a/b + c);

def bondMoneyMarketYield(notional, dirtyPrice, couponRate, couponFrequency, numCouponPaymentsRemaining, daysToNextCoupon, daysInYear=DEFAULT_BASIS_DAYS(), bondDaysInYear=DEFAULT_BASIS_DAYS(), decimalPlaces = 12):
	# Calculate a money market yield in the case that we know what the dirty price is, but don't know the yield...

	difference = 1.0 / min(pow(10,decimalPlaces), pow(10,12));

	couponRate *= 0.01;

	a = couponRate
	b = bondDaysInYear;
	c = daysInYear;
	x = 0.05; # Start market yield check at 5%
	k = couponFrequency;
	h = numCouponPaymentsRemaining
	i = daysToNextCoupon

	# Using Newton-Raphson approximation to successively approximate the value...
	# d/(dx)((100 (-(a - a (1 + (x b)/(k c))^h)/((b x)/c) + 1))/((1 + (x i)/(k c)) (1 + (x b)/(k c))^(h - 1)) - P) = (100 ((b x)/(c k) + 1)^(1 - h) ((c (a - a ((b x)/(c k) + 1)^h))/(b x^2) + (a h ((b x)/(c k) + 1)^(h - 1))/(k x)))/(1 + (i x)/(c k)) - (100 i ((b x)/(c k) + 1)^(1 - h) (1 - (c (a - a ((b x)/(c k) + 1)^h))/(b x)))/(c k (1 + (i x)/(c k))^2) + (100 b (1 - h) ((b x)/(c k) + 1)^(-h) (1 - (c (a - a ((b x)/(c k) + 1)^h))/(b x)))/(c k (1 + (i x)/(c k)))

	for item in range(1000):

		# Calculate the base function...
		price = bondPriceUsingMoneyMarketYield(notional, couponRate * 100, x * 100, couponFrequency, numCouponPaymentsRemaining, daysToNextCoupon, daysInYear, bondDaysInYear)
		fx = price - dirtyPrice;

		# Calculate ddx

		bx = (b * x)/(c * k) + 1;
		ix = (i * x)/(c * k) + 1;
		ct = c * (a - a * pow(bx, h))
		cx = ct/(b * x);
		cx2 = ct/(b * x * x);

		aa = notional * pow(bx, 1 - h);
		ab = cx2 + ((a * h * pow(bx, h - 1))/(k * x));
		ac = ix;

		ba = notional * i * pow(bx, 1- h);
		bb = 1 - cx;
		bc = c * k * ix * ix;

		ca = notional * b * (1 - h) * pow(bx, -h);
		cb = 1 - cx;
		cc = c * k * ix;

		ddx = ((aa*ab)/ac) - ((ba*bb)/bc) + ((ca*cb)/cc); 

		x1 = x - (fx/ddx);

		#print ("x_n f(x_n) f'(x_n) price " + str(x) + " " + str(fx) + " " + str(ddx) + " " + str(price) + " ")

		if abs(x1 - x) < difference:
			#print ("difference value " + str(difference) + " " + str(abs(x1 - x)));
			break;

		x = x1;

	return x * 100;

def dirtyBondPriceForCalculators(notional, couponRate, marketYield, couponFrequency, numCouponPaymentsRemaining, daysToNextCoupon, daysInYear=DEFAULT_BASIS_DAYS()):
	# Bond price calculation using CFA equivalent pricing model	
	couponRate *= 0.01;
	marketYield *= 0.01;

	yieldDenominator = 1 + (marketYield/couponFrequency);

	a = 1 - (1 / pow(yieldDenominator, numCouponPaymentsRemaining)); # a / b gives us the scale factor which is compounded to both give us the complete stream of coupon payments...
	b = 1 - (1 / yieldDenominator);	# This gives us the discount factor, if we were apply the discount like a discount instrument.
	c = 1 / pow(yieldDenominator, numCouponPaymentsRemaining - 1); # discount redemption payment by the total number of coupon payments minus the first payment
	d = 1 / pow(yieldDenominator,daysToNextCoupon/daysInYear); # discount by days to next coupon payment
	# print("a b c d rate " +  str(a) + " " + str(b) + " " + str(c) + " " + str(d) + " " + str((couponRate/couponFrequency)*(a/b)));

	return notional * ((couponRate/couponFrequency)*(a/b) + c) * d;

def bondAccruedInterest(notional, couponRate, daysSinceLastCoupon, daysInYear=DEFAULT_BASIS_DAYS()):
	# Calculate the amount relative to the notional of the bond that we have accrued by holding it.
	return notional * couponRate * 0.01 * (daysSinceLastCoupon/daysInYear);

def bondDuration(marketYield, cashflows, yearsToMaturity):
	# Calculate the bond duration... sum pv of cashflow x time to cashflow/sum pv of cashflow... this gives us the point where
	#	changes to the yield should balance the price change from discounting changes and the coupon reinvestment rate changes.

	numItems = len(cashflows);
	
	sumCashflowTimeToCashflow = 0;
	sumCashflows = 0;

	for i in range(numItems):
		cashflow = cashflows[i];
		time = yearsToMaturity[i];

		pv = complexPresentValue(cashflow, marketYield, time);

		sumCashflowTimeToCashflow += (pv * time);
		sumCashflows += pv;

	return sumCashflowTimeToCashflow / sumCashflows;

def bondModifiedDuration(duration, marketYield, couponFrequency):
	# Calculate the modified bond duration, which is the negative change in price over change in yield all divided by the
	#	the dirty price... or the slope of the curve divided by the dirty price.  The steeper the curve, the faster that
	#	the price will change for any change in yield!  This approximates to the duration discounted by the yield

	marketYield *= 0.01;

	return duration / (1 + marketYield/couponFrequency);

def bondConvexity(dirtyPrice, marketYield, couponFrequency, cashflows, yearsToMaturity, daysInYear=DEFAULT_BASIS_DAYS()):
	# Calculate the convexity of the bond, which is the percentage second derivative of the price change wrt yield.
	#	Actually no need to divide through by daysInYear if the years to maturity is given pre-divided through by daysInYear...

	numItems = len(cashflows);

	scaledYield = marketYield * 0.01;

	sumCashflows = 0;

	for i in range(numItems):
		cashflow = cashflows[i];
		time = yearsToMaturity[i];

		pv = complexPresentValue(cashflow, marketYield/couponFrequency, couponFrequency * time + 2);

		sumCashflows += (pv * time * (time + 1/couponFrequency));

	return sumCashflows / dirtyPrice;

def bondPriceChange(dirtyPrice, marketYield, marketYieldDelta, couponFrequency, cashflows, yearsToMaturity):
	# Calcluate very rough price change due to yield change, using duration and modified duration.

	duration = bondDuration(marketYield, cashflows, yearsToMaturity);
	modifiedDuration = bondModifiedDuration(duration, marketYield, couponFrequency);

	return bondPriceChangeByModifiedDuration(dirtyPrice, marketYieldDelta, modifiedDuration)

def bondPriceChangeByModifiedDuration(dirtyPrice, marketYieldDelta, modifiedDuration):
	# Calculate a very rough price change if you have the dirty price, delta and modified duration
	marketYieldDelta *= 0.01;

	return -dirtyPrice * marketYieldDelta * modifiedDuration;	

def bondPriceChangeUsingConvexity(dirtyPrice, marketYield, marketYieldDelta, couponFrequency, cashflows, yearsToMaturity):
	# Calculate the change in price from a percentage change in yield.

	duration = bondDuration(marketYield, cashflows, yearsToMaturity);
	modifiedDuration = bondModifiedDuration(duration, marketYield, couponFrequency);
	convexity = bondConvexity(dirtyPrice, marketYield, couponFrequency, cashflows, yearsToMaturity);

	marketYieldDelta *= 0.01;

	return -dirtyPrice * modifiedDuration * marketYieldDelta + 0.5 * dirtyPrice * convexity * marketYieldDelta * marketYieldDelta;

def bondYieldToMaturity(notional, cleanPrice, couponRate, yearsToMaturity):
	# Calculate the yield from the notional amount, the clean price paid and the coupon cashflows...
	# internalRateOfReturnOfCashflowsWithDates

	coupons = [];
	dates = [];

	for item in range(yearsToMaturity):
		coupons.append(couponRate);
		dates.append(item+1);

	# Add maturity redemption at end of the period.
	coupons.append(notional);
	dates.append(yearsToMaturity);

	return internalRateOfReturnOfCashflowsWithDates(cleanPrice, coupons, dates);

def bondSimpleYieldToMaturity(notional, cleanPrice, couponRate, yearsToMaturity):
	# Calculate the the yield to maturity of the bond if you ignore the time value of money and capital gain is amortised to maturity
	return 100 * (couponRate + ((notional - cleanPrice) / yearsToMaturity))/cleanPrice;

def bondCurrentYield(cleanPrice, couponRate):
	# Calculate the current bond yield, ignoring capital gain/loss from difference between the price and principal redemption and the time value of money.
	return 100 * (couponRate / cleanPrice);

def bondComplexYieldFromFinalCoupon(notional, cleanPrice, couponRate, couponFrequency, daysSinceLastCoupon, daysToMaturity, daysInYear=DEFAULT_BASIS_DAYS()):
	# Calculate the effective yield if we have a single coupon remaining to be paid on a bond.  This uses the normal complex calculation.
	#	We don't know what the market yield is, so need to go from accrued interest rate...
	accruedInterest = bondAccruedInterest(notional, couponRate, daysSinceLastCoupon, daysInYear);
	dirtyPrice = cleanPrice + accruedInterest;
	cashflow = notional + notional * (couponRate / couponFrequency) * 0.01;
	return complexYieldFromDays(dirtyPrice, cashflow, daysToMaturity, daysInYear);
	
def bondSimpleYieldFromFinalCoupon(notional, cleanPrice, couponRate, couponFrequency, daysSinceLastCoupon, daysToMaturity, daysInYear=DEFAULT_BASIS_DAYS()):
	# Calculate the yield if we have a single coupon remaining to be paid on a bond.  Some people quote this like short term money market lending, ie simple interest...
	accruedInterest = bondAccruedInterest(notional, couponRate, daysSinceLastCoupon, daysInYear);
	dirtyPrice = cleanPrice + accruedInterest;
	cashflow = notional + notional * (couponRate / couponFrequency) * 0.01;
	return simpleYield(dirtyPrice, cashflow, daysToMaturity, daysInYear);

def bondHedgeUsingModifiedDuration(shortDirtyPrice, shortModifiedDuration, longFaceValues, longDirtyPrices, longModifiedDurations):
	# What face value bond do you need to sell to hedge against your long portfolio...

	numItems = len(longFaceValues)

	sumChangeInPrice = 0;

	for i in range(numItems):
		faceValue = longFaceValues[i];
		price = longDirtyPrices[i];
		value = faceValue * (price/100);
		sumChangeInPrice += value * longModifiedDurations[i];

	return sumChangeInPrice / (shortDirtyPrice * 0.01 * shortModifiedDuration);

def bondFuturesPrice(dirtyPrice, couponRate, marketYield, couponFrequency, conversionFactor, daysSinceLastCoupon, daysToMaturity, daysInCouponPeriod, daysInYear=DEFAULT_BASIS_DAYS()):
	# Calculate the price of a future for delivery at some point.

	return bondForwardsPrice(dirtyPrice, couponRate, marketYield, couponFrequency, conversionFactor, daysSinceLastCoupon, daysToMaturity, daysInCouponPeriod, daysInYear)/conversionFactor;

def bondForwardsPrice(dirtyPrice, couponRate, marketYield, couponFrequency, conversionFactor, daysSinceLastCoupon, daysToMaturity, daysInCouponPeriod, daysInYear=DEFAULT_BASIS_DAYS()):
	# Calculate the bond forward price for delivery at some point in the future.

	marketYield *= 0.01;

	daysInBondYear = (daysInCouponPeriod * couponFrequency);
	accruedCouponAtBondPurchase = couponRate * (daysSinceLastCoupon / daysInBondYear);	# Accrued coupon on purchase of bond hedge....
	accruedCouponAtDelivery = couponRate * ((daysToMaturity + daysSinceLastCoupon) / daysInBondYear); # Accrued coupon at the point of bond delivery to futures buyer...
	couponReinvested = 0;

	print("ACBP ACD " + str(accruedCouponAtBondPurchase) + " " + str(accruedCouponAtDelivery))

	return ((dirtyPrice + accruedCouponAtBondPurchase) * (1 + marketYield * (daysToMaturity/daysInYear)) - accruedCouponAtDelivery - couponReinvested);

def bondHedgeRatio(marketYield, conversionFactor, daysToMaturity, daysInYear=DEFAULT_BASIS_DAYS()):
	# This is the hedge ratio which when multiplied by the bond face value gives us the notional futures value that we need to hedge...
	return conversionFactor / (1 + marketYield * 0.01 * (daysToMaturity/daysInYear));

def bondFuturesHedgeNotional(faceValue, marketYield, conversionFactor, daysToMaturity, daysInYear=DEFAULT_BASIS_DAYS()):
	# This gives us the notional value of the futures contracts which we need to hedge a given face value of bond that we are short.
	return faceValue * bondHedgeRatio(marketYield, conversionFactor, daysToMaturity, daysInYear);

def bondImpliedRepoRate(cleanPrice, futuresPrice, accruedCouponNow, accruedCouponDelivery, couponReinvested, conversionFactor, daysToMaturity, daysInYear=DEFAULT_BASIS_DAYS()):
	# This gives us the implied repo rate, which we can use to check whether cash-and-carry arbitrage will make money or not.
	
	numerator = (futuresPrice * conversionFactor) + accruedCouponDelivery + couponReinvested;
	denominator = cleanPrice + accruedCouponNow;

	return (numerator / denominator - 1) * (daysInYear/daysToMaturity) * 100;

def bondCashAndCarryArbitrage(notional, cleanPrice, futuresPrice, repoRate, accruedCouponNow, accruedCouponDelivery, conversionFactor, daysToMaturity, daysInYear=DEFAULT_BASIS_DAYS()):
	# Calculate the cash-and-carry arbitrage profit given by buying bond, repo bond, sell future for bond, futures delivery.

	repoRate *= 0.01;

	# We need to work out the cost of borrowing which we pay through the repo
	bondCostEquivalent = notional/conversionFactor;
	initialCost = bondCostEquivalent * (cleanPrice + accruedCouponNow)/100;
	borrowingCost = initialCost * ( 1 + repoRate * (daysToMaturity/daysInYear));
	#print("borrowingCost " + str(borrowingCost))

	# We need to work out what income we have from various cashflows.
	receipts = bondCostEquivalent * (futuresPrice * conversionFactor + accruedCouponDelivery)/100;
	#print("receipts " + str(receipts))

	return receipts - borrowingCost;

def interestRateStrip(interestRates, days, daysInYear=DEFAULT_BASIS_DAYS()):
	# You can construct an interest rate from the cash interest rate and the forward-forward/FRA rates for a series of consecutive
	#	time periods.  This works as you can refinance at LIBOR for the time periods and offset by an FRA which would give you
	#	a set of known hedged interest rates.
	
	count = len(interestRates);
	rate = 1.0;
	totalDays = 0;

	for i in range(count):
		rate *= (1 + interestRates[i] * 0.01 * (days[i]/daysInYear));
		totalDays += days[i];
	rate -= 1.0;
	rate *= (daysInYear/totalDays);

	return rate * 100;

def interestRateFuturePriceChange(notional, numberOfContracts, priceMovement, months, monthsInYear=12):
	# Generate the profit or loss of a STIR (Short-term Interest Rate) future...
	# This can be used to calculate what the minimum price change is for a given exchange (The "tick".)
	return numberOfContracts * notional * (priceMovement/100) * (months / monthsInYear);

def interestRateFutureNumberContracts(notional, notionalPerContract, libor, days, futureDays, daysInYear=DEFAULT_BASIS_DAYS()):
	# Generate the number of futures contracts we need to hedge a given notional amount.  The future days is the number of days in the 
	#	current futures period, which should be something like 90 / 360 for a strict three month future etc.  The days figure cover the 
	#	equivalent days for an FRA which would be constructed for this forward rate... it could be the same as the future period, or 
	#	some other time...
	numContracts = notional / notionalPerContract;
	return round((numContracts * (days / futureDays)) / (1 + libor * 0.01 * (days / daysInYear)));

def interestRateFutureNumberContractsFromInterpolation(numNearContract, numFarContract, nearDays, farDays, newFutureDays):
	# Generate the number of near and far contracts required based on the interpolation of days, where both contracts start on the same date.
	time = timeRatio(nearDays, farDays, newFutureDays);
	rates = [numNearContract, numFarContract * time];
	return rates;
