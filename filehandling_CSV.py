

# import csv

# 1. Use csv.writer instead of file.write, and use 'w' mode for a fresh file
# with open("driver.csv", "w", newline="") as file:
#     writer = csv.writer(file)
#     writer.writerow(["name", "deliveries", "wallet"])
#     writer.writerow(["Tega", "25", "12000"])
#     writer.writerow(["John", "15", "8000"])
#     writer.writerow(["Mary", "30", "6000"])
    
#  2. Open with standard newline="" and iterate through the reader to print rows
# with open("drivers.csv", "r", newline="") as file:
#     reader = csv.reader(file)
#     for row in reader:
#         print(row)

# import csv

# total_wallet = 0
# qualified_count = 0

# with open("drivers.csv", "r", newline="") as file:
#     reader = csv.DictReader(file)

#     total_wallet = sum(
#     int(driver["wallet"])
#     for driver in reader
#     if int(driver["deliveries"]) >= 30
    
    
        
#     )

# qualified_drivers = [
#     driver
#     for driver in reader
#     if int(driver["deliveries"]) >= 30
# ]

# print(total_wallet)
# print(qualified_drivers)

# import csv

# total_wallet = 0
# qualified_count = 0

# with open("drivers.csv", "r", newline="") as file:
#     reader = csv.DictReader(file)

#     for driver in reader:
#         if int(driver["deliveries"]) >= 30:
#             total_wallet += int(driver["wallet"])
#             qualified_count += 1

# print(f"Qualified drivers: {qualified_count}")
# print(f"Combined wallet: ₦{total_wallet:,}")

# import csv

# with open("new_drivers.csv", "w", newline = "") as file :
#     writer = csv.writer(file)
#     writer.writerow(["name","deliveries", "wallet"])
#     writer.writerow(["David", "25", '14000'])
#     writer.writerow(["Peter", "42", "25000"])

# drivers = [
#     {"name": "David", "deliveries": "25", "wallet": "14000"},
#     {"name": "Peter", "deliveries": "42", "wallet": "25000"}
# ]

# fieldnames = ["name","deliveries", "wallet"]

# with open("new_drivers.csv", "w", newline = "") as file:
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
    
#     writer.writeheader()
#     writer.writerows(drivers)

# new_driver = {
#     "name": "David",
#     "deliveries": "0",
#     "wallet": 0
# }
# with open("drivers.csv", "a", newline = "") as file:
#     writer = csv.DictWriter(
#         file,
#         fieldnames = ["name","deliveries","wallet" ]
#     )
#     writer.writerow(new_driver)

# with open("drivers.csv", "r", newline="") as file:
#     reader = csv.DictReader(file)
#     drivers = list(reader)

#     for driver in drivers:
#         if driver["name"] == "Tega":
#             driver["wallet"] = "20000"

# with open("drivers.csv", "w", newline="") as file:
#     fieldnames = ["name", "deliveries", "wallet"]
#     writer = csv.DictWriter(file, fieldnames=fieldnames)

#     writer.writeheader()
#     writer.writerows(drivers)

# import csv

# with open("drivers.csv", "r", newline="") as file:
#     reader = csv.DictReader(file)
#     drivers = list(reader)

# for driver in drivers:
#     if driver["name"] == "Mary":
#         driver["wallet"] = 25000
# with open("drivers.csv", "w", newline="") as file:
#     fieldnames = ["name", "deliveries", "wallet"]
#     writer = csv.DictWriter(file, fieldnames=fieldnames)

#     writer.writeheader()
#     writer.writerows(drivers)

# what if marys data do not exist in the file, use this check format

# mary_found = False

# for driver in drivers:
#     if driver["name"] == "Mary":
#         driver["wallet"] = 25000
#         mary_found = True

# if mary_found:
#     # Save the updated records
#     print("Mary's wallet updated successfully.")
# else:
#     print("Mary was not found.")

# import csv

# with open("drivers.csv", "r", newline="") as file:
#     reader = csv.DictReader(file)
#     drivers = list(reader)

#     invalid_drivers_count= 0
#     valid_drivers = []
#     invalid_drivers = []

#     for driver in drivers:
#         try:
#             deliveries = int(driver["deliveries"])

#             if deliveries < 0:
#                 print(f"invalid driver :{driver['name']}")
#                 invalid_drivers.append(driver)
#                 invalid_drivers_count += 1
#             else:
#                 valid_drivers.append(driver)
            
#         except ValueError:
#             print(f"Invalid Driver : {driver['name']}")
#             invalid_drivers.append(driver)
#             invalid_drivers_count += 1
# print(f"Total invalid drivers: {invalid_drivers_count}")

# with open("valid_drivers.csv", "w", newline="") as file:
#     writer = csv.DictWriter(file, fieldnames=headers)
#     writer.writeheader()
#     writer.writerows(valid_drivers)

# with open("invalid_drivers.csv", "w", newline="") as file:
#     writer = csv.DictWriter(file, fieldnames=headers)
#     writer.writeheader()
#     writer.writerows(invalid_drivers)


# # STEP 4: Display summary
# print(f"Valid drivers: {len(valid_drivers)}")
# print(f"Invalid drivers: {len(invalid_drivers)}")



import csv

valid_drivers = []
invalid_drivers = []

headers = ["name", "deliveries", "wallet"]

# STEP 1: Read the original CSV
with open("drivers.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    for driver in reader:
        try:
            deliveries = int(driver["deliveries"])

            if deliveries < 0:
                invalid_drivers.append(driver)
            else:
                valid_drivers.append(driver)

        except ValueError:
            invalid_drivers.append(driver)


# STEP 2: Save valid drivers
with open("valid_drivers.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(valid_drivers)


# STEP 3: Save invalid drivers
with open("invalid_drivers.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(invalid_drivers)


# STEP 4: Display summary
print(f"Valid drivers: {len(valid_drivers)}")
print(f"Invalid drivers: {len(invalid_drivers)}")