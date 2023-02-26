# This is the web crawler for the victims' names and death date on https://homicide.latimes.com/
# John Wang
# This is the version 4

import requests
from bs4 import BeautifulSoup
import csv
import re

resultfinal = []
counter = 0

# Access URL
url = "https://homicide.latimes.com/"
obj = requests.get(url)
soup = BeautifulSoup(obj.content,'lxml')

# <section id="posts">
VictimName = soup.find_all('section',{'id':'posts'})

    # It looks like <a href="/post/fernando-fierro/">Fernando Fierro, 44</a>
for Nameagelist in VictimName:
    Nameage = Nameagelist.find('a')

if Nameage.get('href').startswith('/post/'):
    newurl = Nameage.get('href')
    suburl = "https://homicide.latimes.com" + newurl
    subobj = requests.get(suburl)
    soup1 = BeautifulSoup(subobj.content,'lxml')


CheckFormatname_age = soup1.find('h1').text.strip()

'''
# Type in the number of people you want
'''
for i in range(0,10): 
    resultdate = [""]
    resultyear = [""]
    resultname = [""]
    resultlocation = [""]
    resultage = [""]
    resultgender = [""]
    resultcause = [""]
    resultrace = [""]
    resultagency = [""]
    resultinvolved = [""]

    Name_age = soup1.find('h1').text.strip()
    if ',' in Name_age or CheckFormatname_age:

        name = Name_age.split(',')[0]
        resultname[0] = name

        # <div class="post-list-badge detail">
        Deathdates = soup1.find('div',{'class':'post-list-badge detail'})
        # <span class="death-date">Jan. 21, 2023</span>
        if Deathdates is not None:
            deathdate = Deathdates.find('span',{'class':'death-date'})
            dateyear = deathdate.get_text().split(',')
            date = dateyear[0]
            year = dateyear[1]

            if date[3] == '.':
                resultdate[0] = date
            else:
                date_parts = date.split()
                resultdate[0] = date_parts[0][0:3] + "." + date_parts[1]
                
            resultyear[0] = year
        else:
            resultdate[0] = date
            resultyear[0] = year


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

            resultlocation[0] = location
            resultage[0] = age
            resultgender[0] = gender
            resultcause[0] = cause
            resultrace[0] = race
            resultagency[0] = agency
            resultinvolved[0] = involved

            resultfinal.extend(list(zip(resultdate, resultyear, resultname, resultlocation, resultage, resultgender, resultcause, resultrace, resultagency, resultinvolved)))

    # nextpage: <div class="span5 offset2 prev">
    nextpage = soup1.find('div',{'class':'span5 offset2 prev'})
    if nextpage is not None:
        atag = nextpage.find('a')
        newurl = atag.get('href')
    else:
        '''
        # check if someone new is deleted

        '''
        if counter == 0:
            newurl = "/post/wendy-carolina-flores-de-roque/" # someone before him/her was deleted
            counter += 1
        elif counter == 1:
            newurl = "/post/oneil-uriel-reid/"
            counter += 1
        elif counter == 2:
            newurl = "/post/jack-richard-rodarte/"
            counter += 1
        elif counter == 3:
            newurl = "/post/brayon-renton-durr/"
            counter += 1
        elif counter == 4:
            newurl = "/post/homer-montes-garcia/"
            counter += 1
        elif counter == 5:
            newurl = "/post/iris-griselda-galan-rivera/"
            counter += 1
            '''
                elif counter == 6:
                newurl = "FIND THE URL OF THE VICTIM AFTER THE PERSON WHO WAS DELETED"
                counter += 1

            '''
        else:
            print("Someone after was deleted, number: " + str(i))
            break
    # noise data is filtered, actual outcome would be less than i

    print(i)
    print(counter)

    suburl = "https://homicide.latimes.com" + newurl
    subobj = requests.get(suburl)
    soup1 = BeautifulSoup(subobj.content,'lxml')
    


# Output
with open("Homicide-v4.csv", "w", encoding="UTF-8", newline='') as datacsv:
    writer = csv.writer(datacsv)
    writer.writerow(["Death Date", "Death Year", "Victim Name", "Death Location", "Victim Age", "Victim Gender", "Cause of Death", "Victim Race", "Agency", "If Officer Involved "])
    for result in resultfinal:
        writer.writerow(result) 
