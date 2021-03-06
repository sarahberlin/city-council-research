import requests
import bs4
import csv
from csv import DictWriter

root_url = 'http://council.nyc.gov'
index_url = root_url + '/html/members/members.shtml'


#get page urls of all the councilors
def get_page_urls():
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text)    
    return [a.attrs.get('href') for a in soup.select('tr a[href^=/d]')]

#get data from each individual councilor's page
def get_councilor_data(page_url):
    councilor_data = {}
    response = requests.get(root_url + page_url)
    soup = bs4.BeautifulSoup(response.text)
    #district
    councilor_data['district'] = ((soup.select('title')[0].get_text()).split(" - ")[0]).encode('utf-8')
    #name
    try:
        if page_url == '/d6/html/members/home.shtml':
            councilor_data['name'] = soup.select('tr td em')[0].get_text().encode('utf-8').split(' - ')[0]
        else:    
            councilor_data['name'] = soup.select('h1')[0].get_text().encode('utf-8').replace("\n", "").replace('"', '')
    except:
        pass
    #party
    try:
        if len(soup.select('title')[0].get_text().split(" - "))==2:
            councilor_data['party'] = "Unknown"
        else:
            councilor_data['party'] = ((soup.select('title')[0].get_text()).split(" - ")[2]).encode('utf-8')
    except:
        pass  
    #phone
    try:      
        if len(soup.select('td.nav_text br')[2].get_text().split("District")[0].split("District")[0].encode('utf-8').replace("\n", "").replace("            ", "")) > 15:
                councilor_data['phone'] = ''
        else:    
            councilor_data['phone'] = soup.select('td.nav_text br')[2].get_text().split("District")[0].split("District")[0].encode('utf-8').replace("\n", "").replace("            ", "").strip()
    except:
        pass
    #email
    try:
        councilor_data['email'] = ([a.attrs.get('href') for a in soup.select('tr td a[href^=mailto]')][0]).replace('mailto:', '')
    except:
        pass              
    #website
    councilor_data['website'] = (root_url + page_url).encode('utf-8')
    #address
    str = ' '
    seq = soup.find('td', {'class': 'nav_text'}).get_text().encode('utf-8').split('\n')[1].replace('            ',''),soup.find('td', {'class': 'nav_text'}).get_text().encode('utf-8').split('\n')[2], soup.find('td', {'class': 'nav_text'}).get_text().encode('utf-8').replace('District Office Phone', '').replace('(Entrance on Hoffman Street)', '').split('\n')[3]
    councilor_data['address'] = str.join(seq).strip()
    return councilor_data 


#creates empty list to store all of the councilor dictionaries
dictList = []

#run the functions together
page_urls = get_page_urls()
for page_url in page_urls:
    dictList.append(get_councilor_data(page_url)) 

#creates csv
fieldnames = ['district', 'name', 'party','phone', 'email', 'website', 'address']
ny_council_file = open('ny_council.csv','wb')
csvwriter = csv.DictWriter(ny_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

ny_council_file.close()
 
with open("ny_council.csv", "r") as ny_council_csv:
     ny_council = ny_council_csv.read()

print ny_council
