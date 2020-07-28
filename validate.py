def validate(marketData, tradingAlgorythm, window, balance):
    """ 
    Validate a trading algorythm

    Parameters:
        marketData (pandas.dataframe): The trading data of market - columns['timestamp', 'openVal', 'high', 'low', 'closeVal', 'volume']
        tradingAlgorythm (function): trading function. return: [decision: 'sell'/'buy'/'none', tradingAmount: number]
        window (number): the amount of the latest marketData's ticker which is given to tradingAlgoruthm to make decision.
        balance (list): the original balance [base_asset, quote_asset]

    Returns:
        number: the amount of quote asset in balance after trading with trading algorythm and given market data.
    """
    for i, ticker in marketData.iterrows():
        # Pass current balance and <window> latest ticker to trading algorythm
        start = i - window + 1 if i >= window-1 else 0
        end = i + 1
        decision, tradingAmount = tradingAlgorythm(
            balance, marketData.iloc[start:end])

        # Recalculate balance after make decision
        if decision == 'sell':
            balance[0] -= tradingAmount
            balance[1] += tradingAmount * ticker['openVal']
        elif decision == 'buy':
            balance[0] += 1
            balance[1] -= tradingAmount * ticker['openVal']
        else:
            continue

    finalBalance = balance[1] + balance[0] * marketData.iloc[-1]['openVal']
    return finalBalance
