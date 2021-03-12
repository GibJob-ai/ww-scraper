from selenium import webdriver
import PySimpleGUI as sg
import json
import os
from werkzeug.utils import secure_filename
import random

JOB_TITLE = "Job Title:"
ORGANIZATION = "Organization:"
DIVISION = "Division:"

TITLES_MAIN_TABLE = (JOB_TITLE,
          "Job Category (NOC):",
          "Job Summary:",
          "Job Responsibilities:",
          "Required Skills",
          "Application Documents Required:")
TITLES_LOWER_TABLE = (ORGANIZATION,
                      DIVISION)

BASE_DIRECTORY = os.path.expanduser('~/Documents/GibJob')
DATA_DIRECTORY = BASE_DIRECTORY + '/JobData'

def get_main_table_content_by_title(header_content:str):
    element = driver.find_element_by_xpath(f"//strong[contains(text(), '{header_content}')]/parent::td/parent::tr/td[2]/span")
    return element.text

def get_lower_table_content_by_title(header_content: str):
    element = driver.find_element_by_xpath(
        f"//strong[contains(text(), '{header_content}')]/parent::td/parent::tr/td[2]")
    return element.text

def scrape_job():
    driver.switch_to.window(window_name=driver.window_handles[-1])
    job_info = {}

    for title in TITLES_MAIN_TABLE:
        job_info[title] = get_main_table_content_by_title(title)

    for title in TITLES_LOWER_TABLE:
        job_info[title] = get_lower_table_content_by_title(title)

    return job_info

def write_to_file(job_info, file_name):
    json_object = json.dumps(job_info, indent=4)
    if not os.path.exists(DATA_DIRECTORY):
        os.makedirs(DATA_DIRECTORY)
    with open(f"{DATA_DIRECTORY}/{file_name}", 'w') as f:
        f.write(json_object)

def generate_filename(job_title):
    digits = random.randint(0,99999999)
    return secure_filename(f'{job_title}_{digits}.json')

def run_scraper_to_json():
    job_info = scrape_job()
    job_title = job_info[JOB_TITLE]
    file_name = generate_filename(job_title)
    write_to_file(job_info, file_name)

DRIVER_PATH = './chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://waterlooworks.uwaterloo.ca')



sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Button('Gib Job')]]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
event, _ = window.read()
print('You entered')
window.close()

run_scraper_to_json()

driver.close()

# TODO -- Additional inputs on job posting, wait on user input (filter questions)
# TODO -- Check for exact content value for header_content value
