# driver.py

class Driver:

    pay_per_delivery = 1500

    def __init__(self, name, phone, vehicle):
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

    def calculate_earnings(self):
        return self.deliveries * Driver.pay_per_delivery

    def calculate_bonus(self):

        if self.deliveries >= 20:
            return 5000
        else:
            return 0
    def calculate_fuel(self):

        if self.deliveries >= 30:
            return 1000
        else:
            return 0

    def add_delivery(self):
        self.deliveries += 1
        self.update_wallet()

    def update_wallet(self):

        self.bonus = self.calculate_bonus()
        self.fuel = self.calculate_fuel()

        new_bonus = self.bonus - self.credited_bonus
        new_fuel = self.fuel - self.credited_fuel

        self.wallet_balance += new_bonus + new_fuel

        self.credited_bonus = self.bonus
        self.credited_fuel = self.fuel

    def process_payment(self, fare, payment_method, discount_rate=0):

        service_fee = fare * 0.10

        discount_amount = fare * discount_rate
        discounted_fare = fare - discount_amount

        if payment_method == "cash":

            wallet_change = -service_fee
            self.wallet_balance += wallet_change

            return discounted_fare, service_fee, wallet_change

        elif payment_method == "card":

            wallet_change = fare - service_fee
            self.wallet_balance += wallet_change

            return discounted_fare, service_fee, wallet_change
