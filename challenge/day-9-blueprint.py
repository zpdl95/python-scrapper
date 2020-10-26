"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
from flask import Flask, render_template, request, redirect, send_file
from day_nine_stack import get_jobs as stack_get_jobs
from day_nine_wework import get_jobs as wework_get_jobs
from day_nine_remoteok import get_jobs as remoteok_get_jobs
from day_nine_exporter import save_to_file
import os
os.system('clear')

headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
}

db = {}
app = Flask("ScrappingJobs")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    word = request.args.get("term")
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            stack_jobs = stack_get_jobs(word, headers)
            wework_jobs = wework_get_jobs(word, headers)
            remoteok_jobs = remoteok_get_jobs(word, headers)
            jobs = stack_jobs + wework_jobs + remoteok_jobs
            db[word] = jobs
    else:
        return redirect("/")
    return render_template("search.html", word=word, jobs=jobs, resultsNumber=len(jobs))


@app.route("/export")
def export():
  try:
    word = request.args.get('term')
    if not word:
      raise Exception()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs, word)
    return send_file(f"{word}-jobs.csv", as_attachment=True)
  except:
    return redirect("/")


app.run(host="0.0.0.0")
