import requests
import bs4
import csv
from csv import DictWriter

root_url = 'http://www.cityofchicago.org'
index_url = root_url + '/city/en/about/wards.html'

#get page urls of all the councilors
def get_page_urls():
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text)    
    return [a.attrs.get('href') for a in soup.select('h4 a[href]')][1:]  

#get data from each individual councilor's page


def get_councilor_data(page_url):
    councilor_data = {}
    response = requests.get(root_url + page_url)
    soup = bs4.BeautifulSoup(response.text)
    try:
        councilor_data['district'] = soup.find_all('h1')[0].get_text().encode('utf-8')
        if "Alderman" in (soup.select('h3')[2].get_text().encode('utf-8')):
            councilor_data['name'] = soup.select('h3')[2].get_text()[9:].encode('utf-8')
        else:
            councilor_data['name'] = soup.select('h3')[2].get_text().encode('utf-8')       
        if len(soup.select('tr td')[3].get_text().encode('utf-8')) < 14:
            councilor_data['phone'] = soup.select('tr td')[3].get_text().encode('utf-8')
        councilor_data['address'] = soup.select('tr td')[7].get_text().encode('utf-8').replace('\n', '')
        councilor_data['email'] = [a.attrs.get('href') for a in soup.select('td a[href]')][0].encode('utf-8').replace('mailto:','')
    except:
        pass
    councilor_data['website'] = (root_url + page_url).encode('utf-8')         
    return councilor_data 


#creates empty list to store all of the councilor dictionaries
dictList = []

#run the functions together
page_urls = get_page_urls()
for page_url in page_urls:
    dictList.append(get_councilor_data(page_url)) 

#creates csv
fieldnames = ['district', 'name', 'phone','email', 'website','address']
chi_council_file = open('chi_council.csv','wb')
csvwriter = csv.DictWriter(chi_council_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)
chi_council_file.close()
 
with open("chi_council.csv", "r") as chi_council_csv:
     chi_council = chi_council_csv.read()

print chi_council 
