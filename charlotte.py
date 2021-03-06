import requests
import bs4
import csv
from csv import DictWriter

root_url = 'http://charmeck.org'
index_url = '/city/charlotte/CityCouncil/MeettheCouncil/Pages/home.aspx'

#get page urls of all the councilors
def get_page_urls():
    response = requests.get(root_url + index_url)
    soup = bs4.BeautifulSoup(response.text)
    return [a.attrs.get('href') for a in soup.select('p a[href^=/city/charlotte/CityCouncil/MeettheCouncil]')][1:]

#get data from each individual councilor's page
def get_councilor_data(page_url):
    councilor_data = {}
    response = requests.get(root_url+page_url)
    soup = bs4.BeautifulSoup(response.text)
    try:
        councilor_data['name'] = soup.select('div.heading')[0].get_text().encode('utf-8').replace('\r\n\t\t\t', '').replace('\t', '').split(',')[0]
        councilor_data['district'] = soup.select('div.heading')[0].get_text().encode('utf-8').replace('\r\n\t\t\t', '').replace('\t', '').split(',')[1].strip()
        councilor_data['email'] = soup.select('a[href^=mailto]')[0].get_text().encode('utf-8').replace(' \n', '')
        councilor_data['website'] = (root_url+page_url)
        councilor_data['address'] = '600 E. 4th Street Charlotte, NC 28202'
        councilor_data['phone'] ='704-336-2241'
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
charlotte_council_file = open('charlotte_council.csv','wb')
csvwriter = csv.DictWriter(charlotte_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

charlotte_council_file.close()
 
with open("charlotte_council.csv", "r") as charlotte_council_csv:
     charlotte_council = charlotte_council_csv.read()

print charlotte_council 
