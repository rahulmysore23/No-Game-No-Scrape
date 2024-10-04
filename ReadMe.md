# General Purpose Web Scraper

This is a flexible, general-purpose web scraper built with Python and Selenium. It can be used to crawl and extract information from any website, with options to restrict crawling to specific domains.

## Features

- Customizable starting URL for any website
- Adjustable crawl depth
- Option to restrict crawling to a specific domain or crawl unrestricted
- Configurable output file
- Chrome driver path specification
- Robust error handling and retry mechanism

## Requirements

- Python 3.6+
- Selenium
- Chrome WebDriver

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/general-web-scraper.git
   cd general-web-scraper
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Download the appropriate [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) for your system and Chrome version.

## Usage

Run the main script with various options:

1. Basic usage (will restrict to the starting URL domain):
   ```
   python main.py https://example.com --chrome-driver "/path/to/chromedriver"
   ```

2. Unrestricted crawling:
   ```
   python main.py https://example.com --chrome-driver "/path/to/chromedriver" --unrestricted
   ```

3. Set custom max depth and output file:
   ```
   python main.py https://example.com --chrome-driver "/path/to/chromedriver" --max-depth 5 --output my_data.json
   ```

4. Combine options:
   ```
   python main.py https://example.com --chrome-driver "/path/to/chromedriver" --unrestricted --max-depth 4 --output unrestricted_data.json
   ```

## Command-line Arguments

- `start_url`: The URL to start scraping from (required)
- `--chrome-driver`: Path to the Chrome driver executable (required)
- `--max-depth`: Maximum depth to crawl (default: 3)
- `--unrestricted`: Disable URL prefix restriction
- `--output`: Output file name (default: scraped_data.json)

## Output

The scraper saves the extracted data in JSON format. Each entry in the JSON file contains:

- URL
- Page title
- Page content
- Links found on the page

## How It Works

This web scraper operates through the following process:

1. **Initialization**: 
   - The scraper is initialized with a starting URL, Chrome driver path, and other optional parameters like max depth and domain restriction.
   - It sets up a headless Chrome browser using Selenium WebDriver.

2. **Crawling**:
   - The scraper starts with the initial URL and adds it to a queue.
   - For each URL in the queue:
     a. It checks if the URL has been visited or if the max depth has been reached.
     b. If not, it proceeds to extract information from the page.

3. **Information Extraction**:
   - The scraper navigates to the URL using the Chrome driver.
   - It waits for the page to load (specifically for the <body> tag to be present).
   - It extracts the following information:
     - Page title
     - Page content (full text of the body)
     - All links on the page

4. **Link Processing**:
   - For each extracted link, the scraper:
     a. Converts relative URLs to absolute URLs.
     b. Checks if the URL is valid and within the allowed domain (if restriction is enabled).
     c. Adds new, unvisited URLs to the queue for future processing.

5. **Data Storage**:
   - The extracted information is stored in a dictionary, with URLs as keys.

6. **Error Handling and Retries**:
   - If a page fails to load or an error occurs during extraction, the scraper will retry a specified number of times with increasing delays.

7. **Completion**:
   - Once all URLs in the queue have been processed or the max depth has been reached, the scraper saves all extracted data to a JSON file.

The scraper uses a breadth-first search approach for crawling, which means it completely processes one depth level before moving to the next. This approach, combined with the max depth parameter, allows for controlled and systematic exploration of a website or network of websites.

## Future Enhancements

1. Multi-threading support for faster crawling
2. Additional browser support (Firefox, Safari, Edge)
3. Custom CSS selector support for targeted content extraction
4. Integration with popular databases for data storage
5. Advanced filtering options for crawled content
6. Respect for robots.txt and implementation of crawl delays
7. Support for handling JavaScript-rendered content
8. Proxy rotation for IP management during large-scale crawling
9. Exportation of data in multiple formats (CSV, XML, etc.)
10. GUI for easier configuration and real-time crawl monitoring

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Disclaimer

This web scraper is for educational and research purposes only. Always respect the website's robots.txt file and terms of service when scraping. Use responsibly and ethically.