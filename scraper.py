from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Function to scrape LinkedIn job listings


def scrape_linkedin_jobs(url, num_jobs_to_scrape):
    s = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    driver.get(url)
    driver.implicitly_wait(10)

    def click_see_more_jobs():
        try:
            see_more_button = driver.find_element(
                By.XPATH, "//button[@aria-label='See more jobs']")
            if see_more_button.is_displayed():
                see_more_button.click()
                time.sleep(3)
        except Exception as e:
            print(f"Error clicking 'See more jobs' button: {str(e)}")

    job_data = {
        'id': [],
        'title': [],
        'company': [],
        'location': [],
        'link': [],
        'image_url': [],
    }

    while len(job_data['id']) < num_jobs_to_scrape:
        click_see_more_jobs()

        job_ids = driver.find_elements(By.CLASS_NAME, 'base-card')
        for i, job in enumerate(job_ids):
            if len(job_data['id']) >= num_jobs_to_scrape:
                break

            company = job.find_element(
                By.CLASS_NAME, 'base-search-card__subtitle').text

            job_data['id'].append(len(job_data['id']) + 1)
            title = job.find_element(
                By.CLASS_NAME, 'base-search-card__title').text
            location = job.find_element(
                By.CLASS_NAME, 'job-search-card__location').text
            job_link = job.find_element(
                By.CLASS_NAME, 'base-card__full-link').get_attribute('href')

            search_entity_media = job.find_element(
                By.CLASS_NAME, 'search-entity-media')
            img_element = search_entity_media.find_element(By.TAG_NAME, 'img')
            img_url = img_element.get_attribute('data-delayed-url')

            job_data['company'].append(company)
            job_data['title'].append(title)
            job_data['link'].append(job_link)
            job_data['image_url'].append(img_url)
            job_data['location'].append(location)

    df = pd.DataFrame(job_data)
    df.to_csv('linkedin.csv', index=False)
    df.to_json('linkedin.json', orient='records')


# Define the URL and number of job listings to scrape
url_to_scrape = 'https://www.linkedin.com/jobs/search?keywords=&location=India&locationId=&geoId=102713980&f_TPR=&f_PP=105214831%2C106164952%2C105556991%2C103671728%2C106888327&position=1&pageNum=0'
num_jobs_to_scrape = 20000

# Call the scraping function
scrape_linkedin_jobs(url_to_scrape, num_jobs_to_scrape)
