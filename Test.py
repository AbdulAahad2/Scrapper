from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

def scrape_iot_companies():
    url = "https://www.iotone.com/supplier"  # Corrected URL
    
    # Set up Selenium WebDriver
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    # Wait for page content to load
    wait = WebDriverWait(driver, 20)
    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".company-list-item")))  # Adjusted selector
    except:
        print("Timeout: Could not find company elements.")
        driver.quit()
        return
    
    companies = []
    
    # Scroll down to load more companies
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # Locate company elements
    company_elements = driver.find_elements(By.CSS_SELECTOR, ".company-list-item")
    
    for company in company_elements:
        try:
            name = company.find_element(By.CSS_SELECTOR, "h3").text.strip()
        except:
            name = "N/A"
        
        try:
            website = company.find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            website = "N/A"
        
        try:
            description = company.find_element(By.CSS_SELECTOR, "p").text.strip()
        except:
            description = "N/A"
        
        companies.append([name, website, description])
    
    driver.quit()
    
    # Save to CSV
    with open("iot_companies.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name", "Website", "Description"])
        writer.writerows(companies)
    
    print(f"Data saved to iot_companies.csv. Total companies found: {len(companies)}")

scrape_iot_companies()
