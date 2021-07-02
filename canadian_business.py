from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time
import random


def get_free_proxies():
	url = "https://free-proxy-list.net"
	soup = BeautifulSoup(requests.get(url).content, 'html.parser')
	proxies = []
	for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
		tds = row.find_all("td")
		try:
			ip = tds[0].text.strip()
			port = tds[1].text.strip()
			proxies.append(str(ip) + ":" + str(port))
		except IndexError:
			continue
	return proxies


def set_proxy(driver, proxy):

   cap = webdriver.DesiredCapabilities.CHROME.copy()
   cap['proxy'] = {
       "proxyType": "MANUAL",
       "httpProxy": proxy,
       "sslProxy": proxy
   }
   driver.close()
   driver.start_session(cap)

proxies = get_free_proxies()
url = "https://www.canadaone.com/business/index.html/CanadaOne/directory/map/p/"

options = Options()
options.add_argument("--log-level=3")
driver = webdriver.Chrome(executable_path=r"C:/SeleniumDrivers/Chrome/91/chromedriver.exe", chrome_options=options)

for i in range(1,11):
	link = url + str(i)
	driver.get(link)
	while not "Canadian Business Directory" in driver.title:
		proxy = proxies.pop(0)
		set_proxy(driver, proxy)
		print(f"PROXY CHANGED TO {proxy}")
		try:
			driver.get(link)
		except:
			print("PROXY IS NOT AVAILABLE RIGHT NOW")
			continue
	try:
		items = driver.find_elements_by_class_name("list-group-item")
		print(f"length of list of items scraped (iteration {i}) is: {len(items)}")
		for item in items:
			website_link = item.find_element_by_link_text('Website').get_attribute('href')
			print(website_link)
	except AttributeError:
		print("Could not get the items")

	time.sleep(random.uniform(1,5))
