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
    councilor_data['district'] = ((soup.select('title')[0].get_text()).split(" - ")[0]).encode('utf-8')
    try:
        councilor_data['name'] = soup.select('h1')[0].get_text().encode('utf-8').replace("\n", "").replace('"', '')
    except:
        pass
    try:
        councilor_data['party'] = ((soup.select('title')[0].get_text()).split(" - ")[2]).encode('utf-8')
    except:
        pass  
    try:      
        councilor_data['phone'] = ((soup.select('td.nav_text br')[2].get_text()).split("District")[0]).encode('utf-8').replace("\n", "").replace("            ", "")
    except:
        pass      
    councilor_data['website'] = (root_url + page_url).encode('utf-8')
    councilor_data['address'] = "City Hall Park, New York, NY 10007"


#creates empty list to store all of the councilor dictionaries
dictList = []

#run the functions together
page_urls = get_page_urls()
for page_url in page_urls:
    dictList.append(get_councilor_data(page_url)) 

#creates csv
fieldnames = ['district', 'name', 'party', 'phone', 'website', 'address']
ny_council_file = open('ny_council.csv','wb')
csvwriter = csv.DictWriter(ny_council_file, delimiter='\t', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)
ny_council_file.close()
 
with open("ny_council.csv", "r") as ny_council_csv:
     ny_council = ny_council_csv.read()

print ny_council 













