import requests
import os

url_list=[]
urls = []

def restart():
  y_n = input('Do you want to start over? y/n ')
  if y_n == 'y':
    init()
  elif y_n == 'n':
    print('k.bye!')
  else:
    print("That's not a valid answer")
    restart()
  
def up_down(urls):
  for url in urls:
    try:
      url_result = requests.get(url)
      if url_result.status_code == 200:
        print(f'{url}'+' is up!')
      else:
        print(f'{url}'+' is down!')
    except:
      print(f'{url}'+' is down!')

def http_test(urls):
  http_url = []
  for url in urls:
    if url[0:7] =='http://' or url[0:8] == 'https://':
      http_url.append(url)
    else:
      http_url.append('https://' + url)
  return http_url

def com_test(urls):
  com_url = []
  for url in urls:
    if url[-4:] == '.com':
      com_url.append(url)
    else:
      print(f"{url} is not valid URL")
      restart()
  return com_url

def url_strip(urls):
  strip_url = []
  for url in urls:
    strip_url.append(url.strip())
  return strip_url

def url_split(urls):
  return urls.split(',')

def init():
  os.system('clear')
  print('Welcome to IsItDown.py!')
  print('Please write a URL or URLs you want to check.(separated by comma)')
  input_url = input().lower()
  url_list = url_split(input_url)
  url_list = url_strip(url_list)
  url_list = com_test(url_list)
  url_list = http_test(url_list)
  up_down(url_list)
  restart()
init()