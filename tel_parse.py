import requests
import re

country_code = ['7', '8']
region_code_first_number = ['1', '3', '4', '5', '6', '7', '8', '9']

def is_valid_phone(test_number):
  result_number = ''
  for digit in test_number:
    if digit.isdigit():
      result_number+=digit

  if (((len(result_number) == 7) and (result_number[0] in region_code_first_number)) or 
      ((len(result_number) == 11) and (result_number[0] in country_code) and (result_number[1] in region_code_first_number))):
      return True

  return False

def format_phone(test_number):
  result_number = ''
  for digit in test_number:
    if digit.isdigit():
      result_number+=digit

  if len(result_number) <= 7:
    return '8495' + result_number
  
  return '8' + result_number[1:]

def is_connection_successful(recall, url):
  return recall == 200

def parse(url):
  page = requests.get(url)

  if not is_connection_successful(page.status_code, url):
    print('Failure to connect to: ', url, '. \nError code: ', page.status_code, sep = '')
    return

  phones_found = map(format_phone, re.findall(r'[\+7|8]?[\- ]?[\(]?[\d]{3}[\)]?[\- ]?[\d\- ]{7,10}', page.text))
  phones_found = {phone for phone in phones_found if is_valid_phone(phone)}
  
  #сначала форматировать все, засунуть в множество, проверенные вывести
  
  return phones_found

#asserts на два адреса ['https://hands.ru/company/about', 'https://repetitors.info']

assert parse('https://hands.ru/company/about') == {'84951370720'}, "Ошибка в поиске по https://hands.ru/company/about"
assert parse('https://repetitors.info') == {'84955405676'}, "Ошибка в поиске по https://repetitors.info"
