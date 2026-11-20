from driver import Driver
from request import Request


class RouteEarner:

    def __init__(self):
        self.drivers = []
        self.requests = []

    def register_driver(self, name, phone, vehicle):
        if not vehicle or not vehicle.strip():
            raise ValueError("Vehicle is required.")
        if not name or not name.strip():
            raise ValueError("Driver name is required.")
        if not isinstance(phone, str):
            raise ValueError("Phone number must be a string.")
        if not phone or not phone.strip():
            raise ValueError("Phone number is required.")
        if len(phone) != 11:
            raise ValueError("Phone number must contain exactly 11 digits.")
        if not phone.isdigit():
            raise ValueError("Phone number must contain only digits.")

        for driver in self.drivers:
            if driver.phone == phone:
                raise ValueError("Phone number already registered.")

        new_driver = Driver(name, phone, vehicle)

        self.drivers.append(new_driver)

        return new_driver

    def create_request(self, pickup, destination, fare,
                        payment_method="cash", discount_rate=0):

        new_request = Request(
            pickup,
            destination,
            fare,
            payment_method,
            discount_rate
        )

        self.requests.append(new_request)

        return new_request

    def assign_driver(self, request, driver):

        if not driver.available:
            print("Driver is not available.")
            return
        
        if driver.restriction_start_balance is not None:
            print("Driver is restricted due to outstanding debt.")
            return

        if request.status != "Pending":
            print("Request is not pending.")
            return

        request.driver = driver
        request.status = "Assigned"

        driver.available = False
            