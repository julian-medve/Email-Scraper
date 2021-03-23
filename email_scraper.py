#import modules
from bs4 import BeautifulSoup
import requests
import time


def scrap_email(firstname, file_emails):

  print(firstname)

  url = "https://allpeople.com/search?ss=%s&ss-e=&ss-p=&ss-i=&where=&industry-auto=&where-auto=" % (firstname)
  
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

      name = edit_content.find_all(id="id_name")[0]["value"]

      edit_email_input = edit_content.find_all(id="id_email0")

      email = edit_email_input[0]['value']

      print(name, email)
      
      file_emails.writelines("%s : %s\n" % (name, email))


# 
# 
# 


first_names = open("male_first_names.txt", "r").readlines()

# file_female_first_names = open("female_first_names.txt", "r")

file_emails = open("emails.txt", "w+")


for first_name in first_names:
    scrap_email(first_name.strip(), file_emails)
    time.sleep(1.25)


# scrap_email("James", file_emails)

file_emails.close()