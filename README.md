# Data scraping using Python
In this Python script, we're trying to get some customer review data. This example code can be used for sraping any data from any website!
## Set up (Local)

..* Download the file
..* Extract the file in your selected folder.
..* Put the files called `scraper.py` and `chromedriver.exe` in the same folder.
> Here we used `chromedriver.exe` for chrome browser version `137.0.7151.56`. You can match your version from your [here](chrome://settings/help) and then download your chromedriver version from [here](https://googlechromelabs.github.io/chrome-for-testing/#stable). After download, extract the file and replce the `chromedriver.exe` to the new one!
..* Now open your `terminal`, for windows `Win`+`R` then type `cmd`
..* Now check if your machine has Python installed or not by type `python --version`. If you see the python version number then it's installed already! If not, then you need to install this first.
..* Install `pip` using `pip install requests` in your terminal
> If you’re using Python 3.x.x specifically and pip doesn't work, try: `pip3 install requests`
..* Now install selenium `pip3 install selenium`

## Update `scraper.py` file

..* Open this file in code editor. The bellow code represent the selectors. We basically grap data using this selector.
```python
    date   = rev.find_element(By.CSS_SELECTOR, ".junip-review-date").text.strip()
    author = rev.find_element(By.CSS_SELECTOR, ".junip-customer-name").text.strip()
    rating = rev.find_element(By.CSS_SELECTOR, ".junip-star-ratings-container")\
                    .get_attribute("aria-label").strip()
    body   = rev.find_element(By.CSS_SELECTOR, ".junip-review-body").text.strip().replace("\n"," ")

    imgs = rev.find_elements(By.CSS_SELECTOR, ".junip-review-image")
```
> More details will found in code comments