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

def DAYS_IN_YEAR():
	return 365;

def DEFAULT_BASIS_DAYS():
	return ACT365_DAYS_IN_YEAR();

def ACT365_DAYS_IN_YEAR():
	# Bond market basis, number of days in year.
	return 365;

def ACTACT_DAYS_IN_YEAR():
	# ACT/ACT days in year... currently set to 366... needs current year to give full result.
	return 366;

def ACT360_DAYS_IN_YEAR():
	# Money market basis, number of days in year.
	return 360;

def WORKING_DAYS_IN_YEAR():
	return 252;
