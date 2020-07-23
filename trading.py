# constant
SELL = 'sell'
BUY = 'buy'
NONE = 'none'

# global variables
curPrice = 0

def randomTrade(balance, marketData):
    '''
    A random trading algorythm to test validating function

     Parameters:
        balance (list): the original balance [base_asset, quote_asset]
        marketData (pandas.dataframe): The trading data of market - columns['timestamp', 'openVal', 'high', 'low', 'closeVal', 'volume']

    Returns:
        list: [decision, trading_amount]
              decision: 'sell'/'buy'/'none'
              trading_amount: 1 by default 
    '''
    if balance[1] > marketData['openVal'].iloc[-1]:
        if marketData['openVal'].iloc[-1] >= curPrice and curPrice > 0:
            return (SELL, 1)
        if marketData['openVal'].iloc[-1] < curPrice or curPrice == 0:
            return (BUY, 1)
        return (NONE, 1)
    if marketData['openVal'].iloc[-1] >= curPrice and curPrice > 0:
        return (SELL, 1)
    return (NONE, 1)
