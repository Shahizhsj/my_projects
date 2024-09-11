from flask import Flask, request, jsonify
import os
import pprint
from bs4 import BeautifulSoup
import requests
import yfinance as yf
import re
import pandas as pd
import pandas_ta as ta
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.tools import Tool
from langchain_google_genai import GoogleGenerativeAI
app=Flask(__name__)
#code to return the top5 news of the given stock
def get_stock_price(ticker,history=5):
    # time.sleep(4) #To avoid rate limit error
    if "." in ticker:
        ticker=ticker.split(".")[0]
    ticker=ticker+".NS"
    stock = yf.Ticker(ticker)
    df = stock.history(period="1y")
    df=df[["Close","Volume"]]
    df.index=[str(x).split()[0] for x in list(df.index)]
    df.index.rename("Date",inplace=True)
    df=df[-history:]
    # print(df.columns)

    return df.to_string()

def google_query(search_term):
    if "news" not in search_term:
        search_term=search_term+" stock news"
    url=f"https://www.google.com/search?q={search_term}&cr=countryIN"
    url=re.sub(r"\s","+",url)
    return url
def get_recent_stock_news(company_name):
    # time.sleep(4) #To avoid rate limit error
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

    g_query=google_query(company_name)
    res=requests.get(g_query,headers=headers).text
    soup=BeautifulSoup(res,"html.parser")
    news=[]
    for n in soup.find_all("div","n0jPhd ynAwRc tNxQIb nDgy9d"):
        news.append(n.text)
    for n in soup.find_all("div","IJl0Z"):
        news.append(n.text)

    if len(news)>6:
        news=news[:4]
    else:
        news=news
    news_string=""
    for i,n in enumerate(news):
        news_string+=f"{i}. {n}\n"
    top5_news="Recent News:\n\n"+news_string

    return top5_news
def get_financial_statements(ticker):
    # time.sleep(4) #To avoid rate limit error
    if "." in ticker:
        ticker=ticker.split(".")[0]
    else:
        ticker=ticker

    company = yf.Ticker(ticker)
    balance_sheet = company.balance_sheet
    if balance_sheet.shape[1]>=3:
        balance_sheet=balance_sheet.iloc[:,:3]    # Remove 4th years data
    balance_sheet=balance_sheet.dropna(how="any")
    balance_sheet = balance_sheet.to_string()
    return balance_sheet

def get_stock_analysis(ticker):
  try:
    start_date = "2023-12-01"
    end_date = "2024-02-01"
    data = yf.download(ticker, start=start_date, end=end_date)
    data['SMA_50'] = ta.sma(data['Close'], length=50)
    data['EMA_50'] = ta.ema(data['Close'], length=50)
    data['RSI'] = ta.rsi(data['Close'])
    macd = ta.macd(data['Close'])
    data = pd.concat([data, macd], axis=1)
    bbands = ta.bbands(data['Close'])
    data = pd.concat([data, bbands], axis=1)
    data['ATR'] = ta.atr(data['High'], data['Low'], data['Close'])
    stoch = ta.stoch(data['High'], data['Low'], data['Close'])
    data = pd.concat([data, stoch], axis=1)
    data['OBV'] = ta.obv(data['Close'], data['Volume'])
    ichimoku = ta.ichimoku(data['High'], data['Low'], data['Close'])
    data = pd.concat([data, pd.DataFrame(ichimoku)], axis=1)
    return data[['SMA_50','EMA_50','RSI','BBL_5_2.0','BBM_5_2.0','BBU_5_2.0','BBB_5_2.0','BBP_5_2.0','ATR','STOCHk_14_3_3','STOCHd_14_3_3','OBV']].to_string()
  except:
    return "Nothing to return"
@app.route("/analyze")
def analyze():
    search = DuckDuckGoSearchRun()
    
    ls = [
    Tool(
        name="get stock data",
        func=get_stock_price,
        description="Use for historic share price data.you should input the stock ticker name to it"
    ),
    
    Tool(
        name="DuckDuckGo Search",
        func=search.run,
        description="Use only for NSE/BSE stock ticker or recent stock-related news."
    ),
    Tool(
        name="get recent news",
        func=get_recent_stock_news,
        description="Use to fetch recent news about stocks.you should input the stock ticker name to it"
    ),
    
    Tool(
        name="get technical indicators",
        func=get_stock_analysis,
        description="Use to fetch company's techinical indicator to evaluate its performance.you should input the stock ticker name to it"
    ) 
]

    llm = GoogleGenerativeAI(model="gemini-pro")
    tools = load_tools(["google-search", "google-serper"], llm=llm)+ls
    agent = initialize_agent(tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True,handle_parsing_errors=True, max_execution_time=50)

    query = request.args.get('query', default='*', type=str)
    p="""As a trading expert and intelligence member of the market, your task is to analyze
stocks/companies based on user queries. You are to provide insights using:
Fundamental Analysis: Evaluate the company's financial health, market position, competitive
advantage, revenue, profit margins, and other key financial ratios. Consider recent earnings
reports, management effectiveness, industry conditions, and future growth prospects.
Sentimental Analysis: Assess market sentiment towards the stock/company by analyzing news
articles, investor opinions, social media trends, and overall media coverage. Determine whether
the sentiment is positive, negative, or neutral.
Technical Analysis: Examine stock price movements, trading volumes, historical trends, chart
patterns, and technical indicators such as moving averages, RSI (Relative Strength Index),
MACD (Moving Average Convergence Divergence), and others to predict future price
movements.
Final Conclusion: After conducting the requested analysis, provide a concise conclusion on
whether to invest in the stock/company. This recommendation should only be given if the user
requests investment advice or a comprehensive analysis involving all three aspects mentioned
above.
For each query:
If the user asks specifically for fundamental analysis, provide insights based solely on the
company's financial and market fundamentals.
If the user seeks sentimental analysis, focus on the prevailing sentiment and its potential impact
on the stock.
If the request is for technical analysis, offer an assessment based on price trends and technical
indicators.
Always ensure the analysis is up-to-date, relying on the most recent data and market trends.
Your goal is to deliver precise, concise, and actionable insights to assist users in making
informed investment decisions.
Note:you should use only avilable tools in the efficient manner and you should get the all the informantion at any cost and if you have limited resource try to gather more and more
you should answer the user still you have limited resources
Disclaimer:
Include a disclaimer noting that the recommendation is based on the current market analysis and is subject to change. Remind users to perform their own research before making trading decisions.
Note:
you should answer the user very fastly and with very quickly
output formant:
Analysis Type: Technical | Sentimental | Fundamental | Combined
Overview:
Provide a brief overview of the market conditions and the reason for this specific trader recommendation.
Technical Analysis Summary:

Key Indicators Used: [List of technical indicators, e.g., Moving Averages, RSI, MACD]
Trend Analysis: [Brief summary of the trend analysis findings]
Signal Strength: [Weak/Moderate/Strong]
Technical Outlook: [Bullish/Bearish/Neutral]
Sentimental Analysis Summary:

Market Sentiment: [Positive/Negative/Neutral]
Sentiment Indicators: [List of sentimental indicators used, e.g., news analysis, social media sentiment]
Impact on Recommendation: [Brief summary of how sentiment analysis impacted the recommendation]

Fundamental Analysis Summary:
Key Metrics Analyzed: [List of fundamental metrics, e.g., Earnings, P/E Ratio, Market Cap]
Market Position: [Leader/Follower/Niche]
Financial Health: [Good/Moderate/Poor]
Fundamental Outlook: [Positive/Negative/Neutral]
Rationale for Recommendation:
Provide a detailed explanation of why this trader is recommended based on the analysis. Include any specific strengths or opportunities identified during the analysis.

Risk Assessment:
Market Risk: [Low/Medium/High]
Analysis Confidence Level: [Low/Medium/High]
Potential Challenges: [Briefly list any potential challenges or risks associated with this recommendation]
Conclusion:
Summarize the recommendation and provide any final thoughts or suggestions for the user.

Please make sure that you represented th answer in the above mentioned format(you should do it)
query:"""

    # Use the agent to process the query
    response = agent.run(p+query)
    return jsonify({"response": response})

