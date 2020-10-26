import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"

alba_jobs = []

result = requests.get(alba_url)

soup = BeautifulSoup(result.text, 'html.parser')

super_brand = soup.find('div',{'id':'MainSuperBrand'})

brand_list = super_brand.find_all('li',{'class':'impact'})

def extract_job(html):
  tbody = html.find('tbody')
  rows = tbody.find_all('tr')
  a_company_jobs = []
  for row in rows:
    items = row.find_all('td')
    try:
      place = items[0].text
      title = items[1].find('span',{'class':'title'}).text
      time_ = items[2].text
      pay = items[3].text
      date_ = items[4].text
      a_company_jobs.append({'place':place, 'title':title, 'time_':time_, 'pay':pay, 'date_':date_})
    except:
      pass
  return a_company_jobs

def save_to_file(alba_jobs):
  count = 1
  for job in alba_jobs:
    print(f'{count} company has finished')
    for name, jb in job.items():
      file = open(f'{name}.csv', mode = 'w', encoding = 'utf-8')
      writer = csv.writer(file)
      writer.writerow(["place", "title", "time", "pay", "date"])
      for j in jb:
        writer.writerow(list(j.values()))
      file.close()
    count += 1

count = 1
for brand in brand_list:
  print(f'Scrapping albaheaven brand {count}')
  company = brand.find('span', {'class':'company'}).get_text()
  link = brand.find('a')['href']
  result = requests.get(link)
  soup = BeautifulSoup(result.text, 'html.parser')
  jobs = extract_job(soup)
  alba_job = {f'{company}':jobs}
  alba_jobs.append(alba_job)
  count += 1
save_to_file(alba_jobs)

      