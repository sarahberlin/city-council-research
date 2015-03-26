import requests
import bs4
import csv
from csv import DictWriter

root_url = 'http://www.indy.gov'
index_url = root_url + '/eGov/Council/Councillors/Biography/Pages/home.aspx'
   
#get page urls of all the councilors
def get_page_urls():
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text)    
    page_urls = []
    for item in ([a.attrs.get('href') for a in soup.select('li a[href*at-large_]')]):
        page_urls.append(item)
    for item in ([a.attrs.get('href') for a in soup.select('li a[href*district]')]):
        page_urls.append(item)
    return page_urls


#get data from each individual councilor's page
def get_councilor_data(page_url):
    councilor_data = {}
    response = requests.get(root_url+page_url)
    soup = bs4.BeautifulSoup(response.text)
    try:
        if 'at-large' in page_url:
            councilor_data['name'] = (soup.select('title')[0].get_text().encode('utf-8').replace('\r\n', '').replace('\t', '').split(",")[0]).strip()
            councilor_data['district'] = (soup.select('title')[0].get_text().encode('utf-8').replace('\r\n', '').replace('\t', '').split(",")[1]).strip()
            councilor_data['website'] =  root_url + page_url
            councilor_data['address'] = 'City-County Building, 200 E. Washington St., Indianapolis, IN 46204'
            councilor_data['email'] = soup.select('a[href^=mailto]')[0].get_text().encode('utf-8')
            councilor_data['phone'] = soup.select('td p')[1].get_text().encode('utf-8').replace('\xc2\xa0', '').split("Phone: ")[1][:13]
        else:
            councilor_data['name'] = (soup.select('title')[0].get_text().encode('utf-8').replace('\r\n', '').replace('\t', '').split(",")[1]).strip()
            councilor_data['district'] = (soup.select('title')[0].get_text().encode('utf-8').replace('\r\n', '').replace('\t', '').split(",")[0]).strip()
            councilor_data['website'] =  root_url + page_url
            councilor_data['address'] = 'City-County Building, 200 E. Washington St., Indianapolis, IN 46204'
            councilor_data['email'] = soup.select('a[href^=mailto]')[0].get_text().encode('utf-8')
            councilor_data['phone'] = soup.select('td p')[1].get_text().encode('utf-8').replace('\xc2\xa0', '').split("Phone: ")[1][:13]
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
fieldnames = ['name','district','address','phone','website', 'email']
indy_council_file = open('indy_council.csv','wb')
csvwriter = csv.DictWriter(indy_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

indy_council_file.close()
 
with open("indy_council.csv", "r") as indy_council_csv:
     indy_council = indy_council_csv.read()

print indy_council 

