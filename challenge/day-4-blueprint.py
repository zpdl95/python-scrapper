import os
import requests
from bs4 import BeautifulSoup

os.system("clear")
url = "https://www.iban.com/currency-codes"

def extrack_country_code(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, 'html.parser')
  table = soup.find('table',{'class':'table'})
  country_tr = table.find_all('tr')
  country_tr = country_tr[1:]
  return country_tr

def country_list_create(country_tr):
  country_index_list = []
  country_name_list = []
  country_code_list = []
  code_num_list = []
  num = 0
  for tr in country_tr:
    td = tr.find_all('td')
    con_list = []
    for i in td:
      i = i.string
      con_list.append(i)
    if None not in con_list:
      country_index_list.append(f'# {num} ' + con_list[0])
      country_name_list.append(con_list[0])
      country_code_list.append(con_list[2])
      code_num_list.append(num)
      num += 1
  return country_index_list, country_code_list, code_num_list, country_name_list


def ask_code(code_num_list, country_code_list, country_name_list):
  try:
    country_num = int(input('#: '))
    if country_num not in code_num_list:
      print('Choose a number from the list!')
      ask_code(code_num_list, country_code_list, country_name_list)
    else:
      print(f"You chose {country_name_list[country_num]}\nThe currency code is {country_code_list[country_num]}")   
  except:
    print("That wasn't a number!")
    ask_code(code_num_list, country_code_list, country_name_list)

def start():
  country_tr = extrack_country_code(url)
  country_index_list, country_code_list, code_num_list, country_name_list = country_list_create(country_tr)
  print('Hello! Please choose select a country by number:')
  for i in country_index_list:
    print(i)
  ask_code(code_num_list, country_code_list, country_name_list)

start()