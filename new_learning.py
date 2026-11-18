print("hello world")

#how to check the type of variable

# name = "John"
# age =  25
# price = 1500.00
# is_student = True

# print(type(name))
# print(type(age))
# print(type(price))
# print(type(is_student))
# # type conversion

# age = "25"
# print(type(age))

# age = int("25")
# print(type(age))

#  working with f strings

# name = "Jhon" 
# age = 30
# country = "Nigeria"

# print(f"My name is {name}, i am {age} years old and i am from {country}")

# name = "John"
# last_name = "Otame"
# age = 30
# country = "Nigeria"
# learning_python = True

# print(type(name))
# print(type(last_name))
# print(type(age))
# print(type(country))
# print(type(learning_python))

# student_name = "David"
# student_age = 23
# student_score = 85.5
# is_registered = True

# print(student_name)
# print(student_age)
# print(student_score)
# print(is_registered)
# print(type(student_name))
# print(type(student_age))
# print(type(student_score))
# print(type(is_registered))

# student_score = int(86.5)
# print(type(student_score))

# CHALLENGE

# name = "David James"
# age = 23
# course = "Computer Science"
# country = "Nigeria"
# level = 200
# is_registered = True

# print(f""" STUDENT PROFILE
#       Name : {name}
#       Age : {age}
#       Course : {course}
#       Country : {country}
#       Level : {level}
#       Registered : {is_registered}
#       """) 

product_name = "Laptop"
product_price = "250000"
quantity = "3"

product_price = float(product_price)
quantity = int(quantity)
total_price = product_price * quantity

print(product_price)
print(total_price)
print(f""" 
PRODUCT PURCHASE SUMMARY
Product : {product_name}
Unit Price : {product_price}
Quantity : {quantity}
Total Price : {total_price}
"""
)

print(type(quantity))
print(type(total_price))