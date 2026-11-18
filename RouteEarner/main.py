from driver import Driver
from request import Request

peter = Driver(
    "Peter",
    "08011111111",
    "Toyota Camry"
)

request1 = Request(
    "Rumuola",
    "GRA",
    5000
)

request1.driver = peter
request1.status = "Assigned"

print(request1.driver.name)
print(request1.status)