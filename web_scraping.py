import requests
from bs4 import BeautifulSoup
import pandas as pd


URL = 'https://www.indeed.co.uk/jobs?q=Data+Scientist&l=United+Kingdom&start='


def scraping(path):
    jobs=[]
    companies=[]
    location=[]
    salary=[]
    summary=[]
    
    for page in range(0, 300, 10):
        url = path+str(page)
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")
        for div in soup.findAll("div", attrs={"class":"jobsearch-SerpJobCard unifiedRow row result"}):
            for a in div.findAll(name="a",attrs={"data-tn-element":"jobTitle"}):
                jobs.append(a["title"])   
            company = soup.findAll(name="span", attrs={"class": "company"})
            for b in company:
                companies.append(b.text.strip())
            c = soup.findAll("span", attrs={"class": "location"})
            for span in c:
                location.append(span.text)
            d = soup.findAll("div",attrs={"class":"summary"})
            for div in d:
                summary.append(div.text.strip())
            try:
                salary.append(div.find("span",attrs={"class":"salary no-wrap"}).text.strip())
            except:
                salary.append("No data")
                
    df = pd.DataFrame(list(zip(jobs, companies, location, salary, summary)),
                      columns=['Position', 'Company', 'Location', 'Salary', 'Summary'])
    return df


if __name__ == '__main__':
    sample = scraping(URL)
    sample.to_csv('data\indeed_jobs.csv', encoding='utf-8')
    print(sample)