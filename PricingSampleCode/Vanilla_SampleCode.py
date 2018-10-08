import pandas as pd
import datetime as dt
import QuantLib as ql

class BlackScholesMerton(object):
    '''
    Black Scholes Merton European option class and its access functions
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def pricing(self, option_type, strike_price, expiry_date, valuation_date, underlying_price, dividend_rate, interest_rate, volatility):
#         ------------- Option setup -------------
        if option_type.lower() in ['c', 'call']:
            put_or_call = ql.Option.Call
        elif option_type.lower() in ['p', 'put']:
            put_or_call = ql.Option.Put
        else:
            print('unknown option type:', option_type)
            return(-1)
        payoff = ql.PlainVanillaPayoff(put_or_call, strike_price)

#         shift expiry date forward by 1 day, so that calculation can be done on the expiry day
        expiry_date_1 = expiry_date + dt.timedelta(days=1)
        eDate = ql.Date(expiry_date_1.day, expiry_date_1.month, expiry_date_1.year)
        exercise = ql.EuropeanExercise(eDate)
        option = ql.VanillaOption(payoff, exercise)

#         ------------- Process setup -------------
        valuation_date = min(expiry_date, valuation_date)
        vDate = ql.Date(valuation_date.day, valuation_date.month, valuation_date.year)

#         Set the valuation date, by default it will use today's date
        ql.Settings.instance().evaluationDate = vDate

#         Calendar
        calendar = ql.China()
        day_counter = ql.ActualActual()

#         Curve setup
        dividend_curve = ql.FlatForward(vDate, dividend_rate, day_counter)
        interest_curve = ql.FlatForward(vDate, interest_rate, day_counter)
        volatility_curve = ql.BlackConstantVol(vDate, calendar, volatility, day_counter)

#         Setup Black Scholes Merton Process
        u = ql.QuoteHandle(ql.SimpleQuote(underlying_price))
        d = ql.YieldTermStructureHandle(dividend_curve)
        r = ql.YieldTermStructureHandle(interest_curve)
        v = ql.BlackVolTermStructureHandle(volatility_curve)
        process = ql.BlackScholesMertonProcess(u, d, r, v)

#         ------------- Set pricing engine, return both option and process -------------
        engine = ql.AnalyticEuropeanEngine(process)
        option.setPricingEngine(engine)
        return(pd.Series({'option':option, 'process':process}))

# ==============================================================================================================
# ==============================================================================================================

# ---------- setup option ----------
bsm = BlackScholesMerton()

expiry_date = dt.datetime.strptime('20170324', '%Y%m%d')
valuation_date = dt.datetime.strptime('20170322', '%Y%m%d')

# ---------- testing pricing ----------
option1, process1 = bsm.pricing('c', 1000, expiry_date, valuation_date, 1023, 0, 0, 0.3)
print('期权价格:',option1.NPV())
print('Delta:',option1.delta())
print('Gamma:',option1.gamma())
print('Vega(%):',option1.vega()/100)
print('ThetaPerDay:',option1.theta()/365)
print('Rho(%):',option1.rho()/100)




