import requests
from bs4 import BeautifulSoup
import os
os.system('clear')

LIMIT = 50

URL = f'https://www.indeed.com/jobs?q=python&limit={LIMIT}'


def get_last_pages():
    result = requests.get(URL)

    soup = BeautifulSoup(result.text, 'html.parser')

    pagination = soup.find('div', {'class': 'pagination'})

    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    last_page = max(pages)
    return last_page


def extract_job(html):
    title = html.find('h2', {'class': 'title'}).find('a')['title']
    company = html.find('span', {'class': 'company'})
    company_anchor = company.find('a')
    if company_anchor is not None:
        company = company_anchor.get_text(strip=True)
    else:
        company = company.get_text(strip=True)
    location = html.find('div', {'class': 'recJobLoc'})['data-rc-loc']
    job_id = html['data-jk']
    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f'https://www.indeed.com/viewjob?jk={job_id}'
    }


def extrack_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f'Scrapping indeed page {page}')
        result = requests.get(f'{URL}&start={page*LIMIT}')
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('div', {'class': 'jobsearch-SerpJobCard'})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_pages = get_last_pages()

    jobs = extrack_jobs(last_pages)

    return jobs
