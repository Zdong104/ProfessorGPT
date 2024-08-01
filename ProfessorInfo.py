## This file 需要手动扒拉扒拉， 半自动的， 所以需要有UI界面才能用

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re
import time
import random



user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/93.0.961.47 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
]

def get_webdriver():
    random_user_agent = random.choice(user_agents)
    options = Options()
    options.add_argument(f"user-agent={random_user_agent}")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--log-level=3")
    options.add_argument('--ignore-certificate-errors')

    # Disable images to speed up tests
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)
    return driver




def scroll_to_element(driver, element):
    """Scroll smoothly to a specific element."""
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

def scroll_to_bottom(driver):
    """Scroll to the bottom of the webpage."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Pause a bit for the page to load

driver = get_webdriver()
driver.get('https://csrankings.org/#/index?ai&vision&mlmining&nlp&inforet&us')



# Initialize a dictionary to hold university and faculty information
university_faculty_dict = {}

try:
    # Wait for the rankings table to be visible
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'ranking')))
    
    # Scroll to the 'ranking' section specifically
    ranking_element = driver.find_element(By.ID, 'ranking')
    scroll_to_element(driver, ranking_element)
    time.sleep(2)  # Wait for dynamic content to load

    

    # Get university IDs for faculties
    university_elements = driver.find_elements(By.XPATH, '//*[@id="ranking"]/tbody/tr/td[2]/span[2]')
    universities = [element.text for element in university_elements]
    
    university_ids_elements = driver.find_elements(By.XPATH, '//*[@id="ranking"]/tbody/tr/td/div')
    
    university_ids = [element.get_attribute('id') for element in university_ids_elements if '-faculty' in element.get_attribute('id')]
    print("Number of University IDs",len(university_ids))
    print("Number of University",len(universities))
    # For each university, get the faculty information


    for university_name, university_id in zip(universities, university_ids):
        faculty_list = []
        # Get number of faculty entries
        faculty_count = len(driver.find_elements(By.XPATH, f'//*[@id="{university_id}"]/div/table/tbody/tr'))
        print("faculty_count",faculty_count)

        # Collect faculty data by iterating over each relevant row
        for i in range(1, faculty_count, 2):  # Adjust the step if necessary
            xpath = f'//*[@id="{university_id}"]/div/table/tbody/tr[{i}]/td[2]/small/a[1]'
            faculty_elements = driver.find_elements(By.XPATH, xpath)
            if faculty_elements:  # Check if the list is not empty
                faculty_element = faculty_elements[0]  # Get the first element from the list
                faculty_name = faculty_element.get_attribute("innerHTML") # Directly get the text, assuming the element is an <a> tag
                faculty_url = faculty_element.get_attribute('href')
                print(faculty_name, faculty_url)
                faculty_list.append((faculty_name, faculty_url))   
            else:
                print("No faculty element found for this XPath:", xpath)
        
        university_faculty_dict[university_name] = faculty_list

finally:
    # Close the driver
    driver.quit()

# Print all university faculty information
for university, faculty_info in university_faculty_dict.items():
    print(university)
    for info in faculty_info:
        print(f" - {info[0]}, URL: {info[1]}")



# Save the university faculty information to a JSON file as a backup
import json
# Specify the file path
file_path = 'university_faculty.json'

# Writing JSON data
with open(file_path, 'w') as json_file:
    json.dump(university_faculty_dict, json_file, indent=4)