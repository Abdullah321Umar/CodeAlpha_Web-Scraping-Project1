import time
import pandas as pd
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from bs4 import BeautifulSoup
import logging

# Setup logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fifa_scraper.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def setup_driver():
    """Setup Chrome WebDriver with optimal options for FIFA site"""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    
    service = Service(r"C:/Users/Abdullah Umer/Desktop/CodeAlpha Internship/Project 1/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    
    # Execute script to hide webdriver property
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def wait_for_complete_table_load(driver, max_wait_time=30):
    """Wait for complete table loading with multiple strategies"""
    try:
        # Strategy 1: Wait for initial table structure
        WebDriverWait(driver, max_wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-cy='ranking-table'] tbody tr"))
        )
        
        # Strategy 2: Wait for multiple rows to ensure pagination/loading is complete
        WebDriverWait(driver, 15).until(
            lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "[data-cy='ranking-table'] tbody tr")) > 10
        )
        
        logging.info("Complete table structure loaded successfully")
        return True
        
    except TimeoutException:
        # Fallback: Try alternative selectors
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
            )
            logging.info("Table loaded with fallback selector")
            return True
        except TimeoutException:
            raise TimeoutException("Failed to load table with all strategies")

def scroll_and_load_all_data(driver):
    """Scroll through the page to ensure all data is loaded"""
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # Check for "Load More" button and click if present
        try:
            load_more_button = driver.find_element(By.CSS_SELECTOR, "[data-cy='load-more'], .load-more-button, button[aria-label*='more']")
            if load_more_button.is_displayed() and load_more_button.is_enabled():
                driver.execute_script("arguments[0].click();", load_more_button)
                time.sleep(3)
                logging.info("Clicked load more button")
        except:
            pass
        
        # Wait for new content to load
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            break
        last_height = new_height
    
    # Final scroll to top and back to ensure all elements are in view
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

def clean_team_name(team_text):
    """Clean team name by removing country codes and extra whitespace"""
    if not team_text:
        return ""
    
    # Remove common country code patterns (3 letter codes at end)
    cleaned = re.sub(r'[A-Z]{3}$', '', team_text).strip()
    
    # Remove multiple whitespaces
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    # Handle special cases where country code might be in middle
    cleaned = re.sub(r'\s[A-Z]{3}\s', ' ', cleaned).strip()
    
    return cleaned if cleaned else team_text

def extract_ranking_data(soup):
    """Extract ranking data from parsed HTML with multiple selector strategies"""
    data = []
    
    # Strategy 1: Try specific FIFA ranking table selector
    selectors = [
        "[data-cy='ranking-table'] tbody tr",
        "table[class*='ranking'] tbody tr",
        "table tbody tr",
        ".ranking-table tbody tr"
    ]
    
    rows = []
    for selector in selectors:
        rows = soup.select(selector)
        if rows:
            logging.info(f"Found {len(rows)} rows using selector: {selector}")
            break
    
    if not rows:
        raise NoSuchElementException("No table rows found with any selector strategy")
    
    for i, row in enumerate(rows):
        try:
            cols = row.find_all(['td', 'th'])
            if len(cols) < 3:  # Skip header or incomplete rows
                continue
                
            # Extract data with flexible column handling
            rank_text = cols[0].get_text(strip=True) if cols[0] else ""
            team_text = cols[1].get_text(strip=True) if len(cols) > 1 else ""
            points_text = cols[2].get_text(strip=True) if len(cols) > 2 else ""
            prev_points_text = cols[3].get_text(strip=True) if len(cols) > 3 else ""
            change_text = cols[4].get_text(strip=True) if len(cols) > 4 else ""
            match_window_text = cols[5].get_text(strip=True) if len(cols) > 5 else ""
            
            # Skip if essential data is missing
            if not rank_text or not team_text:
                continue
            
            # Clean and validate rank (should be numeric)
            rank_clean = re.sub(r'[^\d]', '', rank_text)
            if not rank_clean.isdigit():
                continue
            
            # Clean team name
            team_clean = clean_team_name(team_text)
            
            # Clean points (remove non-numeric except decimal point)
            points_clean = re.sub(r'[^\d.]', '', points_text) if points_text else "0"
            prev_points_clean = re.sub(r'[^\d.]', '', prev_points_text) if prev_points_text else "0"
            
            # Ensure we have valid data
            if team_clean and rank_clean:
                data.append([
                    int(rank_clean),
                    team_clean,
                    points_clean,
                    prev_points_clean,
                    change_text,
                    match_window_text
                ])
                
        except Exception as e:
            logging.warning(f"Error processing row {i+1}: {str(e)}")
            continue
    
    # Sort by rank to ensure correct order
    data.sort(key=lambda x: x[0])
    
    return data

def scrape_fifa_rankings():
    """Main scraping function with enhanced data extraction"""
    driver = None
    df = pd.DataFrame()
    
    try:
        # Setup driver
        driver = setup_driver()
        logging.info("WebDriver initialized successfully")
        
        # Navigate to FIFA rankings
        driver.get("https://www.fifa.com/fifa-world-ranking/men")
        logging.info("Navigated to FIFA rankings page")
        
        # Wait for complete table loading
        wait_for_complete_table_load(driver)
        
        # Scroll and load all data
        scroll_and_load_all_data(driver)
        logging.info("Completed scrolling and data loading")
        
        # Additional wait for any final loading
        time.sleep(3)
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Extract data
        data = extract_ranking_data(soup)
        
        if not data:
            raise ValueError("No valid data extracted")
        
        # Create DataFrame
        df = pd.DataFrame(data, columns=[
            "Rank", "Team", "Total Points", "Previous Points", "Change", "Match Window"
        ])
        
        # Data validation and cleanup
        if df.empty:
            raise ValueError("DataFrame is empty after processing")
        
        # Remove duplicates and sort by rank
        df = df.drop_duplicates(subset=['Rank']).sort_values('Rank').reset_index(drop=True)
        
        # Convert numeric columns
        df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce')
        df['Total Points'] = pd.to_numeric(df['Total Points'], errors='coerce')
        df['Previous Points'] = pd.to_numeric(df['Previous Points'], errors='coerce')
        
        # Remove rows with invalid ranks
        df = df.dropna(subset=['Rank']).reset_index(drop=True)
        
        # Save with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"FIFA_Rankings_Complete_{timestamp}.csv"
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        
        # Success logging
        logging.info(f"Successfully scraped {len(df)} teams")
        logging.info(f"Data saved to {filename}")
        logging.info(f"Rank range: {df['Rank'].min()} to {df['Rank'].max()}")
        
        print(f"✅ Scraping Completed! Data saved to {filename}")
        print(f"Successfully scraped {len(df)} teams")
        print(f"Rank range: {df['Rank'].min()} to {df['Rank'].max()}")
        print("\nTop 10 Teams:")
        print(df.head(10).to_string(index=False))
        
        if len(df) < 50:
            print(f"\n⚠️ Warning: Only {len(df)} teams scraped. FIFA has 211 member associations.")
            print("This might indicate the page structure has changed or data loading is incomplete.")
        
        return df
        
    except TimeoutException as e:
        error_msg = f"Timeout error: {str(e)}"
        logging.error(error_msg)
        print(f"❌ {error_msg}")
        
    except NoSuchElementException as e:
        error_msg = f"Element not found: {str(e)}"
        logging.error(error_msg)
        print(f"❌ {error_msg}")
        
    except WebDriverException as e:
        error_msg = f"WebDriver error: {str(e)}"
        logging.error(error_msg)
        print(f"❌ {error_msg}")
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logging.error(error_msg)
        print(f"❌ {error_msg}")
        
    finally:
        # Cleanup
        if driver:
            try:
                driver.quit()
                logging.info("WebDriver closed successfully")
            except Exception as e:
                logging.error(f"Error closing WebDriver: {str(e)}")
    
    return df

def analyze_scraped_data(df):
    """Analyze the scraped data for quality and completeness"""
    if df.empty:
        return
    
    print("\n" + "="*50)
    print("DATA ANALYSIS REPORT")
    print("="*50)
    print(f"Total teams scraped: {len(df)}")
    print(f"Rank range: {df['Rank'].min()} - {df['Rank'].max()}")
    print(f"Missing ranks in sequence: {set(range(1, int(df['Rank'].max()) + 1)) - set(df['Rank'].tolist())}")
    
    print("\nTop 10 teams with highest points:")
    top_10 = df.nlargest(10, 'Total Points')[['Rank', 'Team', 'Total Points']]
    print(top_10.to_string(index=False))
    
    print("\nData quality metrics:")
    print(f"Teams with valid points: {df['Total Points'].notna().sum()}")
    print(f"Teams with change data: {df['Change'].str.len().gt(0).sum()}")
    
if __name__ == "__main__":
    result_df = scrape_fifa_rankings()
    if not result_df.empty:
        analyze_scraped_data(result_df)











