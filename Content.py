from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from concurrent.futures import ThreadPoolExecutor, as_completed # 多线程加载，加快速度
import random
import json


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


errors_log = {
    "Timeout Failures": [],
    "WebDriver Failures": []
}

def fetch_faculty_data(name, url):
    driver = get_webdriver()
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.TAG_NAME, 'body')))
        webpage_text = driver.execute_script("return document.body.innerText")
        print("Done fetching data for", name)
        return (name, url, webpage_text)
    except TimeoutException:
        print(f"Timeout while fetching data for {name} at {url}")
        errors_log["Timeout Failures"].append({'Name': name, 'URL': url})
        return (name, url, "Timeout Error")
    except WebDriverException as e:
        print(f"WebDriverException for {name} at {url}: {str(e)}")
        # Log this failure
        errors_log["WebDriver Failures"].append({'Name': name, 'URL': url, 'Error': str(e)})
        return (name, url, "WebDriver Error")
    finally:
        driver.quit()

# At the end of your script or in a finally block where you close other resources
def save_errors_log():
    if errors_log:  # Check if there are any failures to log
        with open('errors_log.json', 'w') as f:
            json.dump(errors_log, f, indent=4)
        print("Errors log saved to 'errors_log.json'")



def save_data(data, file_path='university_faculty_finished.json'):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def load_data(file_path='university_faculty_finished.json'):
    try:
        with open(file_path, 'r') as file:
            print(f"Got file:{file_path}")
            return json.load(file)
    except FileNotFoundError:
        return {}  # Return an empty dictionary if no file exists

# Load existing data if available
university_faculty_dict = load_data()

# # Dummy data for demonstration
# university_faculty_dict = {
#     'Carnegie Mellon University': [[
#             "Graham Neubig",
#             "http://www.phontron.com/"
#         ],
#         [
#             "Lei Li 0005",
#             "https://lileicc.github.io/"
#         ],
#         [
#             "Maarten Sap",
#             "https://maartensap.com/"
#         ],
#         [
#             "Louis-Philippe Morency",
#             "https://www.cs.cmu.edu/~morency"
#         ]],
#     "University of Michigan": [
#         [
#             "Lu Wang 0008",
#             "https://web.eecs.umich.edu/~wangluxy"
#         ],
#         [
#             "Rada Mihalcea",
#             "https://web.eecs.umich.edu/~mihalcea"
#         ],
#         [
#             "David Jurgens",
#             "https://www.si.umich.edu/node/15080"
#         ],
#         [
#             "Joyce Y. Chai",
#             "https://web.eecs.umich.edu/~chaijy"
#         ],
#         [
#             "Eytan Adar",
#             "http://www.cond.org/"
#         ],
#         [
#             "Danai Koutra",
#             "http://web.eecs.umich.edu/~dkoutra"
#         ]],
#         "New York University": [
#         [
#             "Kyunghyun Cho",
#             "http://www.kyunghyuncho.me/"
#         ],
#         [
#             "Samuel R. Bowman",
#             "https://www.nyu.edu/projects/bowman"
#         ],
#         [
#             "He He 0001",
#             "https://hhexiy.github.io/"
#         ],
#         [
#             "Tal Linzen",
#             "https://tallinzen.net/"
#         ],
#         [
#             "Ralph Grishman",
#             "http://cs.nyu.edu/grishman"
#         ]]    
# }


total_professors = sum(len(professors) for professors in university_faculty_dict.values())
print(f"Got {total_professors} professors in total.")

def is_data_complete(entry):
    """ Check if the data entry is complete or still needs processing """
    # Assuming the entry format is [name, url, info]
    # and that incomplete or unprocessed entries have an empty string or missing third element
    return len(entry) > 2 and entry[2] != ""


# Use ThreadPoolExecutor to run multiple instances of WebDriver in parallel 线程多开， 加快速度
print("Starting to fetch faculty data...")
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {}  # Using a dictionary to track each future and its corresponding university and index
    for university, faculty_list in university_faculty_dict.items():
        for i, entry in enumerate(faculty_list):
            if not is_data_complete(entry):
                future = executor.submit(fetch_faculty_data, entry[0], entry[1])
                futures[future] = (university, i)
    

    processed_count = 0
    for future in as_completed(futures):
        result = future.result()
        university, index = futures[future]
        university_faculty_dict[university][index] = result
        processed_count += 1
        if processed_count % 100 == 0:
            save_data(university_faculty_dict)
            print(f"Saved progress after processing {processed_count} entries.")


# Save any errors to a JSON file
print("Saving errors log...")
save_errors_log()

# Final save to ensure all changes are recorded
save_data(university_faculty_dict)
print("Data fetching complete and saved.")
