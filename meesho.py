import time
import csv
import re
import os
import sys
import io
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Fix Unicode encoding for Windows and disable buffering for real-time output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)
else:
    # For other platforms, also disable buffering
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)

# Configuration
CSV_FILE = "meesho.csv"
OUTPUT_FILE = "meesho_output.csv"

# Helper function to print with immediate flush
def print_flush(*args, **kwargs):
    """Print with immediate flush for real-time terminal output"""
    print(*args, **kwargs)
    sys.stdout.flush()

# Ensure output directory exists
# os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_product_ids():
    """Load product IDs from CSV file"""
    product_ids = []
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if row and row[0].strip():
                    product_ids.append(row[0].strip())
        print(f"[OK] Loaded {len(product_ids)} product IDs from {CSV_FILE}")
    except Exception as e:
        print(f"[ERROR] Failed to load CSV: {str(e)}")
    return product_ids

def extract_price_rating(driver, product_id):
    """Extract price and rating from the current page"""
    try:
        # Wait for page to load
        time.sleep(12)
        
        # Try multiple selectors to find price
        price = None
        
        # Strategy 1: Exact class match
        price_selectors = [
            'h4.sc-eDvSVe.biMVPh',
            'h4[class*="biMVPh"]',
            'h4[font-size="32px"]',
            'span[font-weight="book"][color="greyBase"]',
            'h4',  # Generic h4 as last resort
        ]
        
        for selector in price_selectors:
            try:
                price_element = driver.find_element(By.CSS_SELECTOR, selector)
                price_text = price_element.text.strip()
                # Check if it contains rupee sign or numeric price
                if '₹' in price_text or any(char.isdigit() for char in price_text):
                    price = price_text if price_text else None
                    print(f"    [PRICE] Found with selector '{selector}': {price}")
                    break
            except:
                continue
        
        if not price:
            print(f"    [PRICE] Not found with any selector")
        
        # Try multiple selectors to find rating
        rating = None
        
        rating_selectors = [
            ('span.sc-idXgbr.fAnWan span.sc-eDvSVe.jkpPSq', 'text'),
            ('span.sc-idXgbr.fAnWan', 'label_attr'),
            ('span.sc-eDvSVe.laVOtN', 'text'),
            ('span.sc-idXgbr span', 'text'),
            ('span[aria-label*="rating"]', 'text'),
            ('div[aria-label*="rating"]', 'text'),
            # Try to find rating before rating count
            ('span:before + span[contains(text(), "Ratings")]', 'text'),
            ('*[text()*="★"]', 'text'),
        ]
        
        for selector, method in rating_selectors:
            try:
                rating_element = driver.find_element(By.CSS_SELECTOR, selector)
                
                if method == 'label_attr':
                    rating_text = rating_element.get_attribute('label')
                else:
                    rating_text = rating_element.text.strip()
                
                # Check if it's a valid rating (contains decimal or number)
                if rating_text and ('.' in rating_text or any(char.isdigit() for char in rating_text)):
                    # Add star symbol to rating (e.g., "3.8★")
                    rating = f"{rating_text}★"
                    print(f"    [RATING] Found with selector '{selector}': {rating}")
                    break
            except:
                continue
        
        if not rating:
            print(f"    [RATING] Not found with any selector")
            
            # Debug: Try to find rating nearby the rating count element using multiple strategies
            try:
                # Strategy 1: Find rating count element and look in parent container
                rating_count_elem = driver.find_element(By.CSS_SELECTOR, 'span[font-size="16px"][font-weight="book"][color="greyT2"]')
                parent = rating_count_elem.find_element(By.XPATH, './parent::*')
                all_text = parent.text
                
                # Look for rating pattern in nearby text (format like "4.2 Ratings")
                # Exclude "Follower" and "Product" to avoid misreading follower counts
                if 'Follower' not in all_text and 'Product' not in all_text:
                    rating_match = re.search(r'(\d+\.\d+)', all_text)
                    if rating_match:
                        found_rating = rating_match.group(1)
                        # Check if it's between 0 and 5 (likely a rating)
                        # Exclude 1.0 to avoid follower count
                        try:
                            rating_value = float(found_rating)
                            if 1 < rating_value <= 5:  # Don't accept 1.0
                                rating = f"{found_rating}★"
                                print(f"    [RATING] Found via text search: {rating}")
                        except:
                            pass
                
                # Strategy 2: Look for all spans in the parent container
                try:
                    spans_in_parent = parent.find_elements(By.TAG_NAME, 'span')
                    for span in spans_in_parent:
                        span_text = span.text.strip()
                        # Check if span text looks like a rating (e.g., "4.2", "4")
                        # EXCLUDE: follower counts, price-like numbers
                        if 'Follower' in span_text or 'Product' in span_text:
                            continue  # Skip follower/product counts
                        rating_match = re.search(r'^(\d+\.\d+|\d+)$', span_text)
                        if rating_match:
                            found_rating = rating_match.group(1)
                            try:
                                rating_value = float(found_rating)
                                # Only accept ratings between 0 and 5, and NOT 1 (to avoid follower count)
                                if 0 <= rating_value <= 5 and rating_value != 1:
                                    rating = f"{found_rating}★"
                                    print(f"    [RATING] Found via span search: {rating}")
                                    break
                            except:
                                pass
                except:
                    pass
                    
            except Exception as e:
                pass
        
        # If still no rating found, set to "NA"
        if not rating:
            rating = "NA"
        
        # Try multiple selectors to find rating count
        rating_count = None
        
        # Try CSS selectors first
        rating_count_selectors_css = [
    'span.sc-dOfePm.IwbSn.ShippingInfo__OverlineStyled-sc-frp12n-4.ebArIt',
    'span[font-size="12px"][font-weight="book"][color="greyT2"]',  # backup
]
        for selector in rating_count_selectors_css:
            try:
                rating_count_element = driver.find_element(By.CSS_SELECTOR, selector)
                rating_count_text = rating_count_element.text.strip()
                # Check if it contains "Rating" or "Follower" or looks like a count
                if 'Rating' in rating_count_text or 'Follower' in rating_count_text or rating_count_text:
                    rating_count = rating_count_text
                    print(f"    [RATING_COUNT] Found with selector '{selector}': {rating_count}")
                    break
            except:
                continue
        
        # If not found with CSS, try XPath
        if not rating_count:
            rating_count_selectors_xpath = [
                "//span[contains(text(), 'Ratings')]",
                "//span[contains(text(), 'Rating')]",
                "//span[contains(text(), 'Followers')]",
            ]
            
            for selector in rating_count_selectors_xpath:
                try:
                    rating_count_element = driver.find_element(By.XPATH, selector)
                    rating_count_text = rating_count_element.text.strip()
                    if rating_count_text:
                        rating_count = rating_count_text
                        print(f"    [RATING_COUNT] Found with XPath '{selector}': {rating_count}")
                        break
                except:
                    continue
        
        if not rating_count:
            print(f"    [RATING_COUNT] Not found with any selector")
        
        return {
            'product_id': product_id,
            'product_url': f"https://www.meesho.com/product/p/{product_id}",
            'price': price,
            'rating': rating,
            'rating_count': rating_count,
            'status': 'success' if (price or rating) else 'no_data',
            'error': None if (price or rating) else 'No data found'
        }
    except Exception as e:
        return {
            'product_id': product_id,
            'product_url': f"https://www.meesho.com/product/p/{product_id}",
            'price': None,
            'rating': None,
            'rating_count': None,
            'status': 'error',
            'error': str(e)
        }

def save_single_result(result, is_first=False):
    """Save single result to CSV (append mode)"""
    fieldnames = ['product_id', 'product_url', 'price', 'rating', 'rating_count', 'status', 'error']
    
    file_exists = os.path.exists(OUTPUT_FILE)
    
    try:
        with open(OUTPUT_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # Write header only if file is new
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(result)
    except Exception as e:
        print(f"[ERROR] Failed to save result: {str(e)}")

def save_results(results):
    """Save all results to CSV (overwrite mode)"""
    fieldnames = ['product_id', 'product_url', 'price', 'rating', 'rating_count', 'status', 'error']
    
    try:
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"[OK] Results saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"[ERROR] Failed to save results: {str(e)}")

# Load product IDs
product_ids = load_product_ids()

# Process ALL products (no limit)
# To test with just a few, uncomment the line below:
# product_ids = product_ids[:10]

# Setup browser
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")

# Launch undetected Chrome
print_flush("\n" + "=" * 70)
print_flush("🚀 MEESHO PRODUCT SCRAPER - STARTING 🚀")
print_flush("=" * 70)
print_flush(f"📦 Total products to process: {len(product_ids)}")
print_flush(f"📁 Output file: {OUTPUT_FILE}")
print_flush("=" * 70)
print_flush("\n🌐 Launching Chrome browser...")
driver = uc.Chrome(options=options)
print_flush("✅ Chrome browser launched successfully!")

results = []
successful = 0
failed = 0

try:
    for i, product_id in enumerate(product_ids, 1):
        url = f"https://www.meesho.com/product/p/{product_id}"
        
        # Show progress in terminal with emoji indicators
        print_flush("\n" + "=" * 70)
        print_flush(f"\n🔵 Processing {i} / {len(product_ids)} ({i*100//len(product_ids)}%)")
        print_flush(f"Product ID: {product_id}")
        print_flush(f"URL: {url}")
        print_flush("=" * 70)
        
        # Navigate to page
        print_flush("\n🌐 Navigating to page...")
        driver.get(url)
        
        # Wait for page to load
        print_flush("⏳ Waiting for page to load...")
        time.sleep(3)
        
        # Extract data
        print_flush("🔍 Extracting data...")
        result = extract_price_rating(driver, product_id)
        results.append(result)
        
        # Display extracted data with emojis
        print_flush("\n" + "-" * 70)
        print_flush("📊 EXTRACTED DATA:")
        print_flush(f"   💰 Price: {result['price'] or '❌ Not found'}")
        print_flush(f"   ⭐ Rating: {result['rating'] or 'NA'}")
        print_flush(f"   👥 Rating Count: {result['rating_count'] or '❌ Not found'}")
        print_flush(f"   📈 Status: {result['status']}")
        print_flush("-" * 70)
        
        # Save IMMEDIATELY after each fetch (incremental saving)
        save_single_result(result, is_first=(i == 1))
        print_flush(f"\n💾 Data saved to: {OUTPUT_FILE}")
        
        if result['status'] == 'success':
            successful += 1
            print_flush(f"✅ SUCCESS: Product {product_id}")
        else:
            failed += 1
            print_flush(f"❌ FAILED: Product {product_id} - {result.get('error', 'No data found')}")
        
        # Delay between requests
        if i < len(product_ids):
            delay = 12
            print_flush(f"\n⏳ Waiting {delay} seconds before next request...")
            time.sleep(delay)
    
    # Summary
    print_flush("\n\n" + "=" * 70)
    print_flush("🎉 MEESHO SCRAPER - COMPLETED 🎉")
    print_flush("=" * 70)
    print_flush(f"📊 Total processed: {len(results)}")
    print_flush(f"✅ Successful: {successful}")
    print_flush(f"❌ Failed: {failed}")
    if len(results) > 0:
        success_rate = (successful / len(results)) * 100
        print_flush(f"📈 Success rate: {success_rate:.1f}%")
    print_flush(f"💾 Results saved to: {OUTPUT_FILE}")
    print_flush("=" * 70)

finally:
    print_flush("\n🌐 Closing browser...")
    driver.quit()
    print_flush("✅ Done!")