import smtplib
import requests

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
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

# # Getting only the values from the dictionary
stock_data_list = [value for (key, value) in stock_data.items()]
# print(stock_data_list)
stock_data_list_expand = stock_data_list[1].items()

final_data_list = [value for (key, value) in stock_data_list_expand]

yesterdays_closing_data = float(final_data_list[0]["4. close"])
print(yesterdays_closing_data)

thedaybefore_closing_data = float(final_data_list[1]["4. close"])
print(thedaybefore_closing_data)
#
# ## The below is to extract the data directly from the dictionary
# # yesterdays_closing_data = float(stock_data["Time Series (Daily)"][DATE_1]["4. close"])
# # print(yesterdays_closing_data)
# # thedaybefore_closing_data = float(stock_data["Time Series (Daily)"][DATE_2]["4. close"])
# # print(thedaybefore_closing_data)
#
percentage_change = round((((yesterdays_closing_data - thedaybefore_closing_data) / yesterdays_closing_data) * 100), 2)
print(percentage_change)
#
percentage_symbol_value = ""
#
if percentage_change > 0:
  percentage_symbol_value = "🔺"
else:
  percentage_symbol_value = "🔻"


# Get the latest news, top 3 at least

parameters_news = {
    "q": COMPANY_NAME,
    # "from": DATE_2,
    # "to": DATE_1,
    "sortBy": "popularity",
    "apiKey": NEWS_API_KEY,
}

# link = "https://newsapi.org/v2/everything?q=Tesla Inc&from=2024-04-23&to=2024-04-24&sortBy=popularity&apiKey=ce3a8d2566e74d21a8d172794fcf7c46"

news_response = requests.get("https://newsapi.org/v2/everything", params=parameters_news)
news_response.raise_for_status()
news_data = news_response.json()
# print(news_data)

top_three_articles = news_data["articles"][:3]
print(top_three_articles)

for i in top_three_articles:
  news_title = i["title"]
  # print(news_title)
  news_content = i["description"]
  # print(news_content)

    
  # Sending Email with the relevant info
  
  with smtplib.SMTP(host="smtp.****@***.com", port=587) as connection:
    connection.starttls()
    connection.login(user=EMAIL, password=PASS)
    connection.sendmail(
      from_addr=EMAIL,
      to_addrs="*****@*****.com",
      msg=f"Subject: {STOCK}: {percentage_symbol_value}{abs(percentage_change)}\n\nHeadline: {news_title}\n\nBrief: {news_content}".encode("utf-8"))






