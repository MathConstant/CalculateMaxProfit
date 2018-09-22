
import pandas as pd
import numpy as np
import math

bitcoin_prices = pd.read_csv('market-price.csv', header=None)

# level 1
def calculate_max_potential_profit(prices):
        profit = 0
        lowest = prices.iloc[0][1]
        for index, row in prices.iterrows():
            lowest = min(lowest, row[1])
            profit = max(profit, row[1] - lowest)
        return profit


print("calculate_max_potential_profit   ", calculate_max_potential_profit(bitcoin_prices))

# level 2
# assuming that you can only buy or sell once per day
# as the other case would be level 1 *5 - 2* lowest
def calculate_max_potential_profit_2 (prices):
    profit = [0] * 3
    lowest = [float("inf")] + [0] * 4

    for index, row in prices.iterrows():
        i = 0
        while i < 5:
            if row[1] < lowest[i]:
                lowest.insert(i, row[1])
                del lowest[5]
                break
            i += 1
        i = 0
        while i < 3:  # only one loop here as to ensure that multiple profits don't use the same lowest value
            if row[1] - lowest[i] > profit[i]:
                profit[i] = row[1] - lowest[i]
                break
            i += 1
    return profit[0] + profit[1] + profit[2] - lowest[-1] - lowest[-2]


print ("calculate_max_potential_profit_2 ", calculate_max_potential_profit_2 (bitcoin_prices))


# level 3

def calculate_transaction_fee(x):
    return math.log(x) + 0.07 * x


def calculate_max_potential_profit_3 (prices):
    profit = [0] * 3
    lowest = [float("inf")] + [0] * 4

    for index, row in prices.iterrows():
        i = 0
        while i < 5:
            if row[1] + calculate_transaction_fee(row[1]) < lowest[i]:
                lowest.insert(i, row[1] + calculate_transaction_fee(row[1]))
                del lowest[5]
                break
            i += 1
        i = 0
        while i < 3:  # only one loop here as to ensure that multiple profits don't use the same lowest value
            if  row[1] - calculate_transaction_fee(row[1]) - lowest[i] > profit[i]:
                profit[i] = row[1] - calculate_transaction_fee(row[1]) - lowest[i]
                break
            i += 1
    return profit[0] + profit[1] + profit[2] - lowest[-1] - lowest[-2]


print ("calculate_max_potential_profit_3 ", calculate_max_potential_profit_3 (bitcoin_prices))

# level 4
test_data = historical_data = bitcoin_prices
test_data [0] = historical_data [0] = pd.to_datetime(historical_data [0])
mask = (historical_data [0] >= '2017-02-07') & (historical_data [0] <= '2017-12-31')
historical_data = historical_data.loc[mask]
test_data = test_data.loc[(test_data [0] > '2017-12-31')]

usd_balance = 29341   # USD balance
btc_balance = 0       # Bitcoin balance

#print (test_data)
def buy(price):
    adjusted_price = price + calculate_transaction_fee(price)
    if usd_balance >= adjusted_price:
        usd_balance -= adjusted_price
        btc_balance += 1
    else:
        raise RuntimeError('not enough USD balance')


def sell(price):
    adjusted_price = price - calculate_transaction_fee(price)
    if btc_balance >= 1:
        usd_balance += adjusted_price
        btc_balance -= 1
    else:
        raise RuntimeError('not enough BTC balance')


def run ():
    # could check average length of price drops in historical data then buy if the price has been droping for that amount of time
    # then sell if the profit is within some margin (say 20%) of the max profit in the last month (or two weeks)
    return 0


# level 2 debug version
# assuming that you can only buy or sell once per day
def calculate_max_potential_profit_2_debug (prices):
    profit = [[-1, -1, 0]] * 3
    lowest = [[0, float("inf")]] + [[-1, 0]] * 4

    for index, row in prices.iterrows():
        i = 0

        while i < 5:
            if row[1] < lowest[i][1]:
                lowest.insert(i, [index, row[1]])
                del lowest[5]
                break
            i += 1
        i = 0
        while i < 3:
            if row[1] - lowest[i][1] > profit[i][2]:
                profit[i] = [lowest[i][0],index, row[1] - lowest[i][1]]
                break
            i += 1
    print (lowest)
    print(profit)
    return profit[0][2] + profit[1][2] + profit[2][2] - lowest[-1][1] - lowest[-2][1]