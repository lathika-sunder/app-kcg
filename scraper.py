from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time


def scrape_jobs(url, num_jobs_to_scrape):
    s = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    driver.get(url)
    driver.implicitly_wait(10)

    job_data = {
        'id': [],
        'title': [],
        'link': [],
        'skills': []  # Add a new key for skills
    }

    while len(job_data['id']) < num_jobs_to_scrape:
        # Use the specific class for job titles
        job_ids = driver.find_elements(By.CLASS_NAME, 'title.ellipsis')

        for i, job in enumerate(job_ids):
            if len(job_data['id']) >= num_jobs_to_scrape:
                break

            title = job.text
            job_link = job.get_attribute('href')

            # Find the skills element and extract text
            skills_element = driver.find_element(
                By.CLASS_NAME, 'tags.has-description')
            skills = skills_element.text.split(
                '\n')  # Split skills into an array

            job_data['id'].append(len(job_data['id']) + 1)
            job_data['title'].append(title)
            job_data['link'].append(job_link)
            job_data['skills'].append(skills)

    df = pd.DataFrame(job_data)
    df.to_csv('jobs.csv', index=False)
    df.to_json('jobs.json', orient='records')


# Define the URL and number of job listings to scrape
url_to_scrape = 'https://www.naukri.com/jobs-in-india'
num_jobs_to_scrape = 5

# Call the scraping function
scrape_jobs(url_to_scrape, num_jobs_to_scrape)
