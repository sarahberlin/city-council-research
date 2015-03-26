import requests
import bs4
import csv
from csv import DictWriter

#set up
root_url = 'http://lacity.org/city-government/elected-official-offices/city-council/council-directory'
response = requests.get(root_url)
soup = bs4.BeautifulSoup(response.text)
dictList = []

def get_councilor_data():
	for x in range(0,15):
		newDict = {}
		try:
			if x < 9:
				newDict['name'] = soup.findAll('td', {'class': 'views-field views-field-title'})[x].get_text().encode('utf-8').strip()[18:]
			else:
				newDict['name'] = soup.findAll('td', {'class': 'views-field views-field-title'})[x].get_text().encode('utf-8').strip()[19:]
			newDict['address'] = soup.findAll('td', {'class': 'views-field views-field-field-headquarters-location'})[x].get_text().encode('utf-8').replace('\n', '').replace('Los Angeles', ' Los Angeles').replace("Office", "Office ")
			newDict['email'] = [a.attrs.get('href') for a in soup.select('a[href^=mailto:]')][x].replace("mailto:", "")
			newDict['website'] = [a.attrs.get('href') for a in soup.select('a[href^=http://cd]')][x]
			newDict['phone'] = ''
			newDict['district'] = soup.findAll('td', {'class': 'views-field views-field-title'})[x].select('a')[0].get_text().encode('utf-8')
		except:
			pass
		dictList.append(newDict)
	print dictList

get_councilor_data()

#creates csv
fieldnames = ['district', 'name', 'website','address','phone','email']
LA_council_file = open('LA_council.csv','wb')
csvwriter = csv.DictWriter(LA_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

LA_council_file.close()
 
with open("LA_council.csv", "r") as LA_council_csv:
     LA_council = LA_council_csv.read()

print LA_council 
