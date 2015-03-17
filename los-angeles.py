import requests
import bs4
import csv
from csv import DictWriter


#set up
root_url = 'http://lacity.org/city-government/elected-official-offices/city-council/council-directory'
response = requests.get(root_url)
soup = bs4.BeautifulSoup(response.text)

#creating lists for each type of information, ie names list contains names of all councilors
names = []
for x in range(0,15):
	if x <= 8:
		names.append(soup.select('tbody tr')[x].get_text().encode('utf-8').replace('\n\n \n\n', '').replace('          \n\nEmailDistrict Map \n\n','new').replace(' \n\n', 'new').replace('\n','').split("new")[0][18:])
	else:
		names.append(soup.select('tbody tr')[x].get_text().encode('utf-8').replace('\n\n \n\n', '').replace('          \n\nEmailDistrict Map \n\n','new').replace(' \n\n', 'new').replace('\n','').split("new")[0][19:])	 	

districts = []
for x in range(0,15):
	if x <= 8:
		districts.append(soup.select('tbody tr')[x].get_text().encode('utf-8').replace('\n\n \n\n', '').replace('          \n\nEmailDistrict Map \n\n','new').replace(' \n\n', 'new').replace('\n','').split("new")[0][:18])
	else:
		districts.append(soup.select('tbody tr')[x].get_text().encode('utf-8').replace('\n\n \n\n', '').replace('          \n\nEmailDistrict Map \n\n','new').replace(' \n\n', 'new').replace('\n','').split("new")[0][:19])

addresses=[]
for x in range(0,15):
	if x == 3 or x == 14:
		addresses.append(soup.select('tbody tr')[x].get_text().encode('utf-8').replace('\n\n \n\n', '').replace('          \n\nEmailDistrict Map \n\n','new').replace(' \n\n', 'new').replace('\n','').replace("Los Angeles", " Los Angeles").split("new")[2])
	else:
		addresses.append(soup.select('tbody tr')[x].get_text().encode('utf-8').replace('\n\n \n\n', '').replace('          \n\nEmailDistrict Map \n\n','new').replace(' \n\n', 'new').replace('\n','').replace("Los Angeles", " Los Angeles").split("new")[1])	

websites =[]
for x in range (0, 46):
	if x < 10 and x%3 == 0:
		websites.append([a.attrs.get('href') for a in soup.select('td a[href]')][x].encode('utf-8'))
	elif x >= 13 and (x-1)%3 == 0:
		websites.append([a.attrs.get('href') for a in soup.select('td a[href]')][x].encode('utf-8'))

emails = []
for x in range (0, 46):
	if x < 11 and (x-1)%3 == 0:
		emails.append([a.attrs.get('href') for a in soup.select('td a[href]')][x].encode('utf-8'))
	elif x >= 14 and (x-2)%3 == 0:
		emails.append([a.attrs.get('href') for a in soup.select('td a[href]')][x].encode('utf-8'))

#creates dictionary cData to store each list, so that it can be looped through		

cData = {}
cData['names'] = names
cData['districts'] = districts
cData['addresses'] = addresses
cData ['websites'] = websites
cData['emails'] = emails
#print cData

#creates empty list to store looped information. ultimateList will be used to make the actual csv
ultimateList = []

#loops through cData, pulls out first item, second item, etc., puts those in their own dictionary, then combines all the dictionaries in ultimateList
for x in range(0,15):
	for item in cData:
		newdict = {}
		newdict['name'] = cData['names'][x]
		newdict['district'] = cData['districts'][x]
		newdict['address'] = cData['addresses'][x]
		newdict['website'] = cData['websites'][x]
		newdict['email'] = cData['emails'][x]
	ultimateList.append(newdict)

#creates csv
fieldnames = ['district', 'name', 'website','address','phone','email']
LA_council_file = open('LA_council.csv','wb')
csvwriter = csv.DictWriter(LA_council_file, delimiter='\t', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in ultimateList:
    csvwriter.writerow(row)

LA_council_file.close()
 
with open("LA_council.csv", "r") as LA_council_csv:
     LA_council = LA_council_csv.read()

print LA_council 
