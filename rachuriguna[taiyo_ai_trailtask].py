# -*- coding: utf-8 -*-
"""RachuriGuna[Taiyo.AI-TrailTask].ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sN89RISVocyrz8a1rLi7YEc-oBuOLudB
"""

import requests
from bs4 import BeautifulSoup

URL = "https://www.gov.uk/contracts-finder/"
page = requests.get(URL)
print(page.content)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="before-you-start")

print(results)

job_elements = results.find_all("div", class_="gem-c-govspeak govuk-govspeak ")

for i in soup.find_all('a', href = True):
  if("etenders" in i['href']):
    nextpage = requests.get(i['href'])
    nextsoup = BeautifulSoup(nextpage.content, 'html.parser')
    print("next url title : ",nextsoup.find('title').string)
    print(i['href'])
    next_URL=i['href']

html_page1 = requests.get(next_URL).text
s = BeautifulSoup(html_page1,"html.parser")
print(s)

results = s.find_all("div", class_="col-12")
print(results)

date = []
company = []
link =[]

list_tags = s.find_all("li")
print(list_tags)

for i in list_tags:
  block = i.find('a')
  k = block.find_all('span')
  if(block.find('span',attrs={'class': 'eventDate'}) != None):
    st = ""
    for j in range(1,3):
      s = k[j]
      st += s.text
    date.append(st)
    c = block.text.split('\n')[5]
    c1 = c.strip("\t")
    c1 = c.split("\r")
    company.append(c1)
    s1 = "https://etendersni.gov.uk"
    s2 = block['href']
    lin = "".join([s1,s2])
    link.append(lin)

print(date)
print(company)
print(link)

new_company=[]
flat_list = [item for sublist in company for item in sublist]
for i in flat_list:
  k=i.split("\t")
  k=k[-1].split('\r')
  while '' in k:
    k.remove('')
  new_company.append(k)
new_company=[item for sublist in new_company for item in sublist]

print(date)
print(new_company)
print(link)

import csv
fields = ['Date','Title','Link']
rows=[]
for i in range(len(company)):
  rows.append([date[i], new_company[i], link[i]])
print(rows)

with open("tenders_data.csv",'w',newline = "") as output:
  writer = csv.writer(output)
  writer.writerow(fields)
  writer.writerows(rows)