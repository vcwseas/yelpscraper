from bs4 import BeautifulSoup
from urllib.request import urlopen

import random
import time

#TODO: Parsing sometimes fails inconsistently. Probably to do with the search by div and class.
#TODO: Limit requests rate
#TODO: Categories formatting has an extra comma at the end.

def parse_page(url):
    request = urlopen(url, timeout = 4)
    soup = BeautifulSoup(request, 'html.parser')
    results = soup.findAll('div', attrs = {'class':'search-result natural-search-result'})
    parsed_results = []
    for result in results:
        name = result.find('a', {'class':'biz-name'}).getText()
        img = result.find('img', {'class':"photo-box-img"})["src"]
        rating = result.find('div', {'class':"i-stars"})["title"]
        review_count = result.find('span', {'class':'review-count'}).getText().strip()
        try:
            area = result.find('span',  {"class":"neighborhood-str-list"}).getText().strip()
        except Exception:
            print("Area extraction failed.")
            area = ''
        try: 
            address = result.find('address').getText().strip()
        except Exception:
            print("Address extraction failed.")
            address = ''
        price_range = result.find("span", {"class":"business-attribute price-range"}).getText().strip()
        
        c = result.find("span",{"class":"category-str-list"})
        c = c.getText().split("\n")
        categories = []
        for thing in c:
            if thing != '' and len(thing) > 2:
                categories.append(thing.strip())
        categories = ", ".join(categories)
        parsed_results.append((name, rating, review_count, area, address, price_range, categories, img))
    return parsed_results

def format_url(page_number):
    '''
    Defaults to San Francisco.
    '''
    url = "https://www.yelp.com/search?find_desc=Dinner&find_loc=San+Francisco,+CA&start={0}".format(page_number)
    return url

if __name__ == "__main__":
    results = []
    page_number = 0

    res = parse_page(format_url(page_number))
    while len(res) > 0:
        print("Processing Page:{0}".format(page_number))
        results = results + res
        page_number += 10
        res = parse_page(format_url(page_number))
        # time.sleep(random.randint(1,2) * 0.45454)
        if page_number == 500:
            break


    print(results)
        