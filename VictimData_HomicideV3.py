# This is the web crawler for the victims' names and death date on https://homicide.latimes.com/
# John Wang
# This is the version 3

import requests
from bs4 import BeautifulSoup
import csv
import re

result3 = []

# Access URL
for i in range(1, 250): # You can change page number here
    url = "https://homicide.latimes.com/" + "?page=" + str(i)
    
    obj = requests.get(url)

    soup = BeautifulSoup(obj.content,'lxml')
    # soup = BeautifulSoup(html, 'html.parser') # You can try this one if statement above cannot work
    
    # Code version 1 
    # It's in html format, e.g., <div class="death-date">Dec. 21</div>
    Deathdates = soup.find_all('div',{'class':'death-date'})

    result = [] 
    result1 = [] # Date

    for Deathdate in Deathdates:
        date = Deathdate.get_text()
        if date[3] == '.':
            result1.append(date)
        else:
            date_parts = date.split()
            result1.append(date_parts[0][0:3] + "." + date_parts[1])



    # Code version 1 
    # <section id="posts">
    VictimName = soup.find_all('section',{'id':'posts'})

    # It looks like <a href="/post/fernando-fierro/">Fernando Fierro, 44</a>
    for Nameagelist in VictimName:
        Nameage = Nameagelist.find_all('a')

    result2 = [] # Name
    
    for Name in Nameage:
        href = Name.get('href')
        if href and href.startswith('/post/'): # Check if href is not None
            name = Name.get_text().split(',')[0]
            result2.append(name)


    # Code version 2, maybe I should rewrite version 1 :( 
    resultlocation = []
    resultage = []
    resultgender = []
    resultcause = []
    resultrace = []
    resultagency = []
    resultinvolved = []

    # Get each victim's URL e.p.https://homicide.latimes.com/post/charles-robert-towns/
    for Subsite in Nameage:
        if Subsite.get('href').startswith('/post/'):
            newurl = Subsite.get('href')
            suburl = "https://homicide.latimes.com" + newurl
            subobj = requests.get(suburl)
            soup1 = BeautifulSoup(subobj.content,'lxml')
            
            # Data in subpage
            Details = soup1.find_all('ul',{'class':'aspects'})
            for detail in Details:
                detailline = detail.get_text() # many data in a long string 
                # e.p.'\n122 West Garvey Ave #B\nAge: 72\nGender: Male\nCause: Unknown\nRace/Ethnicity: Asian\nAgency: LASD\n'


                # Split string e
                locationmatch = re.search(r'\n([^\n]+)\n', detailline)
                location = locationmatch.group(1)
                if location.startswith("Age"):
                    location = "Unknown" 
                

                agematch = re.search(r'Age: ([^\n]+)\n', detailline)
                if agematch:
                    age = agematch.group(1)
                else:
                    age = "Unknown"
  
                gendermatch = re.search(r'Gender: ([^\n]+)\n', detailline)
                if gendermatch:
                    gender = gendermatch.group(1)
                else:
                    gender = "Unknown"

                causematch = re.search(r'Cause: ([^\n]+)\n', detailline)
                if causematch:
                    cause = causematch.group(1)
                else:
                    cause = "Unknown"

                racematch = re.search(r'Race/Ethnicity: ([^\n]+)\n', detailline)
                if racematch:
                    race = racematch.group(1)
                else:
                    race = "Unknown"
                
                agencymatch = re.search(r'Agency: ([^\n]+)\n', detailline)
                if agencymatch:
                    agency = agencymatch.group(1)
                else:
                    agency = "Unknown"

                if "Officer-involved" in detailline:
                    involved = "Officer-involved"
                else:
                    involved = "Unknown"

                resultlocation.append(location)
                resultage.append(age)
                resultgender.append(gender)
                resultcause.append(cause)
                resultrace.append(race)
                resultagency.append(agency)
                resultinvolved.append(involved)
                
    
    

    result3.extend(list(zip(result1, result2, resultlocation, resultage, resultgender, resultcause, resultrace, resultagency, resultinvolved)))
    

    years = 2023
    last_result = None
    
    result4 = []

    # Code version 1 
    # Swtich year when last month is Jan and this month is Dec, since there is no death year on the home page
    for result in result3:
        i = 1
        if result[0][0:3] == 'Dec' and last_result and last_result[0][0:3] == 'Jan':
            years = years - i
            i = i + 1
        result4.append([result[0], str(years), result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8]])
        last_result = result

    
# Output
with open("Homicide-v3.csv", "w", encoding="UTF-8", newline='') as datacsv:
    writer = csv.writer(datacsv)
    writer.writerow(["Death Date", "Death Year", "Victim Name", "Death Location", "Victim Age", "Victim Gender", "Cause of Death", "Victim Race", "Agency", "If Officer Involved "])
    for result in result4:
        writer.writerow(result) 
