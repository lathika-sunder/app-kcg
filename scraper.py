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
    
    # Scroll down to load more job listings
    def scroll_to_load_more():
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
    
    job_data = {
        'id': [],
        'company': [],
        'title': [],
    }
    
    while len(job_data['id']) < num_jobs_to_scrape:
        scroll_to_load_more()
        
        job_ids = driver.find_elements(By.CLASS_NAME, 'base-card')
        for i, job in enumerate(job_ids):
            if len(job_data['id']) >= num_jobs_to_scrape:
                break
            
            job_data['id'].append(len(job_data['id']) + 1)
            company = job.find_element(By.CLASS_NAME, 'base-search-card__subtitle').text
            title = job.find_element(By.CLASS_NAME, 'base-search-card__title').text
            
            job_data['company'].append(company)
            job_data['title'].append(title)
            
        try:
            load_more_button = driver.find_element(By.XPATH, "//button[@aria-label='Load more results']")
            driver.execute_script("arguments[0].click();", load_more_button)
            time.sleep(3)
        except:
            break
    
    df = pd.DataFrame(job_data)
    df.to_csv('linkedin.csv', index=False)  # Save to CSV
    df.to_json('linkedin.json', orient='records')  # Save to JSON

# Define the URL and number of job listings to scrape
url_to_scrape = 'https://www.linkedin.com/jobs/search'
num_jobs_to_scrape = 2000  # Change this number to the desired number of job listings

# Call the scraping function
scrape_linkedin_jobs(url_to_scrape, num_jobs_to_scrape)
