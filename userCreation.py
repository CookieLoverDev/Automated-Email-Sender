# This code generates and creates and CSV file with random people. This is done in order to check, if main code can import 
# emails from csv and send required message and file to them

from randomuser import RandomUser
import random
import csv

r = RandomUser()
employeeList = r.generate_users(10)

with open("employee.csv", "w", encoding="utf-8", newline='') as file:
    writer = csv.writer(file)
    columns = ["Name", "Email"]

    writer.writerow(columns)
    for person in employeeList:
        writer.writerow([person.get_first_name(), "example@gmail.com"])