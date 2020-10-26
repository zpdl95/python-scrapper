import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import os
os.system('clear')
"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
}
"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = [
    "javascript", "reactjs", "reactnative", "programming", "css", "golang",
    "flutter", "rust", "django"
]

app = Flask("DayEleven")


@app.route("/")
def home():
    return render_template("home.html", subreddits=subreddits)


@app.route("/read")
def read():
    reading = []
    results = []
    args = list(request.args.to_dict().keys())
    for subreddit in args:
        url = f'https://www.reddit.com/r/{subreddit}/top/?t=month'
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.text, 'html.parser')
        box = soup.find('div', {'class': 'rpBJOHq2PR60pnwJlUyP0'})
        box_box_list = box.find_all('div',
                                    {'class': '_1oQyIsiPHYt6nx7VOmd1sz'})
        print(len(box_box_list))
        for i in box_box_list:
            title = i.find('h3', {'class': '_eYtD2XCVieq6emjKBH3m'}).text
            upvotes = i.find('div', {'class': '_23h0-EcaBUorIHC-JZyh6J'}).text
            link = i.find('a')['href']
            if 'k' in upvotes:
                upvotes = int(float(upvotes.strip('k')) * 1000)
            elif '•' in upvotes:
                continue
            else:
                upvotes = int(upvotes)
            result = {
                'title': title,
                'link': link,
                'upvotes': upvotes,
                'script': f'r/{subreddit}'
            }
            results.append(result)
        reading.append(f"r/{subreddit}")
    results = sorted(results, key=lambda result: result['upvotes'], reverse=True)
    return render_template("read.html", results=results, reading=reading)


app.run(host="0.0.0.0")
