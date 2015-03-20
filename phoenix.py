import requests
import bs4
import csv
from csv import DictWriter

root_url = 'https://www.phoenix.gov'
index_url = root_url + '/mayorcouncil'

#get page urls of all the councilors
def get_page_urls():
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text)    
    urls = []
    for x in [a.attrs.get('href') for a in soup.select('a[href^=/district]')]:
        if len(x) == 10:
            urls.append(x)
    urls = urls[0:8]
    return urls

#get data from each individual councilor's page
def get_councilor_data(page_url):
    councilor_data = {}
    response = requests.get(root_url+page_url)
    soup = bs4.BeautifulSoup(response.text)
    if page_url == '/district6':
        try:
            councilor_data['district'] = "District 6"
            councilor_data['name'] = soup.select('h3.title')[0].get_text().replace('Councilman ','').replace('Councilwoman ','')
        except:
            pass   
    else:
        try:
            councilor_data['district'] = soup.select('h3.title')[0].get_text().encode('utf-8').replace('\r\n                                    \r\n                                    \r\n                                    ', '').replace('\r\n                                    \r\n                                ', '').replace('\r\n                                        \r\n                                        \r\n                                        ','').replace('\r\n                                        \r\n                                    ','')
            councilor_data['name'] = soup.select('h3.title')[1].get_text().encode('utf-8').replace('\xe2\x80\x8b', '').replace('Councilman ','').replace('Councilwoman ','').replace('Vice Mayor ','') 
            councilor_data['address'] = "200 W. Washington St., 11th Floor Phoenix, AZ 85003"

            councilor_data['website'] = (root_url+page_url)     
            
            councilor_data['phone'] = '602-262-6011'     
            for x in range(0,7):
                councilor_data['email'] = root_url + [a.attrs.get('href') for a in soup.select('a[href*/contact-district]')][x]
        except:
            pass      
    return councilor_data 

#print (get_councilor_data())

#creates empty list to store all of the councilor dictionaries
dictList = []

#run the functions together
page_urls = get_page_urls()
for page_url in page_urls:
    dictList.append(get_councilor_data(page_url)) 

#creates csv
fieldnames = ['name','district','address','phone','website','email']
phoenix_council_file = open('phoenix_council.csv','wb')
csvwriter = csv.DictWriter(phoenix_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)
phoenix_council_file.close()
 
with open("phoenix_council.csv", "r") as phoenix_council_csv:
     phoenix_council = phoenix_council_csv.read()

print phoenix_council 
