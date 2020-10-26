import requests
from bs4 import BeautifulSoup

def get_last_page(url):
    result = requests.get(url)

    soup = BeautifulSoup(result.text, 'html.parser')

    pages = soup.find('div', {'class': 's-pagination'}).find_all('a')
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    title = html.find('a', {'class': 's-link'})['title']
    company, location = html.find('h3', {
        'class': 'mb4'
    }).find_all(
        'span', recursive=False)  #recursive는 첫번째 level인자만 받는다
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id = html['data-jobid']
    link = f'https://stackoverflow.com/jobs/{job_id}'
    return {
        'title': title,
        'company': company,
        'link': link
    }


def extract_jobs(last_page, url, headers):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{url}&pg={page+1}", headers=headers)
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('div', {'class': 'js-result'})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word, headers):
    url = f'https://stackoverflow.com/jobs?r=true&q={word}'
    last_page = get_last_page(url)
    jobs = extract_jobs(2, url, headers)
    print(len(jobs),'stack count')
    return jobs
