# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 15:41:04 2019

@author: rayde
"""
from stock_scraper import calculations
from yahoofinancials import YahooFinancials

class balance_sheet(calculations):
    def __init__(self, symbol, source, start, end):
        super().__init__(symbol, source, start, end)
        self.yahoo = YahooFinancials(self.symbol)
        self.bsd = self.__get_bs__()
        self.retained_earnings = self.__retained_earnings__()
        self.debt = self.__Debt__()
        self.cash = self.__cash__()
        
    def __get_bs__(self):
        self.bsd = self.yahoo.get_financial_stmts('quarterly', 'balance')
        return self.bsd
    
    def __retained_earnings__(self):
        x = list(self.bsd['balanceSheetHistoryQuarterly'][self.symbol][0].keys())
        return self.bsd['balanceSheetHistoryQuarterly'][self.symbol][0][x[0]]['retainedEarnings']
        
    def __Debt__(self):
        x = list(self.bsd['balanceSheetHistoryQuarterly'][self.symbol][0].keys())
        return self.bsd['balanceSheetHistoryQuarterly'][self.symbol][0][x[0]]['longTermDebt'] 
    
    def __cash__(self):
        x = list(self.bsd['balanceSheetHistoryQuarterly'][self.symbol][0].keys())
        return self.bsd['balanceSheetHistoryQuarterly'][self.symbol][0][x[0]]['cash'] 

class earnings(balance_sheet):
    def __init__(self, symbol, source, start, end):
        super().__init__(symbol, source, start, end)
        self.earn = self.__get_earn__()
    
    def __get_earn__(self):
        earnings_data = self.yahoo.get_stock_earnings_data()
        return earnings_data
    
class addtl(calculations):
    def __init__(self, symbol):
        super().__init__(symbol)
        self.beta = self.Beta()
        self.Div_Beta = self.Div_Beta()
        self.R_Beta = self.R_Beta()
     #   'beta':[self.beta],
      #  'Div_Beta': [self.Div_Beta],
       # 'R_Beta':[self.R_Beta],

    def buyback_Yield(self):
        pass
    
    def P_S(self):
        pass
    
    def FCF(self):
        pass
    
    def Net_debt(self):
        pass
    
    def Debt_Cap(self):
        pass
    
    def EBITDA(self):	
        pass
    
    def EV(self):
        pass
    
    def EBITDA_EV(self):	
        pass
    
    def P_CASH(self):
        pass
    
    def Price_Target(self):	
        pass
    
    def Capital_Gains(self):	
        pass
    
    def MktCap_Avg(self):	
        pass
    
    def Beta(self):
        return 1

    def Div_Beta(self):
        return self.div_r/self.beta
    
    def R_Beta(self):
        return self.t_r/self.beta