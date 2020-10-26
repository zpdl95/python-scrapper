import requests
from flask import Flask, render_template, request
import json
import os
os.system('clear')

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
    return f"{base_url}/items/{id}"


db = {}
app = Flask("DayNine")

def get_html(html):
    list_hits = []
    result_html = requests.get(html)
    html_html = json.loads(result_html.text)
    hits = html_html['hits']
    for hit in hits:
        html_row = {
            'title': hit['title'],
            'url': hit['url'],
            'author': hit['author'],
            'points': hit['points'],
            'num_comments': hit['num_comments'],
            'objectID': hit['objectID']
        }
        list_hits.append(html_row)
        
    return list_hits


@app.route("/")
def index():
    order_by = request.args.get('order by')
    if order_by:
      if order_by == 'new':
        if db.get(order_by):
          list_hits = db.get(order_by)
        else:
          list_hits = get_html(new)
          db[order_by] = list_hits
      elif order_by == 'popular':
        list_hits = db.get(order_by)
    else:
      list_hits = get_html(popular)
      order_by = 'popular'
      db[order_by] = list_hits
    order_by = order_by.capitalize()

    return render_template("index.html", list_hits = list_hits, order_by = order_by)

@app.route("/<objectID>")
def detail(objectID):
    result_detail = requests.get(make_detail_url(objectID))
    html_detail = json.loads(result_detail.text)

    return render_template("detail.html", html_detail = html_detail)


app.run(host="0.0.0.0")
