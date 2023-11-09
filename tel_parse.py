import requests
import re

country_code = ['7', '8']
region_code_first_number = ['1', '3', '4', '5', '6', '7', '8', '9']

def if_phone(test_number):
  result_number = ''
  for digit in test_number:
    if digit.isdigit():
      result_number+=digit

  match len(result_number):
    case 7:
      if result_number[0] in region_code_first_number:
        print('8495', result_number, sep = '')
    case 11:
      if (
          result_number[0] in country_code 
          and result_number[1] in region_code_first_number
         ):
        print('8', result_number[1:], sep = '')

  return

def connection_successful(recall, url):
  if recall != 200:
    print('Failure to connect to: ', url, '. \nError code: ', recall, sep = '')
    return False
  else:
    return True

def parse_one(url):
  page = requests.get(url)

  if not connection_successful(page.status_code, url): return

  is_found = False
  phones_found = set(re.findall(r'[\+7|8]?[\- ]?[\(]?[\d]{3}[\)]?[\- ]?[\d\- ]{7,10}', page.text))

  print("\tNumbers found in ", url, ':', sep = '')
  for phone in phones_found:
    if_phone(phone)
    is_found = True

  if not is_found:
    print("\tNo numbers was found in ", url, ".", sep = '')
  
  print("\tProcess was finished succesfully!")
  return

def parse_url(url: list):
  for item in url:
    parse_one(item)

#TEST_URLS = ['https://hands.ru/company/about', 'https://repetitors.info']

#parse_url(TEST_URLS) 