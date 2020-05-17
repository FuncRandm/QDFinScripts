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
from QDFinConstants import WORKING_DAYS_IN_YEAR

# Generate a simple linear ratio between times...
def timeRatio(sourceTime, destinationTime, targetTime):
	return (targetTime - sourceTime) / (destinationTime - sourceTime);

# Simple linear interpolation between start and end point, with the ratio calculated from the start, destination and target times.
def linearInterpolation(sourceValue, destinationValue, sourceTime, destinationTime, targetTime):
	return sourceValue + (destinationValue - sourceValue) * timeRatio(sourceTime, destinationTime, targetTime);

# Logarithmic interpolation between 
def logInterpolation(sourceValue, destinationValue, sourceTime, destinationTime, targetTime):
	time = (targetTime - sourceTime) / (destinationTime - sourceTime);
	logx = math.log(sourceValue) + (math.log(destinationValue) - math.log(sourceValue)) * time;	
	return math.exp(logx);

# Calculate the mean average of a set of numbers
def mean(numbers):
	numberSum = 0.0;
	for item in numbers:
		numberSum += item;
	return numberSum / len(numbers);

# Calculate the variance, the mean of all the differences from the mean squared.  You can offset the item count in numbers by an arbitrary amount.
def variance(numbers, offset = 0):
	meanAv = mean(numbers);
	numberSum = 0.0;
	for item in numbers:
		numberSum += math.pow(item - meanAv, 2);
	return numberSum / (len(numbers) - offset);

# Calculate the standard deviation, which is the square root of the variance.  You can offset the item count in numbers by an arbitrary amount.
def standardDeviation(numbers, offset = 0):
	return math.sqrt(variance(numbers, offset));

# Calculate the volatility of a set of numbers... vol of an option is the annualised standard deviation of the log of relative price movements
# Assumes that there is more than 1 number, and that we're reducing the vol by 1 if we don't have data points for the entire date range.
def historicVolatility(numbers, days=WORKING_DAYS_IN_YEAR()):
	lastItem = numbers[0];
	numItems = len(numbers);
	differences = list();

	# Calculate a list of the log of the relative price difference
	for i in range(1, numItems):
		item = numbers[i];
		differences.append(math.log(item / lastItem));
		lastItem = item;

	# If the number of data points is not the same as our annualised count, then we offset the variance calc by one to get
	# a more accurate volatility... and generate the standard deviation of the ln(price movement).
	offset = 0;
	if days != numItems:
		offset = 1;
	differenceVariance = variance(differences, offset);

	diffsStandardDeviation = standardDeviation(differences, offset);

	# Volatility is the standard deviation * square root of frequency per year of the data.  Scale to percentage amount.
	return 100.0 * diffsStandardDeviation * math.sqrt(days);

# Correlation coefficient, calculate a value that lies between +1 and -1.  If they are perfectly correlated, their coefficient is +1,
# if they move exactly in line but in opposite directions, their correlation is -1.  If there is no correlation, their coefficient is 0.
# Assumes that both lists are non-empty and have the same length
def correlationCoefficient(listA, listB):
	numItems = len(listA);
	meanA = mean(listA);
	meanB = mean(listB);
	sumAB = 0;

	for i in range(numItems):
		x = listA[i];
		y = listB[i];
		sumAB += x * y;
	top = sumAB - (numItems * meanA * meanB);

	sumASq = 0;

	for item in listA:
		sumASq += math.pow(item, 2);

	sumBSq = 0;

	for item in listB:
		sumBSq += math.pow(item, 2);

	bottom = math.sqrt((sumASq - (numItems * meanA * meanA)) * (sumBSq - (numItems * meanB * meanB)))

	return top / bottom;

# Covariance measure how things vary related to each other.
# Assumes that both lists are non-empty and have the same length, and that we're calculating yearly cov.
def covariance(listA, listB, days=WORKING_DAYS_IN_YEAR()):

	numItems = len(listA);

	offset = 0;
	if days != numItems:
		offset = 1;

	coefficient = correlationCoefficient(listA, listB);

	sdA = standardDeviation(listA, offset);
	sdB = standardDeviation(listB, offset);

	#print("A " + str(sdA));
	#print("B " + str(sdB));
	#print("Coeff " + str(coefficient));

	return coefficient * sdA * sdB;

# Covariance measure how things vary related to each other.
# Assumes that both lists are non-empty and have the same length.
# Clearer calculation that doesn't depend on correlation coefficient. 
#  Sum of the product of differences to the mean of both lists over N - 1.
def fastCovariance(listA, listB):
	numItems = len(listA);

	meanA = mean(listA);
	meanB = mean(listB);

	total = 0;

	for i in range(numItems):
		total += (listA[i] - meanA) * (listB[i] - meanB);
		
	return total / (numItems - 1);

# Gives the output for a given input value when put through a gaussian
# distribution function.  1  / ( sqrt(2 * PI) * e^(0.5 * x^2) ) where
# e is approx 2.71828.
def gaussian(x):
	denominator = math.sqrt(2.0 * math.pi) * math.exp(0.5 * math.pow(x,2)); 
	return 1 / denominator;
