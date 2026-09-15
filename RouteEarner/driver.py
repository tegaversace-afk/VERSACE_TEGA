class Driver:

    next_id = 1
    pay_per_delivery = 1500

    def __init__(self, name, phone, vehicle):
        self.driver_id = f"RE{Driver.next_id:03d}"
        Driver.next_id += 1

        self.name = name
        self.phone = phone
        self.vehicle = vehicle

        self.deliveries = 0
        self.earnings = 0
        self.wallet_balance = 0

        self.available = False

        self.bonus = 0
        self.fuel = 0
        self.credited_bonus = 0
        self.credited_fuel = 0

        self.restriction_start_balance = None