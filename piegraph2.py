import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpld3

def download_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    data['Daily Return'] = data['Adj Close'].pct_change()
    return data

def calculate_sharpe_ratio(data, risk_free_rate=0.0):
    mean_return = data['Daily Return'].mean()
    std_return = data['Daily Return'].std()
    sharpe_ratio = (mean_return - risk_free_rate) / std_return
    return sharpe_ratio

def calculate_sortino_ratio(data, risk_free_rate=0.0):
    mean_return = data['Daily Return'].mean()
    target = 0
    data['Downside'] = np.where(data['Daily Return'] < target, data['Daily Return'], 0)
    downside_deviation = np.sqrt((data['Downside'] ** 2).mean())
    sortino_ratio = (mean_return - risk_free_rate) / downside_deviation
    return sortino_ratio

''' need to check this calcuation'''
def calculate_omega_ratio(data, threshold=0.0):
    print("in calculate omega_ratio")
    gains = data[data['Daily Return'] > threshold]['Daily Return'].sum()
    losses = -data[data['Daily Return'] < threshold]['Daily Return'].sum()
    print(f"gains={gains} - losses{losses}")
    omega_ratio = gains / losses

    print(f"omega_ratio={omega_ratio} ")
    return omega_ratio

def calculate_calmar_ratio(data):
    mean_return = data['Daily Return'].mean() * 252
    max_drawdown = data['Adj Close'].expanding(min_periods=1).max().pct_change().min()
    calmar_ratio = mean_return / abs(max_drawdown)
    return calmar_ratio

def calculate_martin_ratio(data, risk_free_rate=0.0):
    mean_return = data['Daily Return'].mean() - risk_free_rate
    max_drawdown = data['Adj Close'].expanding(min_periods=1).max().pct_change().min()
    data['Drawdown'] = data['Adj Close'].expanding(min_periods=1).max() - data['Adj Close']
    ulcer_index = np.sqrt((data['Drawdown'] ** 2).mean())
    martin_ratio = mean_return / ulcer_index
    return martin_ratio

def calculate_treynor_ratio(data, beta, risk_free_rate=0.0):
    mean_return = data['Daily Return'].mean() - risk_free_rate
    treynor_ratio = mean_return / beta
    return treynor_ratio

def calculate_information_ratio(data, benchmark_data):
    active_return = data['Daily Return'] - benchmark_data['Daily Return']
    mean_active_return = active_return.mean()
    tracking_error = active_return.std()
    information_ratio = mean_active_return / tracking_error
    return information_ratio

def plot_pie_chart(labels, sizes, title):
    print(labels, sizes, title)
    colors = plt.cm.Paired(np.arange(len(labels)))
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(title)
    return fig

def save_html(figures, filename):
    html_str = ""
    for fig in figures:
        html_str += mpld3.fig_to_html(fig)
    with open(filename, 'w') as f:
        f.write(html_str)

# Example usage
ticker = 'BTC-USD'
benchmark_ticker = '^GSPC'  # S&P 500 as an example benchmark
start_date = '2021-01-01'
end_date = '2022-01-01'
risk_free_rate = 0.0  # Assume risk-free rate is 0 for simplicity
beta = 1  # Assume beta is 1 for simplicity in this example

data = download_data(ticker, start_date, end_date)
benchmark_data = download_data(benchmark_ticker, start_date, end_date)

sharpe_ratio = calculate_sharpe_ratio(data, risk_free_rate)
sortino_ratio = calculate_sortino_ratio(data, risk_free_rate)
#removed omega ratio due to calculation error
#omega_ratio = calculate_omega_ratio(data)
calmar_ratio = calculate_calmar_ratio(data)
martin_ratio = calculate_martin_ratio(data, risk_free_rate)
treynor_ratio = calculate_treynor_ratio(data, beta, risk_free_rate)
information_ratio = calculate_information_ratio(data, benchmark_data)

ratios = {
    'Sharpe Ratio': sharpe_ratio,
    'Sortino Ratio': sortino_ratio,
    #'Omega Ratio': omega_ratio,
    #'Calmar Ratio': calmar_ratio,
    'Martin Ratio': martin_ratio,
    'Treynor Ratio': treynor_ratio,
    'Information Ratio': information_ratio
}

figures = []
for ratio_name, ratio_value in ratios.items():
    print(f"ratio_name={ratio_name} -  ratio_value={ratio_value}")
    fig = plot_pie_chart([ratio_name, 'Remaining'], [ratio_value, 1-ratio_value], f'{ratio_name} (relative to 1)')
    figures.append(fig)

save_html(figures, 'temp_html/financial_ratios.html')
print(f'Financial ratios saved to financial_ratios.html')
