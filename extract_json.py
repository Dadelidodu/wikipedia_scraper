import json
import time
from leaders_scraper import get_first_paragraph, get_leaders

def extract_json():
    leaders_per_country = get_leaders()
    with open('leaders.json', 'w') as json_file:
        json.dump(leaders_per_country, json_file)

start_time = time.time()
extract_json()
end_time = time.time()

print('leaders.json file was saved successfuly') 
print(f"Total Execution time: {end_time - start_time:.2f} seconds")