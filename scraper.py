from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time
import csv  # Import the csv module

url1 = 'https://www.linkedin.com/jobs/search?keywords=Marketing%20Data%20Analyst&location=Berlin%2C%20Berlin%2C%20Germany&geoId=106967730&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=1'

s = Service("chromedriver.exe")

driver = webdriver.Chrome(service=s)
driver.get(url1)
driver.implicitly_wait(10)
y = driver.find_elements(By.CLASS_NAME, 'results-context-header__job-count')[0].text
print(y)

n = pd.to_numeric(y)

i = 2
while i <= int(2) + 1:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    i = i + 1

    try:
        send = driver.find_element(By.XPATH, "//button[@aria-label='Load more results']")
        driver.execute_script("arguments[0].click();", send)
        time.sleep(3)

    except:
        pass
        time.sleep(5)

companyname = []
titlename = []

try:
    for i in range(n):
        company = driver.find_elements(By.CLASS_NAME, 'base-search-card__subtitle')[i].text
        companyname.append(company)
        # Extract job titles from the 'h1' tag
        title = driver.find_elements(By.CLASS_NAME, 'base-search-card__title')[i].text
        titlename.append(title)

except IndexError:
    print("no")

# Create a DataFrame with company and title columns
data = {'company': companyname, 'title': titlename}
df = pd.DataFrame(data)

# Save the DataFrame to 'linkedin.csv' file
df.to_csv('linkedin.csv', index=False)  # Use index=False to exclude the index column

# Read the CSV file
df = pd.read_csv('linkedin.csv')

# Convert the DataFrame to JSON
json_data = df.to_json(orient='records')

# Save the JSON data to 'linkedin.json' file
with open('linkedin.json', 'w') as json_file:
    json_file.write(json_data)