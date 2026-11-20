from routeearner import RouteEarner

# Create the RouteEarner platform
app = RouteEarner()

# Register a driver
peter = app.register_driver(
    "Peter",
    "08011111111",
    "Toyota Camry"
)

# Check Peter's initial availability
print("Peter available:", peter.available)

# Bring Peter online
peter.go_online()
print("Peter available:", peter.available)

# Take Peter offline
peter.go_offline()
print("Peter available:", peter.available)
john = app.register_driver(
    "John",
    "08022222222",
    "Honda Accord"
)

mary = app.register_driver(
    "Mary",
    "08033333333",
    "Toyota Corolla"
)

# Display driver information
print("Driver:", peter.name)
print("Phone:", peter.phone)
print("Vehicle:", peter.vehicle)



# Check registered drivers
print("Total drivers:", len(app.drivers))

# Create a customer delivery request
request1 = app.create_request(
    "Rumuola",
    "GRA",
    5000
)

request2 = app.create_request(
    "Rumuola",
    "Trans Amadi",
    5000,
    "card",
    0.20
)

print("Payment method:", request2.payment_method)
print("Discount rate:", request2.discount_rate)

# Bring Peter online
peter.go_online()

# Assign Peter to the request
app.assign_driver(request1, peter)

# Display assignment information
print("Assigned driver:", request1.driver.name)
print("Request status:", request1.status)
print("Peter available:", peter.available)
# Complete the delivery
request1.complete()

# Display delivery results
print("\n--- DELIVERY RESULTS ---")

print("Request status:", request1.status)
print("Customer paid:", request1.customer_paid)
print("Service fee:", request1.service_fee)
print("Driver wallet:", peter.wallet_balance)
print("Driver deliveries:", peter.deliveries)
print("Peter online:", peter.online)
print("Peter available:", peter.available)

# Bring John online
john.go_online()

# Assign John to the second request
app.assign_driver(request2, john)

# Complete the second delivery
request2.complete()

print("\n--- CARD PAYMENT RESULTS ---")

print("Request status:", request2.status)
print("Customer paid:", request2.customer_paid)
print("Service fee:", request2.service_fee)
print("Driver wallet change:", request2.wallet_change)
print("John's wallet:", john.wallet_balance)
print("John's deliveries:", john.deliveries)

# --- TEST DRIVER GOING OFFLINE ---

# Create another delivery request
request3 = app.create_request(
    "GRA",
    "Mile 1",
    3000,
    "cash"
)

# John comes online
john.go_online()

# Assign the delivery to John
app.assign_driver(request3, john)

# John goes offline before completing the delivery
john.go_offline()

# Complete the delivery
request3.complete()

print("\n--- OFFLINE DRIVER RESULTS ---")
print("Request status:", request3.status)
print("John online:", john.online)
print("John available:", john.available)
print("John deliveries:", john.deliveries)

# Display request information
print("Pickup:", request1.pickup)
print("Destination:", request1.destination)
print("Fare:", request1.fare)
print("Status:", request1.status)

# Check total requests
print("Total requests:", len(app.requests))

# --- TEST DRIVER BONUS ---

test_driver = app.register_driver(
    "Test Driver",
    "08044444444",
    "Toyota Corolla"
)

test_driver.deliveries = 19

test_driver.add_delivery()

print("\n--- BONUS TEST RESULTS ---")
print("Deliveries:", test_driver.deliveries)
print("Bonus:", test_driver.bonus)
print("Wallet:", test_driver.wallet_balance)
# Test whether bonus is credited twice
test_driver.update_wallet()

print("\n--- DUPLICATE BONUS TEST ---")
print("Deliveries:", test_driver.deliveries)
print("Bonus:", test_driver.bonus)
print("Wallet:", test_driver.wallet_balance)
# --- TEST FUEL INCENTIVE ---

test_driver.deliveries = 29

test_driver.add_delivery()

print("\n--- FUEL INCENTIVE RESULTS ---")
print("Deliveries:", test_driver.deliveries)
print("Bonus:", test_driver.bonus)
print("Fuel:", test_driver.fuel)
print("Wallet:", test_driver.wallet_balance)

# Test whether fuel incentive is credited twice
test_driver.update_wallet()

print("\n--- DUPLICATE FUEL TEST ---")
print("Deliveries:", test_driver.deliveries)
print("Bonus:", test_driver.bonus)
print("Fuel:", test_driver.fuel)
print("Wallet:", test_driver.wallet_balance)

# --- TEST DRIVER DEBT RESTRICTION ---

debt_driver = app.register_driver(
    "Debt Test Driver",
    "08055555555",
    "Toyota Corolla"
)

# Set wallet to -5900
debt_driver.wallet_balance = -5900

# Process a cash payment with a ₦1,000 fare
debt_driver.process_payment(1000, "cash")

# Bring driver online
debt_driver.go_online()

# Create a new delivery request
request4 = app.create_request(
    "Rumuola",
    "GRA",
    3000
)

# Attempt to assign the request
app.assign_driver(request4, debt_driver)

print("\n--- DEBT RESTRICTION RESULTS ---")
print("Wallet:", debt_driver.wallet_balance)
print("Restriction start balance:", debt_driver.restriction_start_balance)
print("Request status:", request4.status)
print("Driver online:", debt_driver.online)
print("Driver available:", debt_driver.available)
# --- TEST DEBT RECOVERY ---

# Process a card payment of ₦5,000
debt_driver.process_payment(5000, "card")

print("\n--- DEBT RECOVERY RESULTS ---")
print("Wallet:", debt_driver.wallet_balance)
print("Recovery amount:", debt_driver.calculate_recovery())
print("Restriction start balance:", debt_driver.restriction_start_balance)
# --- TEST DRIVER REACTIVATION ---

app.assign_driver(request4, debt_driver)

print("\n--- DRIVER REACTIVATION RESULTS ---")
print("Restriction:", debt_driver.restriction_start_balance)
print("Request status:", request4.status)
print("Assigned driver:", request4.driver.name)
print("Driver available:", debt_driver.available)

# --- TEST DRIVER EARNINGS ---

print("\n--- DRIVER EARNINGS RESULTS ---")
print("Driver:", test_driver.name)
print("Deliveries:", test_driver.deliveries)
print("Earnings:", test_driver.earnings)
print("Calculated earnings:", test_driver.calculate_earnings())