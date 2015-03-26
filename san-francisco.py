import requests
import bs4
import csv
from csv import DictWriter

root_url = 'http://www.sfbos.org/'


#get page urls of all the councilors
def get_page_urls():
    response = requests.get(root_url)
    soup = bs4.BeautifulSoup(response.text)    
    urls = []
    for x in range(0,11):
        for ul in soup.findAll('ul', {'id': 'bos_list'}):
            a = ul.findAll('a')[x]
            urls.append(a.attrs['href'])
    return urls

#get data from each individual councilor's page
def get_councilor_data(page_url):
    councilor_data = {}
    response = requests.get(root_url+page_url)
    soup = bs4.BeautifulSoup(response.text)
    try:
        councilor_data['district'] = soup.select('div.sup_district')[0].get_text().encode('utf-8')
        councilor_data['name'] = soup.select('div.sup_name')[0].get_text().encode('utf-8')
        str = ' '
        seq = soup.select('p')[-1].get_text().encode('utf-8').replace('\n', '').split('\r')[0:3]
        councilor_data['address'] = str.join(seq)
        councilor_data['website'] = (root_url+page_url)
        councilor_data['phone'] = soup.select('p')[-1].get_text().encode('utf-8').replace('\n', '').split('\r')[3].replace(' - voice', '')[0:14]
        councilor_data['email'] = [a.attrs.get('href') for a in soup.select('a[href^=mailto]')][0].replace('mailto:','').replace('" target="_top', '')
    except:
        pass    
    return councilor_data 

#creates empty list to store all of the councilor dictionaries
dictList = []

#run the functions together
page_urls = get_page_urls()
for page_url in page_urls:
    dictList.append(get_councilor_data(page_url)) 

#creates csv
fieldnames = ['district', 'name', 'website','address','phone','email']
SF_council_file = open('SF_council.csv','wb')
csvwriter = csv.DictWriter(SF_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

SF_council_file.close()
 
with open("SF_council.csv", "r") as SF_council_csv:
     SF_council = SF_council_csv.read()

print SF_council 
