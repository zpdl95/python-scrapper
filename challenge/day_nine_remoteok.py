import requests
from bs4 import BeautifulSoup


def extract_job(html):
    judge = html.find('td', {'class': 'source'}).find('a')
    if judge != None:
        title = html.find('h2', {'itemprop': 'title'}).text
        company = html.find('h3', {'itemprop': 'name'}).text
        link = html.find('td', {
            'class': 'company_and_position'
        }).find('a')['href']
        link = 'https://remoteok.io/' + link
        return {'title': title, 'company': company, 'link': link}


def extract_jobs(url, headers):
    jobs = []
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all('tr', {'class': 'job'})
    for result in results:
        job = extract_job(result)
        if job != None:
          jobs.append(job)
    return jobs


def get_jobs(word, headers):
    url = f'https://remoteok.io/remote-dev+{word}-jobs'
    jobs = extract_jobs(url, headers)
    print(len(jobs),'remoteok count')
    return jobs
