class Request:

    def __init__(self, pickup, destination, fare):
        self.pickup = pickup
        self.destination = destination
        self.fare = fare

        self.status = "Pending"
        self.driver = None