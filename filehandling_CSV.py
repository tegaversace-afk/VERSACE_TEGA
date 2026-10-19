

import csv

# 1. Use csv.writer instead of file.write, and use 'w' mode for a fresh file
with open("driver.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "deliveries", "wallet"])
    writer.writerow(["Tega", "25", "12000"])
    writer.writerow(["John", "15", "8000"])
    writer.writerow(["Mary", "30", "6000"])
    
# 2. Open with standard newline="" and iterate through the reader to print rows
with open("driver.csv", "r", newline="") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
m