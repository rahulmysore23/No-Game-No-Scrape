import json
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin, urlparse
from collections import deque
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
import time

class WebScraper:
    def __init__(self, start_url, chrome_driver_path, max_depth=3, max_retries=3, delay=1, restrict_domain=True):
        self.start_url = start_url
        self.max_depth = max_depth
        self.max_retries = max_retries
        self.delay = delay
        self.restrict_domain = restrict_domain
        self.visited = set()
        self.queue = deque([(start_url, 0)])
        self.data = {}
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--use-gl=angle")
        chrome_options.add_argument("--use-angle=swiftshader")
        chrome_options.add_argument("--ignore-certificate-errors")
        
        service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def extract_info(self, url):
        for attempt in range(self.max_retries):
            try:
                self.driver.get(url)
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                
                title = self.driver.title
                content = self.driver.find_element(By.TAG_NAME, "body").text
                links = [link.get_attribute('href') for link in self.driver.find_elements(By.TAG_NAME, "a") if link.get_attribute('href')]
                
                return {
                    "title": title,
                    "content": content,
                    "links": links
                }
            except (TimeoutException, WebDriverException) as e:
                if attempt == self.max_retries - 1:
                    print(f"Failed to extract info from {url} after {self.max_retries} attempts: {str(e)}")
                    return None
                time.sleep(self.delay * (attempt + 1))
    
    def is_valid_url(self, url):
        if self.restrict_domain:
            return url.startswith(self.start_url)
        else:
            try:
                result = urlparse(url)
                return all([result.scheme, result.netloc])
            except ValueError:
                return False
    
    def crawl(self):
        while self.queue:
            current_url, depth = self.queue.popleft()
            
            if current_url in self.visited or depth > self.max_depth:
                continue
            
            print(f"Processing: {current_url}")
            self.visited.add(current_url)
            
            info = self.extract_info(current_url)
            if info:
                self.data[current_url] = info
                
                for link in info['links']:
                    absolute_link = urljoin(current_url, link)
                    if self.is_valid_url(absolute_link) and absolute_link not in self.visited:
                        self.queue.append((absolute_link, depth + 1))
            
            time.sleep(self.delay)
        
        self.driver.quit()
    
    def save_data(self, filename="scraped_data.json"):
        with open(filename, "w", encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Web Scraper")
    parser.add_argument("start_url", help="The URL to start scraping from")
    parser.add_argument("--max-depth", type=int, default=3, help="Maximum depth to crawl (default: 3)")
    parser.add_argument("--unrestricted", action="store_true", help="Disable URL prefix restriction")
    parser.add_argument("--output", default="scraped_data.json", help="Output file name (default: scraped_data.json)")
    parser.add_argument("--chrome-driver", required=True, help="Path to the Chrome driver executable")

    args = parser.parse_args()

    scraper = WebScraper(args.start_url, chrome_driver_path=args.chrome_driver, max_depth=args.max_depth, restrict_domain=not args.unrestricted)
    scraper.crawl()
    scraper.save_data(args.output)

if __name__ == "__main__":
    main()