import requests
import bs4
import csv
from csv import DictWriter

root_url = 'http://www.sanjoseca.gov/council'
response = requests.get(root_url)
soup = bs4.BeautifulSoup(response.text)

names = []
districts = []
phones = []
addresses = []
websites = []
emails = []
for x in range(1,11):
    names.append(soup.select('span.Subhead2')[x].get_text().encode('utf-8').split(", ")[0])
    districts.append(soup.select('span.Subhead2')[x].get_text().encode('utf-8').split(", ")[1])
    phones.append(soup.select('tbody tr td')[x].get_text().split('\n')[1].encode('utf-8').replace('            Ph: ', ''))
    addresses.append('200 E. Santa Clara St. San Jose, CA 95113')
    websites.append('http://www.sanjoseca.gov/council')
    emails.append('district{0}@sanjoseca.gov'.format(x))

cData = {}
cData['names'] = names
cData['districts'] = districts
cData['addresses'] = addresses
cData ['websites'] = websites
cData['phones'] = phones
cData['emails'] = emails
#print cData

#creates empty list to store looped information. ultimateList will be used to make the actual csv
ultimateList = []

#loops through cData, pulls out first item, second item, etc., puts those in their own dictionary, then combines all the dictionaries in ultimateList
for x in range(0,10):
    for item in cData:
        newdict = {}
        newdict['name'] = cData['names'][x]
        newdict['district'] = cData['districts'][x]
        newdict['address'] = cData['addresses'][x]
        newdict['website'] = cData['websites'][x]
        newdict['phone'] = cData['phones'][x]
        newdict['email'] = cData['emails'][x]
    ultimateList.append(newdict)


fieldnames = ['district', 'name', 'website','address','phone','email']
san_jose_council_file = open('san_jose_council.csv','wb')
csvwriter = csv.DictWriter(san_jose_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in ultimateList:
    csvwriter.writerow(row)

san_jose_council_file.close()
 
with open("san_jose_council.csv", "r") as san_jose_council_csv:
     san_jose_council = san_jose_council_csv.read()

print san_jose_council 

