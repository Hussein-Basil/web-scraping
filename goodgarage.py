from bs4 import BeautifulSoup
import requests
import re
import xlsxwriter

outWorkbook = xlsxwriter.Workbook("out.xlsx")
outSheet = outWorkbook.add_worksheet()

outSheet.write("A1", "Garage Name")
outSheet.write("B1", "Contact Name")
outSheet.write("C1", "Website Address")
outSheet.write("D1", "Email Address")
outSheet.write("E1", "Telephone")
outSheet.write("F1", "Full Address")


link = "https://www.goodgaragescheme.com/pages/garage.aspx/"

data = []

counter = 1

for i in range(1,11000):

    response = requests.get(link + str(i))

    if not response.status_code == 200:
        continue

    soup = BeautifulSoup(response.content, "html.parser")
    garage_name = soup.find("h1", class_="garagename").text
    address = soup.find("p", class_="address").text

    info = soup.find_all("div", class_="info-section")[-1]

    website = info.find('a', attrs={"target": "_blank"})
    email = info.find('a', attrs={'href': re.compile("^mailto:")})
    telephon = info.find('a', attrs={'href': re.compile("^tel:")})
    contact = info.find('li', text=re.compile("^Contact:"))
    
    print([getattr(website, "text", ""), getattr(email, "text", ""), \
        getattr(telephon, "text", ""), getattr(contact, "text", "")[9:]] \
    )

    outSheet.write(counter, 0, garage_name)
    outSheet.write(counter, 1, getattr(contact, "text", "")[9:])
    outSheet.write(counter, 2, getattr(website, "text", ""))
    outSheet.write(counter, 3, getattr(email, "text", ""))
    outSheet.write(counter, 4, getattr(telephon, "text", ""))
    outSheet.write(counter, 5, address)
    
    counter += 1
    
    if counter > 100:
        outWorkbook.close()
        break

outWorkbook.close()
