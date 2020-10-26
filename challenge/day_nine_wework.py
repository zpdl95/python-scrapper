import requests
from bs4 import BeautifulSoup

def extract_job(html):
    title = html.find('span', {'class': 'title'}).text
    company = html.find('span', {'class': 'company'}).text
    link = html.find('a', recursive=False)['href']
    link = 'https://weworkremotely.com' + link
    return {'title': title, 'company': company, 'link': link}


def extract_jobs(url, headers):
    jobs = []
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all('li', {'class': 'feature'})
    for result in results:
        job = extract_job(result)
        jobs.append(job)
    return jobs


def get_jobs(word, headers):
    url = f'https://weworkremotely.com/remote-jobs/search?term={word}'
    jobs = extract_jobs(url, headers)
    print(len(jobs),'wework count')
    return jobs
