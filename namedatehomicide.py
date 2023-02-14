# This is the web crawler for the victims' names and death date on https://homicide.latimes.com/
# Please install requests, bs4 and lxml
# John Wang
import requests
from bs4 import BeautifulSoup

# Access URL
url = "https://homicide.latimes.com/"
obj = requests.get(url)

soup = BeautifulSoup(obj.content,'lxml')
# soup = BeautifulSoup(html, 'html.parser') # You can try this one if statement above cannot work


# It's in html format, e.g., <div class="death-date">Dec. 21</div>
Deathdates = soup.find_all('div',{'class':'death-date'})

result1 = []

for Deathdate in Deathdates:
    # print(Deathdate.get_text())
    date = Deathdate.get_text()
    result1.append(date)


# <section id="posts">
VictimName = soup.find_all('section',{'id':'posts'})

# It looks like <a href="/post/fernando-fierro/">Fernando Fierro, 44</a>
for Nameagelist in VictimName:
    Nameage = Nameagelist.find_all('a')

result2 = []
for Name in Nameage:
    if Name.get('href').startswith('/post/'): # URL start with /post/*
        # print(Name.get_text().split(',')[0]) # Separate Fernando Fierro and 44
        name = Name.get_text().split(',')[0]
        result2.append(name)

# Output
result3 = list(zip(result1, result2))

# Death date & Victim Name        
for result in result3:
    print(result[0], result[1])