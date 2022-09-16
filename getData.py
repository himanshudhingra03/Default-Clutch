import requests as r
from bs4 import BeautifulSoup
import pandas as pd
import concurrent.futures
import time

output = []

def getLastPage(url):
    print(url)
    res = r.get(url)
    soup = BeautifulSoup(res.text)
    uls = soup.find_all("ul", {"class": "pagination justify-content-center"})
    li = uls[-1].findChildren("li" , recursive=False)
    link = li[-1].findChildren("a" , recursive=False)
    return link[0]['data-page']

def scrapeData(url):
    print("Getting URL: "+url)
    res = r.get(url)
    soup = BeautifulSoup(res.text)
    companies = soup.find_all("li", {"class": "provider provider-row"})
    for company in companies:
        companyRes = {}

        # get company name
        try:
            name = company.find("a", { "data-link_text": "Profile Title"})
            companyRes['Company'] = name.getText().strip()
        except:
            companyRes['Company'] = ""

        # get Website
        try:
            website = company.find("a", {"class": "website-link__item"})
            companyRes['Website'] = website['href']
        except:
            companyRes['Website'] = ""

        # get Location
        try:
            location = company.find("span", {"class": "locality"})
            companyRes['Location'] = location.getText().split(',')[0]
        except:
            companyRes['Location'] = ""

        # get Rating
        try:
            rating = company.find("span", {"class": "rating sg-rating__number"})
            companyRes['Rating'] = rating.getText().strip()
        except:
            companyRes['Rating'] = ""

        # get Review count
        try:
            review = company.find("a", {"class": "reviews-link sg-rating__reviews directory_profile"})
            companyRes['Review Count'] = review.getText().strip()
        except:
            companyRes['Review Count'] = ""

        # get Hourly Rate
        try:
            hourly = company.find("div", {"data-content": "<i>Avg. hourly rate</i>"})
            rate = hourly.findChildren("span" , recursive=False)
            companyRes['Hourly Rate'] = rate[0].getText().strip()
        except:
            companyRes['Hourly Rate'] = ""

        # get Min Project Size
        try:
            project = company.find("div", {"data-content": "<i>Min. project size</i>"})
            size = project.findChildren("span" , recursive=False)
            companyRes['Min Project Size'] = size[0].getText().strip()
        except:
            companyRes['Min Project Size'] = ""

        # get Employee size
        try:
            employee = company.find("div", {"data-content": "<i>Employees</i>"})
            count = employee.findChildren("span" , recursive=False)
            companyRes['Employee Size'] = count[0].getText().strip()
        except:
            companyRes['Employee Size'] = ""
            
        output.append(companyRes)
        



if __name__ == "__main__":

    keywords = ['web-developers', 'developers/reactjs', 'directory/mobile-application-developers']

    URL = "https://clutch.co/"
    
    t1 = time.time()

    for keyword in keywords:
        print(keyword)
         # Get last page
        lastpage = getLastPage(URL+keyword)

        # Scrape data
        urls = [URL+keyword+"?page="+str(i) for i in range(int(lastpage))]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(scrapeData,urls)

        # scrapeData(URL+keywords[0]+"?page=0")
        for result in results:
            print(result)
        df = pd.DataFrame.from_dict(output)
        df.to_excel(f'{keywords.index(keyword)}.xlsx')
        output = []

    t2 = time.time()
    print("Time Taken: "+str(t2-t1))
    
    


