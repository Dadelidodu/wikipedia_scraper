import time
import requests
from bs4 import BeautifulSoup

# Set session

session = requests.Session()

# Setting root url and verifying if response status is 200

root_url = 'https://country-leaders.onrender.com'
endpoint = 'status'
response = session.get(root_url + '/' + endpoint)

if response.status_code == 200:
    print('Response is valid: ', response.status_code,'\n')
else:
    print('Response failed: ', response.status_code,'\n')

# Set the cookies_url and cookies variable + checking cookie_response
    
cookie_url = root_url + '/cookie'
cookie_response = session.get(cookie_url)
cookies = cookie_response.cookies

# Set the countries_url and countries variable 
    
countries_url = root_url + '/countries'
countries_response = session.get(countries_url, cookies=cookies)
countries = countries_response.json()

# Defining the get_first_paragraph function 

def get_first_paragraph(wiki_url: str, session=session):
    
    response = session.get(wiki_url)
    soup = BeautifulSoup(response.content, "html.parser")

    paragraphs = []
    for tag in soup.find_all("p"):
        paragraphs.append(tag.text)
    
        for paragraph in paragraphs:
            if len(paragraph) > 120:
                first_paragraph = paragraph.split('\n')[0]
                break
    return first_paragraph


# Defining the get_leaders function by setting leaders_per_country json with loop


def get_leaders():

    # Set leaders_per_country

    leaders_per_country = {}

    for country in countries:
        
        start_time = time.time()
        
        leaders_url = root_url + '/leaders'
        parameters = {'country': country}
        leaders_per_country_response = session.get(leaders_url, cookies=cookies, params=parameters)
        
        if leaders_per_country_response == 200:
            leaders_per_country[country] = leaders_per_country_response.json()
        
        else:
            new_cookies = session.get(cookie_url).cookies
            leaders_per_country[country] = session.get(leaders_url, cookies=new_cookies, params=parameters).json()

        for index, leader in enumerate(leaders_per_country[country]):
                
                wiki_url = leader['wikipedia_url']
                leader['first_paragraph'] = get_first_paragraph(wiki_url)
                num_of_leaders = len(leaders_per_country[country])
                
                if (index + 1) == num_of_leaders:
                    print(f'{country} is fully loaded')
                else:
                    print(f'{country}: {index + 1}/{num_of_leaders} loaded', end='\r')
                
                time.sleep(0.01)
        end_time = time.time()
        print(f"Execution time for {country}: {end_time - start_time:.2f} seconds \n")

        
    return leaders_per_country
    






    




