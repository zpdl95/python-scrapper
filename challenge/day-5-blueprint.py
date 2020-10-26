import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

os.system("clear")
"""
Use the 'format_currency' function to format the output of the conversion
format_currency(AMOUNT, CURRENCY_CODE, locale="ko_KR" (no need to change this one))
"""

# print(format_currency(43.77375, "USD", locale="ko_KR"))

code_url = "https://www.iban.com/currency-codes"


def extrack_currency_convert(from_cur, to_cur, amount):
    result = requests.get(
        f"https://transferwise.com/gb/currency-converter/{from_cur}-to-{to_cur}-rate?amount={amount}"
    )
    soup = BeautifulSoup(result.text, 'html.parser')
    rate = soup.find('span', {'class': 'text-success'}).string
    currency = amount * float(rate)
    print(f"\n{from_cur}",
          format_currency(amount, f"{from_cur}", locale="ko_KR"), "is",
          format_currency(currency, f"{to_cur}", locale="ko_KR"))


def extrack_country_code(code_url):
    result = requests.get(code_url)
    soup = BeautifulSoup(result.text, 'html.parser')
    table = soup.find('table', {'class': 'table'})
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


def convert_currency(country_code_list, country_num, another_country_num):
    print(
        f'How many {country_code_list[country_num]} do you want to convert to {country_code_list[another_country_num]}.\n'
    )
    from_cur = country_code_list[country_num]
    to_cur = country_code_list[another_country_num]
    try:
        amount = int(input())
        extrack_currency_convert(from_cur, to_cur, amount)
    except:
        print("That wasn't a number.")
        convert_currency(country_code_list, country_num, another_country_num)


def ask_code(code_num_list, country_code_list, country_name_list):
    try:
        country_num = int(input('#: '))
        if country_num not in code_num_list:
            print('Choose a number from the list!')
            ask_code(code_num_list, country_code_list, country_name_list)
        else:
            print(f"{country_name_list[country_num]}\n")
            print('Now choose another country.\n')
            try:
                another_country_num = int(input('#: '))
                if another_country_num not in code_num_list:
                    print('Choose a number from the list!')
                    ask_code(code_num_list, country_code_list,
                             country_name_list)
                else:
                    print(f"{country_name_list[another_country_num]}\n")
                    convert_currency(country_code_list, country_num,
                                     another_country_num)
            except:
                print("That wasn't a number!")
                ask_code(code_num_list, country_code_list, country_name_list)

    except:
        print("That wasn't a number!")
        ask_code(code_num_list, country_code_list, country_name_list)


def start():
    country_tr = extrack_country_code(code_url)
    country_index_list, country_code_list, code_num_list, country_name_list = country_list_create(
        country_tr)
    print('Welcome to CurrencyConvert PRO 2000\n')
    for i in country_index_list:
        print(i)
    print('\nWhere are you from? Choose a country by number.\n')
    ask_code(code_num_list, country_code_list, country_name_list)


start()
