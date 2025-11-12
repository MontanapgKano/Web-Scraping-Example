from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

# Base URLs
BASE_URL = "https://www.myfootdr.com.au"
REGIONS_URL = urljoin(BASE_URL, "/our-clinics/regions")
CSV_FILE = "myfootdr_clinics.csv"

# Create CSV and write headers
with open(CSV_FILE, 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['Name of Clinic', 'Address', 'Email', 'Phone', 'Services'])

# Get all regions
driver.get(REGIONS_URL)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "featured-posts"))
)

soup = BeautifulSoup(driver.page_source, 'html.parser')
region_links = [urljoin(BASE_URL, a['href']) for a in soup.select('div.post-date a')]

# Process each region
for region_url in region_links:
    try:
        driver.get(region_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "regional-clinics"))
        )
        
        region_name = region_url.split('/')[-1].replace('-', ' ').title()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        clinic_cards = soup.find_all('a', class_='feature-button')
        
        # Process each clinic in the region
        for card in clinic_cards:
            try:
                profile_url = urljoin(BASE_URL, card['href'])
                print(f"Scraping: {profile_url}")
                
                driver.get(profile_url)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "entry-title"))
                )
                
                profile_soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                # Extract data
                name_tag = profile_soup.find('h1', class_="entry-title")
                clinic_name = name_tag.get_text(strip=True) if name_tag else "N/A"
                
                address_tag = profile_soup.find('div', class_="address")
                address = address_tag.get_text(" ", strip=True).replace("i", "").strip() if address_tag else "N/A"
                
                email = ""
                mailto_links = profile_soup.find_all('a', href=lambda href: href and 'mailto:' in href)
                if mailto_links:
                    email = mailto_links[0]['href'].replace('mailto:', '')
                
                phone_tag = profile_soup.find('a', class_="rose-o")
                phone = phone_tag['href'].replace('tel:', '') if phone_tag else "N/A"
                if len(phone) == 10 and phone.startswith('0'):
                    phone = f"({phone[:2]}) {phone[2:6]} {phone[6:]}"
                
                services_tag = profile_soup.find('div', class_="clinic-2020-services")
                service_cards = services_tag.find_all('article') if services_tag else []
                services = ", ".join([service_card.find('h3').get_text(strip=True) for service_card in service_cards])
                
                # Save to CSV
                with open(CSV_FILE, 'a', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file)
                    writer.writerow([clinic_name, address, email, phone, services])
                
                time.sleep(1)  # Polite delay
                
            except Exception as e:
                print(f"Error processing clinic {profile_url}: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Error processing region {region_url}: {str(e)}")
        continue

# Clean up
driver.quit()
print("Scraping completed successfully!")
print(f"All data saved to {CSV_FILE}")