import smtplib
import requests

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
DATE_1 = "2024-04-24"
DATE_2 = "2024-04-23"
STOCK_API_KEY = "***********"
NEWS_API_KEY = "********************"
EMAIL = "*****@*****.com"
PASS = "************"

# Getting the stock value form the Stock API
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}

# link = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey=**********"

response = requests.get("https://www.alphavantage.co/query", params=parameters)
response.raise_for_status()
stock_data = response.json()
print(stock_data)

yesterdays_closing_data = float(stock_data["Time Series (Daily)"][DATE_1]["4. close"])
print(yesterdays_closing_data)
thedaybefore_closing_data = float(stock_data["Time Series (Daily)"][DATE_2]["4. close"])
print(thedaybefore_closing_data)

percentage_change = round((((yesterdays_closing_data - thedaybefore_closing_data) / thedaybefore_closing_data) * 100), 2)
print(percentage_change)

percentage_symbol_value = ""

if percentage_change > 5:
    percentage_symbol_value = f"🔺 {percentage_change}%"
elif percentage_change < -5:
    percentage_symbol_value = f"🔻 {percentage_change}%"


# Getting the news of the company from API


parameters_news = {
    "q": COMPANY_NAME,
    "from": DATE_2,
    "to": DATE_1,
    "sortBy": "popularity",
    "apiKey": NEWS_API_KEY,
}

# link = "https://newsapi.org/v2/everything?q=Tesla Inc&from=2024-04-23&to=2024-04-24&sortBy=popularity&apiKey=**************"

news_response = requests.get("https://newsapi.org/v2/everything", params=parameters_news)
news_response.raise_for_status()
news_data = news_response.json()
print(news_data)

news_title = news_data["articles"][0]["description"]
print(news_title)
news_content = news_data["articles"][0]["content"]
print(news_content)

# Sending Email with the relevant info

with smtplib.SMTP(host="smtp.****@***.com", port=587) as connection:
    connection.starttls()
    connection.login(user=EMAIL, password=PASS)
    connection.sendmail(
        from_addr=EMAIL,
        to_addrs="*****@*****.com",
        msg=f"Subject: {STOCK}: {percentage_symbol_value}\n\nHeadline: {news_title}\nBrief: {news_content}")






