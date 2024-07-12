import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_sortino_ratio(ticker, start_date, end_date, risk_free_rate=0.0):
    # Download historical data
    data = yf.download(ticker, start=start_date, end=end_date)
    
    # Calculate daily returns
    data['Daily Return'] = data['Adj Close'].pct_change()
    
    # Calculate expected return
    mean_return = data['Daily Return'].mean()
    
    # Calculate downside deviation
    target = 0
    data['Downside'] = np.where(data['Daily Return'] < target, data['Daily Return'], 0)
    downside_deviation = np.sqrt((data['Downside'] ** 2).mean())
    
    # Calculate Sortino ratio
    sortino_ratio = (mean_return - risk_free_rate) / downside_deviation
    
    return sortino_ratio

def plot_sortino_ratio_pie(sortino_ratio, benchmark=1.0):
    # Data to plot
    labels = ['Sortino Ratio', 'Remaining']
    sizes = [sortino_ratio, benchmark - sortino_ratio]
    colors = ['gold', 'lightgray']
    explode = (0.1, 0)  # explode 1st slice

    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(f'Sortino Ratio Relative to Benchmark ({benchmark})')
    plt.show()

# Example usage
ticker = 'BTC-USD'
start_date = '2021-01-01'
end_date = '2022-01-01'
risk_free_rate = 0.0  # Assume risk-free rate is 0 for simplicity

sortino_ratio = calculate_sortino_ratio(ticker, start_date, end_date, risk_free_rate)
print(f'Sortino Ratio for {ticker} from {start_date} to {end_date}: {sortino_ratio}')

# Plot Sortino ratio as a pie chart
plot_sortino_ratio_pie(sortino_ratio)
