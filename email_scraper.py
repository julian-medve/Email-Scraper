#import modules
from bs4 import BeautifulSoup
import requests
import time


def scrap_email(firstname, filename):

  file_emails = open(filename, "a")

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

      print(edit_url)

      edit_page = requests.get(edit_url)

      edit_content = BeautifulSoup(edit_page.text, "html.parser")

      name = edit_content.find_all(id="id_name")[0]["value"]

      edit_email_input = edit_content.find_all(id="id_email0")

      email = edit_email_input[0]['value']

      print(name, email)
      
      file_emails.writelines("%s : %s\n" % (name, email))

  file_emails.close()


def scrap_name(url):

  # make a get request
  page = requests.get(url)

  # check if an error occurs
  page.raise_for_status()

  # extract text - now we have all the text from the page
  soup = BeautifulSoup(page.text, "html.parser")

  # now find the table with data we want. In order to do it, we have to check the id of the table.
  tbody = soup.find_all(id="myTable")

  records = []

  # if we take a look at the output of print(tbody) we can see that we have many <td> and <tr> tag elements. First we go through all the elements in tbody to find ALL tr (table row) elements
  for elem in tbody:
    rows = elem.find_all("tr")

    # now we want to loop over rows. We can check how many rows are there and decide how many names we wish to store. I want to have many names, so I decided to loop over 300 rows.
    for row in rows[1:301]:
      # in each row we want to find table data with a name. Because in our rows, we have a few td elements, but only the first td element contains the name I'm using find("td") method
      column = row.find("td")
      # to extract only text we can use .text method, but because the names in the table are written in UPPER CASE I'm .capitalize() method.
      column_text = column.text.capitalize()

      # store all the names in records list
      records.append(column_text)

  return records


# 
# 
#


url = "https://namecensus.com/male_names.htm"
names = scrap_name(url)
# names = ["Robert", "Micheal"]
for name in names:
  scrap_email(name.strip(), "emails.txt")
  time.sleep(1)

# scrap_email("Robert", "emails.txt")
