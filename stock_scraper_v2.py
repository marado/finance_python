# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 19:34:10 2019

@author: rayde
"""
import pandas
from pandas_datareader import DataReader
from pandas_datareader.yahoo.actions import YahooActionReader, YahooDivReader
from pandas_datareader.yahoo.quotes import YahooQuotesReader
from pandas import DataFrame
import numpy as np
from balance_sheet import balance_sheet
from yahoo_scrape import scrape
import sys

class __stocks__:
    def __init__(self, symbol, source, start, end, sort=True):
        '''parameters'''
        self.symbol = symbol
        self.source = source
        self.start = start
        self.end = end
        self.__basic__()

    def __basic__(self):
        '''Grab Basic Current Info '''
        self.__readers__()
        self.__description__()
        self.__div_history__()
    
    def __readers__(self): 
        '''Generate Dividend and Split info'''
        self.yar = YahooActionReader(self.symbol, self.start, self.end)
        self.div = YahooDivReader(self.symbol, self.start, self.end)
        ''' Generate Intermediate Data'''
        self.quote = YahooQuotesReader(self.symbol, self.start, self.end)
        self.daily = DataReader(self.symbol, self.source, self.start, self.end)
        self.data = self.quote.read()
        
    def __div_history__(self):
        try:
            history = self.yar.read()
            dividend = history.iloc[0][1]
        except:
            history = np.nan
            dividend = np.nan
        finally:
            self.div_history = history
            self.dividend = float(dividend)
            
    def __description__(self):
        try:
            s = scrape(self.symbol).__profile__()
            industry = s.find('span', string='Industry').find_next().text
            description = s.find('span', string='Description').find_next().text
        except:
            print(sys.last_value)
        finally:
            self.industry=industry
            self.description = description
        
class __stats__(__stocks__):
    def __init__(self, symbol, source, start, end, sort=True):
        super().__init__(symbol, source, start, end, sort=True)
        self.__attributes__()
        
    def __attributes__(self):
        self.__perc_change__()
        self.__marketCap__()              
        self.__PE__()
        self.__priceToBook__()
        self.__Dividend_Yield__()
        self.__other__()

    def __perc_change__(self):
        try:
            change = self.daily['Adj Close'][-1] - self.daily['Adj Close'][0]
            perc_change = change/self.daily['Adj Close'][0]
        except:
            perc_change = np.nan
        finally:
            self.perc_change = float(perc_change)

    def __marketCap__(self):
        try:
            cap = self.data.iloc[0]['marketCap']
        except:
            cap = np.nan
        finally:
            self.marketcap = int(cap)
            
    def __PE__(self):
        try:
            forward = self.data.iloc[0]['forwardPE']
            trailing = self.data.iloc[0]['trailingPE']
            one_pe = 1/trailing
        except:
            forward = np.nan
            trailing = np.nan
            one_pe = np.nan
        finally:
            self.forwardpe = float(forward)
            self.trailingpe = float(trailing)
            self.one_pe = float(one_pe)

    def __priceToBook__(self):
        try:
            pb = self.data.iloc[0]['priceToBook']
        except:
            pb = np.nan
        finally:
            self.pricetobook = float(pb)

    def __Dividend_Yield__(self):
        try:
            divyield = self.data.iloc[0]['trailingAnnualDividendYield']
        except:
            divyield = np.nan
        finally:
            self.div_r = float(divyield)

    def __other__(self):
        self.price = self.data.iloc[0]['price']
        self.outstand = self.data.iloc[0]['sharesOutstanding']
        try:
            pricetocash = float(self.price/(balance_sheet(self.symbol).cash/self.outstand))
        except:
            pricetocash = np.nan
        finally:
            self.pricetocash = pricetocash
            self.volume = self.data.iloc[0]['regularMarketVolume']
            self.name = self.data.iloc[0]['longName']
        
class calculations(__stats__):
    def __init__(self, symbol, source, start, end, sort=True):
        super().__init__(symbol, source, start, end, sort=True)
        self.__Total_Return__()
        self.__Beta__()
        self.__riskadj__()
        self.calcdf = self.__df__()

    def __Total_Return__(self):
        if np.isnan(self.div_r):
            self.t_r = float(self.perc_change)
        else:
            self.t_r = float(self.div_r + self.perc_change)
            
    def __Beta__(self):
        try:
            soup_page = scrape(self.symbol).__quote__()
            beta = soup_page.find('span', string = 'Beta (3Y Monthly)').find_next().text
        except:
            beta = np.nan
        finally:
            self.beta = float(beta)
    
    def __riskadj__(self):
        if np.isnan(float(self.beta)):
            self.returns_adj = self.div_r
        else:
            self.returns_adj = abs(self.div_r/self.beta)            
      
    def __df__(self):
        data = {'name':[self.name], 
                          'price':[self.price],
                          'perc_change' : [self.perc_change],
                          'dividend yield':[self.div_r],
                          'total_return':[self.t_r],
                          'beta':[float(self.beta)],
                          'returns (adj)':[self.returns_adj],
                          'priceToBook':[self.pricetobook],
                          '1/PE':[self.one_pe],
                          'marketcap':[self.marketcap],
                          'shares outstanding': [self.outstand],
                          'trailingPE':[self.trailingpe],
                          'forwardPE':[self.forwardpe],
                          'pricetocash':[self.pricetocash],
                          'dividend': [self.dividend],
                          'volume': [self.volume]}   
        return DataFrame.from_dict(data, orient= 'index', columns = [self.symbol])
    
class industry:
        def __init__(self, df_list):
            self.df_list = df_list
            self.concat_df = pandas.concat(df_list, axis=1)
            self.__industry_averages__()
            self.__industry_ratios__()
        
        def __industry_averages__(self):
            self.avg_divr = self.concat_df.iloc[3].mean()
            self.avg_return = self.concat_df.iloc[2].mean()
            self.avg_beta = self.concat_df.iloc[5].mean()
            self.avg_pb = self.concat_df.iloc[7].mean()
            self.avg_one_pe = self.concat_df.iloc[8].mean()
            self.avg_mc = self.concat_df.iloc[9].mean()
            self.avg_so = self.concat_df.iloc[11].mean()
            self.averages = {'avg_divr': self.avg_divr,
                            'avg_return': self.avg_return,
                            'avg_beta': self.avg_beta,
                             'avg_one_pe': self.avg_one_pe,
                             'avg_pb': self.avg_pb,
                             'avg_mc': self.avg_mc,
                             'avg_so': self.avg_so}
            
        def __industry_ratios__(self):
            self.industry_dict = {'to avg_return': (self.concat_df.iloc[2].subtract(self.avg_return)),
                                'to avg_1pe': (1-self.concat_df.iloc[8].subtract(self.avg_one_pe)),
                                'to avg_divr': (1-self.concat_df.iloc[3].subtract(self.avg_divr)),
                                'to avg_pb': self.concat_df.iloc[7].divide(self.avg_pb),
                                'to avg_mc': self.concat_df.iloc[9].divide(self.avg_mc),
                                'to avg_so': self.concat_df.iloc[11].divide(self.avg_so)}
            self.industry_df = pandas.DataFrame.from_dict(self.industry_dict).T