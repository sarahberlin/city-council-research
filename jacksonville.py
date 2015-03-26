import requests
import bs4
import csv
from csv import DictWriter

root_url = 'http://www.coj.net/city-council/city-council-members.aspx'
response = requests.get(root_url)
soup = bs4.BeautifulSoup(response.text)
dictList = []

def get_councilor_data1():
    for x in range (0,30):
        newDict = {}
        if x >1 and x%2 == 0:
            newDict['district'] = soup.select('tr td')[x].get_text().encode('utf-8').replace('\n\r\n         ', '').replace('\n', '').replace('\r', '').split(': ')[0]
            newDict['name'] = soup.select('tr td')[x].get_text().encode('utf-8').replace('\n\r\n         ', '').replace('\n', '').replace('\r', '').split(': ')[1]
            newDict['phone'] = soup.select('tr td')[x+1].get_text().encode('utf-8').replace('\n\r\n         ', '').replace('\n', '').replace('\r', '').replace('Phone: ', '').replace('Email: ', '').split('         ')[0]
            newDict['email'] = soup.select('tr td')[x+1].get_text().encode('utf-8').replace('\n\r\n         ', '').replace('\n', '').replace('\r', '').replace('\xc2\xa0', '').replace('Phone: ', '').replace('Email:', '').split('         ')[1]
            newDict['address'] = '117 West Duval St., Suite 425 Jacksonville, FL 32202'
            newDict['website'] = 'http://www.coj.net/city-council/city-council-members.aspx'
            dictList.append(newDict)
            print dictList

def get_councilor_data2():
    for x in range(14,19):
        newDict = {}
        newDict['district'] = "At-Large " + soup.select('td h2')[x].get_text().encode('utf-8').replace('\r\n         ', '').split(":")[0]
        newDict['name'] = soup.select('td h2')[x].get_text().encode('utf-8').replace('\r\n         ', '').split(":")[1].strip()
        newDict['address'] = '117 West Duval St., Suite 425 Jacksonville, FL 32202'
        newDict['website'] = 'http://www.coj.net/city-council/city-council-members.aspx'
        newDict['phone'] = '(904) 630-1377'
        newDict['email'] = ''
        dictList.append(newDict)
        print dictList

get_councilor_data1()
get_councilor_data2() 

fieldnames = ['district', 'name', 'website','address','phone', 'email']
jacksonville_council_file = open('jacksonville_council.csv','wb')
csvwriter = csv.DictWriter(jacksonville_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

jacksonville_council_file.close()
 
with open("jacksonville_council.csv", "r") as jacksonville_council_csv:
     jacksonville_council = jacksonville_council_csv.read()

print jacksonville_council
