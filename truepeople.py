from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import xlsxwriter
import time
import random


PATH = "C:/SeleniumDrivers/Chrome/91/chromedriver.exe"
driver = webdriver.Chrome(executable_path=PATH)

outWorkbook = xlsxwriter.Workbook("outFile.xlsx")
outSheet = outWorkbook.add_worksheet()

outSheet.write("A1", "Name")
outSheet.write("B1", "Phone Number")


def get_proxies():
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

def change_proxy(driver, proxy):
    cap = webdriver.DesiredCapabilities.CHROME.copy()
    cap['proxy'] = {
        "proxyType": "MANUAL",
        "httpProxy": proxy,
        "sslProxy": proxy
    }
    driver.close()
    driver.start_session(cap)

proxies = get_proxies()
url = "https://www.truepeoplesearch.com"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
body = soup.find("div", class_="card-body")

for index, i in enumerate(body.find_all('a')):

    url = i["href"]
    driver.get(url)

    while not "Current & Historical" in driver.title:
        proxy = proxies.pop()
        change_proxy(driver, proxy)
        print("PROXY CHANGED")
        try:
            driver.get(url)
        except:
            continue

    name = driver.find_element_by_tag_name("h1").text
    phone = driver.find_element_by_xpath("//div[text()='Phone']//following-sibling::div").text
    print(name, phone, i["href"])

    outSheet.write(index+1, 0, name)
    outSheet.write(index+1, 1, phone)

    time.sleep(random.uniform(0,2))

    if (index+1) > 100:
        break
        outWorkbook.close()        

outWorkbook.close()
