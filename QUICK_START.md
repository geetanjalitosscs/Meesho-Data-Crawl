# ⚡ Quick Start Guide

## Get Started in 3 Steps

### Step 1: Prepare Your Input File

Create a file named `meesho.csv` in the same folder as `meesho.exe`:

```csv
code
9i11jk
9x33y0
9igumn
```

> **Note**: Put one product ID per line (first line is the header)

### Step 2: Run the Scraper

**Option A: Run the executable**
- Double-click `dist/meesho.exe`
- If Windows shows a warning, click "More info" → "Run anyway"

**Option B: Run the Python script**
```bash
python meesho.py
```

### Step 3: Get Your Results

- Results are saved in `meesho_output.csv`
- The CSV includes: Product ID, URL, Price, Rating, Rating Count

## 📊 What You'll See

```
🚀 MEESHO PRODUCT SCRAPER - STARTING 🚀
📦 Total products to process: 3
📁 Output file: meesho_output.csv

🔵 Processing 1 / 3 (33%)
Product ID: 9i11jk

🌐 Navigating to page...
🔍 Extracting data...

📊 EXTRACTED DATA:
   💰 Price: ₹879
   ⭐ Rating: NA
   👥 Rating Count: Follower
   📈 Status: success

💾 Data saved to: meesho_output.csv
✅ SUCCESS: Product 61goh0

⏳ Waiting 5 seconds before next request...
```

## 📝 Requirements

- ✅ Python 3.7+ (for script) OR meesho.exe (for executable)
- ✅ Chrome browser installed
- ✅ Input CSV file with product IDs

## 💡 Tips

- **First Time**: Windows Defender may block `.exe` - click "Run anyway"
- **Large Lists**: Processing 4000+ products takes ~9 hours
- **Interrupted?**: Data is saved after each product - just rerun to continue!
- **Real-Time Output**: Progress is shown live in terminal as products are processed
- **No Rating?**: Products without reviews show "NA" (this is normal!)

## 🎯 Example Input/Output

### Input (meesho.csv):
```csv
code
9i11jk
9x33y0
9igumn
```

### Output (meesho_output.csv):
```csv
product_id,product_url,price,rating,rating_count,status,error
61goh0,https://www.meesho.com/product/p/61goh0,₹879,NA,Follower,success,
86ux3o,https://www.meesho.com/product/p/86ux3o,₹154,3.8★,"29,131 Ratings",success,
a10lfx,https://www.meesho.com/product/p/a10lfx,₹239,4.0★,"44,814 Ratings",success,
```

---

**That's it! You're ready to scrape! 🚀**

