import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ── CONFIG ───────────────────────────────────────────────────────────────
PRODUCT_URL       = "https://nolaninterior.com/products/miracle-sofa-cover-plush"
OUTPUT_CSV        = "junip_reviews.csv"
CHROMEDRIVER_PATH = r".\chromedriver.exe"
CHROME_BINARY     = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
# ─────────────────────────────────────────────────────────────────────────

# 1) Set up Chrome options
options = webdriver.ChromeOptions()
options.binary_location = CHROME_BINARY
options.add_argument("--headless=new")             # headless Chromium
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--enable-unsafe-swiftshader")
options.add_argument("--log-level=3")               # quieter logs

service = Service(CHROMEDRIVER_PATH)
driver  = webdriver.Chrome(service=service, options=options)

try:
    # ── A) LOAD PAGE & DEBUG INFO ────────────────────────────────────────
    driver.get(PRODUCT_URL)
    print("[DEBUG] Page loaded, status code unknown in headless mode")

    # give time for JS/widgets to initialize
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("[DEBUG] Scrolled to bottom to trigger lazy loads")
    time.sleep(3)

    # dump the HTML to inspect what loaded
    with open("page_source_debug.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("[DEBUG] Saved page source to page_source_debug.html")

    # ── B) WAIT FOR REVIEWS TO APPEAR ──────────────────────────────────────
    wait = WebDriverWait(driver, 20)
    # Wait for at least one review date to show up
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".junip-review-date")))
    print("[DEBUG] Found at least one .junip-review-date element")

    # ── C) CLICK "SEE MORE" UNTIL ALL REVIEWS LOAD ────────────────────────
    while True:
        try:
            see_more = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".junip-see-more"))
            )
            driver.execute_script("arguments[0].click();", see_more)
            print("[DEBUG] Clicked .junip-see-more")
            time.sleep(2)
        except:
            print("[DEBUG] No more .junip-see-more button—done loading reviews")
            break

    # ── D) SCRAPE ALL REVIEWS INCLUDING IMAGES ────────────────────────────
    items = driver.find_elements(By.CSS_SELECTOR, ".junip-review-list-item-container")
    print(f"[DEBUG] Total review items found: {len(items)}")

    rows = []
    for rev in items:
        try:
            date   = rev.find_element(By.CSS_SELECTOR, ".junip-review-date").text.strip()
            author = rev.find_element(By.CSS_SELECTOR, ".junip-customer-name").text.strip()
            rating = rev.find_element(By.CSS_SELECTOR, ".junip-star-ratings-container")\
                         .get_attribute("aria-label").strip()
            body   = rev.find_element(By.CSS_SELECTOR, ".junip-review-body").text.strip().replace("\n"," ")

            imgs = rev.find_elements(By.CSS_SELECTOR, ".junip-review-image")
            if imgs:
                urls = [img.get_attribute("src") for img in imgs if img.get_attribute("src")]
                images_str = " | ".join(urls)
            else:
                images_str = "-"

            rows.append([date, author, rating, body, images_str])
            print(f"[DEBUG] Collected review: {date} · {author}")
        except Exception as e:
            print(f"⚠️ Skipped one review due to: {e}")
            continue

    # ── E) SAVE TO CSV ─────────────────────────────────────────────────────
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Author", "Rating", "Review", "Images"])
        writer.writerows(rows)

    print(f"✅ Scraped {len(rows)} reviews → {OUTPUT_CSV}")

except Exception as e:
    print(f"❌ Exception during scraping: {e}")
    # on error, capture screenshot and HTML
    driver.save_screenshot("error_screenshot.png")
    with open("failed_page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("⚠️ Saved error_screenshot.png and failed_page_source.html")

finally:
    driver.quit()
    print("[DEBUG] Browser closed")
