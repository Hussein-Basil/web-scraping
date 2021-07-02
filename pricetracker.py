from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import unicodedata
from send_email import send_email

user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'

def get_product_info(url):
    PATH = 'C:/SeleniumDrivers/Chrome/91/chromedriver.exe'
    
    options = Options()
    options.add_argument('--log-level=3')
    options.add_argument(f'--user-agent={user_agent}')
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en_EN'})

    driver = webdriver.Chrome(executable_path=PATH, options=options)
    driver.get(url)    
    title = driver.find_element_by_xpath('//span[@id="productTitle"]').text.strip()
    price_str = driver.find_element_by_xpath('//span[@id="priceblock_ourprice"]').text.strip()
    print(title, price_str)
    
    try:
        driver.find_element_by_xpath("//div[@id='availability']//span[contains(@class,'a-color-success')]")[0].text.strip()
        available = True
    except:
        available = False

    try:
        price = unicodedata.normalize("NFKD", price_str)
        price = price.replace(',', '.').replace('$', '')
        price = float(price)
    except:
        return None, None, None
    return title, price, available

if __name__ == '__main__':
    url = "https://www.amazon.com/Redragon-S101-Keyboard-Ergonomic-Programmable/dp/B00NLZUM36/"
    products = [(url, 700)]
    
    products_below_limit = []
    for product_url, limit in products:
        title, price, available = get_product_info(product_url)
        if title is not None and price < limit and available:
            products_below_limit.append((url, title, price))


    if products_below_limit:
        message = "Subject: Price below limit!\n\n"
        message += "Your tracked products are below the given limit!\n\n"
        
        for url, title, price in products_below_limit:
            message += f"{title}\n"
            message += f"Price: {price}\n"
            message += f"{url}\n\n"
        
        send_email(message)