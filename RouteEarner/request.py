class Request:

    def __init__(self, pickup, destination, fare):
        self.pickup = pickup
        self.destination = destination
        self.fare = fare

        self.status = "Pending"
        self.driver = None

    def complete(self):

        if self.status == "Delivered":
            print("Request already completed.")
            return

        if self.driver is None:
            print("No driver assigned to this request.")
            return

        if self.status != "Assigned":
            print("Request must be assigned before completion.")
            return
        self.status = "Delivered"

        customer_paid, service_fee, wallet_change = self.driver.process_payment(
            self.fare,
            self.payment_method,
            self.discount_rate
)

        self.customer_paid = customer_paid
        self.service_fee = service_fee
        self.wallet_change = wallet_change

        self.driver.add_delivery()
        self.driver.go_online()