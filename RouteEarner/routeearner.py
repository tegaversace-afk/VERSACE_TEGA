# from driver import Driver


# class RouteEarner:

#     def __init__(self):
#         self.drivers = []

#     def register_driver(self, name):
#         new_driver = Driver(name)
#         self.drivers.append(new_driver)
#         return new_driver

# items = [3000, 2000, 45000,1200, 5700]
# total = 0
# for item in items:
#     total += item
# print(total)

# cart_items = [5000, 3000, 7500, 2500]
# total = 0
# for item in cart_items:
#     total = total + item
# print(total)

# 

number_1 = float(input("Enter the first number  : "))
number_2 = float(input("Enter the second number : "))
operation = input("Choose an operation (+, -, *, /): ")

if operation == "+":
    result = number_1 + number_2
elif operation == "-":
    result = number_1 - number_2
elif operation == "*":
    result = number_1 * number_2
elif operation == "/":
    if number_2 != 0:
        result = number_1 / number_2
    else:
        print("Error: Division by zero is not allowed.")
        result = None
else:
    print("invalid mathematical operation")
    
if result is not None:
    print("Your calculation result is:", result)
