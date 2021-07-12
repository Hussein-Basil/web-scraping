
import json
import requests
import xlsxwriter

workbook = xlsxwriter.Workbook("data.xlsx")
sheet = workbook.add_worksheet()

sheet.write("A1", "Name")
sheet.write("B1", "Physical Address")
sheet.write("C1", "Telephone Number")
sheet.write("D1", "Email")
sheet.write("E1", "Position")

response = requests.get("https://directory.ntschools.net/api/System/GetAllSchools")
SchoolNames = json.loads(response.content)

with open('asdaresp.json', 'w') as outfile:
    json.dump(SchoolNames, outfile, sort_keys=True, indent=4)

for counter, sc in enumerate(SchoolNames):
    print("==============================")
    school_id = sc['itSchoolCode']
    base_url = "https://directory.ntschools.net/api/System/GetSchool?itSchoolCode="
    school = requests.get(base_url + school_id)
    school = json.loads(school.content)

    print(school['name'])
    print(school['physicalAddress']['displayAddress'])
    print(school['telephoneNumber'])
    print(school['schoolManagement'][0]['email'])
    print(school['schoolManagement'][0]['position'])
    
    sheet.write(counter + 1, 0, school['name'])
    sheet.write(counter + 1, 1, school['physicalAddress']['displayAddress'])
    sheet.write(counter + 1, 2, school['telephoneNumber'])
    sheet.write(counter + 1, 3, school['schoolManagement'][0]['email'])
    sheet.write(counter + 1, 4, school['schoolManagement'][0]['position'])

    if counter > 10:
        workbook.close()
        break
