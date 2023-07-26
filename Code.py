# Installing and importing libraries

!pip install yfinance==0.1.67
!mamba install bs4==4.10.0 -y
!pip install nbformat==4.2.0

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Graph function

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

# Extracting Tesla Stock Data using yfinance function

tesla = yf.Ticker('TSLA')
tesla_data = tesla.history(period = 'max')
tesla_data.reset_index(inplace = True)
tesla_data.head()

# Extracting Tesla Revenue Data using requests function

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url).text

# Parsing the data using BeautifulSoup

soup = BeautifulSoup(html_data)

# Creating a new dataframe and filling it with the Tesla Revenue Data

tesla_revenue = pd.DataFrame(columns = ["Date", "Revenue"])

for row in soup.find_all("tbody")[1].find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    
    tesla_revenue = tesla_revenue.append({"Date":date, "Revenue":revenue}, ignore_index = True)

# Removing symbols and null values

tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

# Output last 5 rows to make sure everything is right

tesla_revenue.tail()

# Extracting GameStop Stock Data using yfinance function

gamestop = yf.Ticker("GME")
gme_data = gamestop.history(period = 'max')
gme_data.reset_index(inplace = True)
gme_data.head()

# Extracting GameStop Revenue Data using requests function

url1 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data = requests.get(url1).text

# Parsing the data using BeautifulSoup

soup_gme = BeautifulSoup(html_data)

# Creating a new dataframe and filling it with the GameStop Revenue Data

gme_revenue = pd.DataFrame(columns = ["Date", "Revenue"])

for row in soup_gme.find_all("tbody")[1].find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    
    gme_revenue = gme_revenue.append({"Date":date, "Revenue":revenue}, ignore_index = True)

# Removing symbols and null values
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"")
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

# Output last 5 rows to make sure everything is right
gme_revenue.tail()

# Plotting Tesla Stock Graph

make_graph(tesla_data, tesla_revenue, "Tesla")

# Plotting GameStop Stock Graph

make_graph(gme_data, gme_revenue, "GameStop")
