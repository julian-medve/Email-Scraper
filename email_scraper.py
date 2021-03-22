#import modules
from bs4 import BeautifulSoup
import requests
import time


def scrap_email(firstname, lastname, file_emails):

  print(firstname, lastname)

  url = "https://allpeople.com/search?ss=%s+%s&ss-e=&ss-p=&ss-i=&where=&industry-auto=&where-auto=" % (firstname, lastname)
  
  page = requests.get(url)
  
  search_list = BeautifulSoup(page.text, "html.parser")

  rev_flex = search_list.find_all("div", {"class": "rev-flex"})

  for row in rev_flex:

    # in each row we want to find table data with a name. Because in our rows, we have a few td elements, but only the first td element contains the name I'm using find("td") method
    email = row.find("i", {"class": "fa fa-envelope-square"})

    if email != None :
      
      a = row.find("a")

      href = a['href']

      index = len('https://allpeople.com/')

      edit_url = href[:index] + 'edit/' + href[index:]

      edit_page = requests.get(edit_url)

      edit_content = BeautifulSoup(edit_page.text, "html.parser")
      
      edit_email_input = edit_content.find_all(id="id_email0")

      email = edit_email_input[0]['value']

      print(email)
      
      file_emails.writelines("%s %s : %s\n" % (firstname, lastname, email))


# 
# 
# 


first_names = open("male_first_names.txt", "r").readlines()

# file_female_first_names = open("female_first_names.txt", "r")

last_names = open("last_names.txt", "r").readlines()

file_emails = open("emails.txt", "w+")


for first_name in first_names:
  for last_name in last_names:
    scrap_email(first_name.strip(), last_name.strip(), file_emails)
    time.sleep(3)


# scrap_email("James", "Miller", file_emails)


file_emails.close()

