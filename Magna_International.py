# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 10:41:19 2019

@author: rayde

Magna International Analysis

"""

from stock_scraper import calculations
from datetime import datetime

#pip install pandas-datareader
symbol = "MG.TO"
source = "yahoo"
start = datetime(2018, 7, 19)
end = datetime(2019, 7, 19)
magna = calculations(symbol, source, start, end)

''' clean data '''
magna.dividend
''' verify special dividend or delete '''
magna.dividend.drop(x.index[2])
