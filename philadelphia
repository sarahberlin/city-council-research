import requests
import bs4
import csv
from csv import DictWriter

root_url = 'http://phlcouncil.com/council-members/'
response = requests.get(root_url)
soup = bs4.BeautifulSoup(response.text)
dictList = []

def get_councilor_data():
	for x in range(0,17):
		newDict = {}
		try:
			if 4 < x < 7:
				newDict['name']=(soup.select('div.one_half')[x].get_text().encode('utf-8').replace("\xe2\x80\x99", "'").replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').replace("\xc3\xb1", "n").replace('\xc3\xa1', 'a').split('\n'))[1]
				newDict['district']=(soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n'))[2]
				str = ' '
				seq = soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n')[3], soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n')[4]
				newDict['address'] = str.join(seq)
				newDict['phone'] = soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n')[5].split(', ')[0]
				newDict['website'] = 'http://phlcouncil.com/council-members/'
			elif x < 10 and x != 3 and x != 5 and x != 6:
				newDict['name']=(soup.select('div.one_half')[x].get_text().encode('utf-8').replace("\xe2\x80\x99", "'").replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n'))[0]
				newDict['district']=(soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n'))[1]
				str = ' '
				seq = soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n')[2], soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n')[3]
				newDict['address'] = str.join(seq)
				newDict['phone'] = soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n')[4].split(', ')[0]
				newDict['website'] = 'http://phlcouncil.com/council-members/'
			elif x == 3:
				newDict['name'] = soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n', '')
				newDict['district'] = 'District 4'
				newDict['website'] = 'http://phlcouncil.com/council-members/'
			elif  16 > x >9 :
				newDict['name']=(soup.select('div.one_half')[x].get_text().encode('utf-8').replace("\xe2\x80\x99", "'").replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n'))[0]
				newDict['district']= 'At-Large'
				str = ' '
				seq = soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '').replace('\xc2\xa0', '').split('\n')[1], soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '').replace('\xc2\xa0', '').split('\n')[2]
				newDict['address'] = str.join(seq)
				newDict['phone'] = soup.select('div.one_half')[x].get_text().encode('utf-8').replace('\n\n\n', '').replace('\n\n', '\n').replace('\xc2\xa0', '').split('\n')[3].split(', ')[0]
				newDict['website'] = 'http://phlcouncil.com/council-members/'
			else:
				newDict['name'] = "Vacant"
				newDict['district']= 'At-Large'
		except:
			pass	
		dictList.append(newDict)
		print dictList

get_councilor_data()

fieldnames = ['district', 'name', 'website','address','phone']
philly_council_file = open('philly_council.csv','wb')
csvwriter = csv.DictWriter(philly_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

philly_council_file.close()
 
with open("philly_council.csv", "r") as philly_council_csv:
     philly_council = philly_council_csv.read()

print philly_council
