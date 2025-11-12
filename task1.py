import cloudscraper
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin, urlparse
import random
from itertools import cycle

# Base URL
BASE_URL = "https://www.enfsolar.com/directory/installer/United%20States?page="
START_PAGE = 1
END_PAGE = 10
CSV_FILE = f"{START_PAGE}-{END_PAGE}.csv"
scraper = cloudscraper.create_scraper()
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edge/115.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edge/114.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edge/112.0.0.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G986B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 10; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Samsung Galaxy S9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_1 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.4 Mobile/15E148 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.0.0; Moto Z2 Play) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; Samsung Galaxy A51) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.4 Mobile/15E148 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:86.0) Gecko/20100101 Firefox/86.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Huawei P30) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/13.6 Mobile/15E148 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.0.0 Safari/537.36"
]

PROXIES = cycle([
    "http://mitato355:ProxySeller%23@46.3.124.28:50100",
    "http://mitato355:ProxySeller%23@185.250.187.36:50100",
    "http://mitato355:ProxySeller%23@185.250.187.227:50100",
    "http://mitato355:ProxySeller%23@203.21.95.217:50100",
    "http://mitato355:ProxySeller%23@5.22.207.93:50100",
    "http://mitato355:ProxySeller%23@209.200.239.182:50100",
    "http://mitato355:ProxySeller%23@45.192.135.62:50100",
    "http://mitato355:ProxySeller%23@5.22.204.201:50100",
    "http://mitato355:ProxySeller%23@103.115.171.207:50100",
    "http://mitato355:ProxySeller%23@200.234.178.192:50100",
    "http://mitato355:ProxySeller%23@91.186.214.17:50100",
    "http://mitato355:ProxySeller%23@45.10.156.175:50100",
    "http://mitato355:ProxySeller%23@217.194.153.180:50100",
    "http://mitato355:ProxySeller%23@103.112.71.60:50100",
    "http://mitato355:ProxySeller%23@194.50.224.56:50100",
    "http://mitato355:ProxySeller%23@185.250.187.156:50100",
    "http://mitato355:ProxySeller%23@185.13.225.213:50100",
    "http://e85db5af20e546ff:RNW78Fm5@res.proxy-seller.com:10000",
    "http://878d3ce0f10023e8:RNW78Fm5@res.proxy-seller.com:10000",
    "http://9648fa1458ca5c52:RNW78Fm5@res.proxy-seller.com:10000",
    "http://b6178e1c981c5875:RNW78Fm5@res.proxy-seller.com:10000",
    "http://afa14765efb0f92c:RNW78Fm5@res.proxy-seller.com:10000",
    "http://4175831ef8894abb:RNW78Fm5@res.proxy-seller.com:10000",
    "http://073cda27fa52225e:RNW78Fm5@res.proxy-seller.com:10000",
    "http://aa5fd1528227bf06:RNW78Fm5@res.proxy-seller.com:10000",
])

# Create CSV and write headers
with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Company Name', 'Website URL', 'Page Number'])

def get_domain(url):
    # Parse the URL
    parsed_url = urlparse(url)
    # Get the domain name (netloc)
    domain = parsed_url.netloc
    # Remove 'www.' if it exists
    domain = domain.replace('www.', '')
    return domain

# Navigate through all pages
for page in range(START_PAGE, END_PAGE):  # Pages 1 to 84
    print(f"Processing page {page}/84")
    url = BASE_URL + str(page)
    response = scraper.get(url)
    response.raise_for_status()
    
    # Parse page content
    soup = BeautifulSoup(response.text, 'html.parser')
    company_cards = soup.find_all('tr', class_='mkjs-el')
    
    # Process each company card
    for card in company_cards:
        try:
            # Extract profile URL
            profile_relative = card.find('a', class_='mkjs-a')['href']  if card.find('a', class_='mkjs-a') else ""
            profile_url = urljoin(BASE_URL, profile_relative)
            
            # Visit company profile to get website URL
            domain = ""
            if profile_url:
                scraper = cloudscraper.create_scraper(
                    browser={
                        'custom': random.choice(USER_AGENTS),
                        'platform': random.choice(['windows', 'macos', 'linux']),
                        'desktop': True
                    }
                )
                proxy = next(PROXIES)
                profile_response = scraper.get(
                    profile_url,
                    proxies={'http': proxy, 'https': proxy},
                    timeout=30
                )
                profile_response.raise_for_status()
                profile_soup = BeautifulSoup(profile_response.text, 'html.parser')
                name_tag = profile_soup.find(id="mkjs-company-profile")
                company_name = name_tag.get_text(strip=True) if name_tag else "N/A"
                website_button = profile_soup.find('a', class_='mkjs-a')
                if website_button and website_button.has_attr('href'):
                    website_url = website_button['href']
                    domain = get_domain(website_url)
                
                # Navigate back to results page
                # driver.back()
                time.sleep(random.choice([2, 2.3, 2.5]))
            
            # Save to CSV
            with open(CSV_FILE, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([company_name, domain, page])
                
        except Exception as e:
            print(f"Error processing company: {str(e)}")
            continue

    # Track progress
    print(f"Completed page {page}. {len(company_cards)} companies processed")

# Clean up
print("Scraping completed successfully!")
print(f"Data saved to {CSV_FILE}")