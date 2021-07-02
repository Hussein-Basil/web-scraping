from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import csv

keywords = []

with open('example-input.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    for line in csv_reader:
        keywords.append(line[0])

output_file = open('example-output.csv', 'w')
output_writer = csv.writer(output_file)


options = Options()
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument('--log-level=3')
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
driver.maximize_window()


for keyword in keywords:
    driver.get("http://www.google.com/")

    search = driver.find_element_by_name("q")
    search.send_keys(keyword)
    search.send_keys(Keys.RETURN)
    
    result = driver.findresult = driver.find_element_by_tag_name("h3")
    output_writer.writerow([result.text])
    print(result.text)

output_file.close()