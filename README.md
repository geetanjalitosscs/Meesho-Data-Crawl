# 🛍️ Meesho Product Scraper

A powerful web scraper tool to extract product information (price, rating, and rating count) from Meesho.com for multiple products automatically.

## ✨ Features

- ✅ **Automated Scraping**: Scrapes price, rating, and rating count for all products in one run
- 🌐 **Browser Automation**: Uses undetected Chrome driver to bypass anti-bot measures
- 💾 **Incremental Saving**: Saves data after each product (no data loss if interrupted)
- 📊 **Real-Time Progress**: Live terminal output as products are processed (not buffered)
- 📁 **CSV Export**: Saves results to `meesho_output.csv`
- 🔄 **Robust Extraction**: Multiple CSS selector fallbacks with intelligent filtering
- ⚡ **Smart Rating Detection**: Filters out follower counts and other non-rating numbers
- 🎯 **Missing Data Handling**: Shows "NA" when rating is not available

## 📋 Requirements

- Python 3.7+
- Chrome browser installed
- Required Python packages (install via pip):
  ```
  pip install undetected-chromedriver selenium
  ```

## 🚀 Installation

1. Clone or download this repository
2. Install required packages:
   ```bash
   pip install undetected-chromedriver selenium
   ```

## 📝 Input File Format

Create a CSV file named `meesho.csv` with the following structure:

```csv
code
9i11jk
9x33y0
9igumn
8zx41g
```

- **Header**: `code` (required)
- **Data**: Product IDs (one per row)

## 🎯 Usage

### Method 1: Run Python Script

```bash
python meesho.py
```

### Method 2: Run Executable

1. Double-click `dist/meesho.exe`
2. Click "More info" if Windows Defender warning appears
3. Click "Run anyway"

## 📊 Output Format

Results are saved to `meesho_output.csv` with the following columns:

- `product_id`: Product identifier
- `product_url`: Full Meesho product URL
- `price`: Product price (e.g., "₹133")
- `rating`: Product rating with star (e.g., "3.8★" or "NA" if not available)
- `rating_count`: Number of ratings (e.g., "4,010 Ratings")
- `status`: Extraction status (success/no_data/error)
- `error`: Error message (if any)

### Example Output:

```csv
product_id,product_url,price,rating,rating_count,status,error
9i11jk,https://www.meesho.com/product/p/9i11jk,₹879,NA,Follower,success,
86ux3o,https://www.meesho.com/product/p/86ux3o,₹154,3.8★,"29,131 Ratings",success,
a10lfx,https://www.meesho.com/product/p/a10lfx,₹239,4.0★,"44,814 Ratings",success,
```

## 🖥️ Terminal Output

The script provides real-time feedback in the terminal:

```
🚀 MEESHO PRODUCT SCRAPER - STARTING 🚀
======================================================================
📦 Total products to process: 4141
📁 Output file: meesho_output.csv
======================================================================

🌐 Launching Chrome browser...
✅ Chrome browser launched successfully!

======================================================================
🔵 Processing 1 / 4141 (0%)
Product ID: 9i11jk
URL: https://www.meesho.com/product/p/9i11jk
======================================================================

🌐 Navigating to page...
⏳ Waiting for page to load...
🔍 Extracting data...

----------------------------------------------------------------------
📊 EXTRACTED DATA:
   💰 Price: ₹133
   ⭐ Rating: 3.8★
   👥 Rating Count: 4,010 Ratings
   📈 Status: success
----------------------------------------------------------------------

💾 Data saved to: meesho_output.csv
✅ SUCCESS: Product 9i11jk

⏳ Waiting 5 seconds before next request...
```

## ⚙️ Configuration

Edit `meesho.py` to customize settings:

```python
# File paths
CSV_FILE = "meesho.csv"              # Input CSV file
OUTPUT_FILE = "meesho_output.csv"    # Output CSV file

# Delays (in seconds)
time.sleep(3)   # Page load wait time
time.sleep(5)   # Delay between requests
```

## 🛠️ Troubleshooting

### Windows Defender Warning

If you see "Windows protected your PC" when running the `.exe`:

1. Click **"More info"**
2. Click **"Run anyway"**

This is normal for unsigned executables.

### Chrome Driver Issues

The script uses `undetected-chromedriver` which handles Chrome driver setup automatically. Make sure Chrome is installed on your system.

### Missing Data

If some products don't return data:
- The product may be out of stock or removed
- Meesho may have changed their HTML structure
- Check the `status` and `error` columns in the CSV

### No Rating Found

If rating shows "NA":
- The product genuinely has no reviews yet
- This is normal for new or unpopular products
- The script correctly filters out follower counts and other non-rating numbers

## 📁 Project Structure

```
crawl/
├── meesho.py              # Main scraper script
├── meesho.csv              # Input CSV with product IDs
├── meesho_output.csv      # Output CSV with results
├── dist/
│   └── meesho.exe         # Compiled executable
└── README.md              # This file
```

## 🔧 Building the Executable

To rebuild the `.exe` file:

```bash
pyinstaller --name=meesho --console --onefile meesho.py --noconfirm
```

## ⚠️ Important Notes

1. **Rate Limiting**: The script waits 5 seconds between requests to avoid being blocked
2. **Browser Window**: Chrome will open during scraping (visible by default)
3. **Data Safety**: Results are saved incrementally - you can stop the script anytime without losing data
4. **Large Files**: Processing 4000+ products can take several hours
5. **Real-Time Output**: Terminal shows progress as each product is processed (unbuffered output)
6. **Missing Ratings**: Products without reviews show "NA" (not an error, just no data available)

## 📈 Expected Performance

- **Processing Speed**: ~1 product every 8 seconds
- **Total Time**: ~9 hours for 4141 products
- **Success Rate**: ~90-95% (may vary based on Meesho's anti-bot measures)

## 🐛 Known Issues

- First run may need manual approval for Chrome
- Some products may not have ratings available
- Windows Defender may flag the executable (safe to run)

## 📞 Support

For issues or questions:
1. Check the `error` column in the output CSV
2. Review the terminal output for detailed status
3. Ensure Chrome and all dependencies are up to date

## 📄 License

This project is for educational and research purposes only. Use responsibly and respect Meesho's terms of service.

---

**Made with ❤️ for efficient data extraction**

