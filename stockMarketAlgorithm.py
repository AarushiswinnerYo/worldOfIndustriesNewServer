import random 
import time
import asyncio 
import threading
import numpy as np
from dataHandle import load_data
import matplotlib.pyplot as plt
from collections import deque

trends = ["Bear", "Bull", "random", "saturated", "sudden"],

#set scaling to 1 for releastic change in stockmarket price 
# it is set 5 change price quickly
# we can set trend by generating array [deviation_no, profit_or_loss, no_of_ticks]
global stock_trends
stock_trends = np.ndarray

scale = 1

def load_data_into_array() -> tuple:
    data: dict = load_data()
    stocks: dict = data['stocks']
    length_of_inventory: int = len(stocks)
    price_of_stocks: np.ndarray = np.zeros(length_of_inventory)
    for index, stock in enumerate(stocks, start=0):
        price_of_stocks[index] = stock["price"]

    global stock_trends
    stock_trends = np.ones([length_of_inventory, 3])

    return price_of_stocks, length_of_inventory


def get_price_change(price_of_stocks: np.ndarray, length_of_inventory: int, scale=scale) -> np.ndarray:
    random_deviation_array: np.ndarray = scale * np.random.uniform(0.000005, 0.0025, (1, length_of_inventory))
    global stock_trends
    result = price_of_stocks * random_deviation_array
    stock_trends[:, 0] = result
    return result


def profit_or_loss(price_of_stocks: np.ndarray, length_of_inventory: int, random_deviation_array: np.ndarray):    
    for i in range(length_of_inventory):
        chance = random.choice([1, -1])
        random_deviation_array[i] *= int(chance)
    price_of_stocks += random_deviation_array


def generate_trends(length_of_inventory: int):
    global stock_trends
    frame_column = np.random.randint(15, 90, (1, length_of_inventory))
    stock_trends[:, 2] = frame_column
    trend_column = np.random.choice([0, 1, 2, 3, 4], (1, length_of_inventory), p=[0.5, 0.2, 0.2, 0.05, 0.05])
    stock_trends[:, 1] = trend_column 


def reset_trend(stock_index: int, length_of_inventory:int):
    frame_no = np.random.randint(15, 90)
    trend_column = np.random.choice([0, 1, 2, 3, 4], (1), p=[0.5, 0.2, 0.2, 0.05, 0.05])

    global stock_trends
    stock_trends[stock_index, 2] = frame_no
    stock_trends[stock_index, 1] = trend_column

def check_trend_for_reset(length_of_inventory: int):
    global stock_trends
    for i, trend in enumerate(stock_trends[:, 2]):
        if trend <= 0:
            reset_trend(i, length_of_inventory)


def if_profit_or_loss(length_of_inventory: int):
    random_trend_prob = [1, 1] 
    bearish_trend_prob = [2, 1]
    bullish_trend_prob = [1, 2]
    highly_bear_trend = [85, 15]
    highly_bull_trend = [15, 85]
    global stock_trends
    for i, trends in enumerate(stock_trends[:, 1]):
        if trends == 0:
            profit_or_loss = random.choices([-1.0, 1.0], weights=random_trend_prob)
            stock_trends[i, 0] *= np.float64(profit_or_loss)

        elif trends == 1:
            profit_or_loss = random.choices([-1.0, 1.0], weights=bearish_trend_prob)
            stock_trends[i, 0] *= np.float64(profit_or_loss)

        elif trends == 2:
            profit_or_loss = random.choices([-1.0, 1.0], weights=bullish_trend_prob)
            stock_trends[i, 0] *= np.float64(profit_or_loss)

        elif trends == 3:
            profit_or_loss = random.choices([-1.0, 1.0], weights=highly_bear_trend)
            stock_trends[i, 0] *= np.float64(profit_or_loss)

        elif trends == 4:
            profit_or_loss = random.choices([-1.0, 1.0], weights=highly_bull_trend)
            stock_trends[i, 0] *= np.float64(profit_or_loss)

    counter = np.ones(length_of_inventory)
    stock_trends[:, 2] -= counter


def change_price(price_of_stocks: int, length_of_inventory: int):
    global stock_trends
    difference_array = stock_trends[:, 0].reshape(length_of_inventory)
    price_of_stocks += difference_array
    return price_of_stocks


plt.ion()
fig, ax = plt.subplots()
N = 100  # Number of points to retain
x_data = deque(maxlen=N)
y_data = deque(maxlen=N)
line, = ax.plot([], [], 'r-')

ax.set_xlabel("Time (iterations)")
ax.set_ylabel("Stock Price (a[0])")
ax.set_xlim(0, N)
i=0
stock_index = 24

if __name__ == "__main__":
    a,b = load_data_into_array()
    generate_trends(b)
    while True:
        if_profit_or_loss(b)
        change_price(a, b)
        get_price_change(a, b)
        print(a[stock_index])
        check_trend_for_reset(b)
       
        x_data.append(i)
        y_data.append(a[0])

        # Update only the latest segment of the plot
        line.set_data(list(x_data), list(y_data))

        ax.set_xlim(max(0, i - N), i + 10)  # Keep x-axis moving
        ax.relim()
        ax.autoscale_view()

        plt.draw()
        plt.pause(0.01)  # Shorter pause for better performance
        
        i += 1       

