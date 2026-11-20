import unittest

from routeearner import RouteEarner


class TestRouteEarner(unittest.TestCase):

    def test_register_driver(self):

        app = RouteEarner()

        driver = app.register_driver(
            "Tega",
            "08011111111",
            "Toyota Camry"
        )

        self.assertEqual(driver.name, "Tega")
        self.assertEqual(driver.phone, "08011111111")
        self.assertEqual(driver.vehicle, "Toyota Camry")
        self.assertEqual(len(app.drivers), 1)
        
    def test_driver_availability(self):

        app = RouteEarner()

        driver = app.register_driver(
            "John",
            "08022222222",
            "Honda Accord"
        )

        self.assertFalse(driver.online)
        self.assertFalse(driver.available)

        driver.go_online()

        self.assertTrue(driver.online)
        self.assertTrue(driver.available)

        driver.go_offline()

        self.assertFalse(driver.online)
        self.assertFalse(driver.available)

    def test_create_request(self):

        app = RouteEarner()

        request = app.create_request(
            "Rumuola",
            "GRA",
            5000
        )

        self.assertEqual(request.pickup, "Rumuola")
        self.assertEqual(request.destination, "GRA")
        self.assertEqual(request.fare, 5000)
        self.assertEqual(request.payment_method, "cash")
        self.assertEqual(request.discount_rate, 0)
        self.assertEqual(request.status, "Pending")
        self.assertEqual(len(app.requests), 1)

    def test_assign_driver(self):

        app = RouteEarner()

        driver = app.register_driver(
            "Mary",
            "08033333333",
            "Toyota Corolla"
        )

        driver.go_online()

        request = app.create_request(
            "Rumuola",
            "GRA",
            5000
        )

        app.assign_driver(request, driver)

        self.assertEqual(request.driver, driver)
        self.assertEqual(request.status, "Assigned")
        self.assertFalse(driver.available)
        self.assertTrue(driver.online)

    def test_complete_cash_delivery(self):

        app = RouteEarner()

        driver = app.register_driver(
            "Peter",
            "08011111111",
            "Toyota Camry"
        )

        driver.go_online()

        request = app.create_request(
            "Rumuola",
            "GRA",
            5000
        )

        app.assign_driver(request, driver)

        request.complete()

        self.assertEqual(request.status, "Delivered")
        self.assertEqual(request.customer_paid, 5000)
        self.assertEqual(request.service_fee, 500)
        self.assertEqual(driver.wallet_balance, -500)
        self.assertEqual(driver.deliveries, 1)
        self.assertEqual(driver.earnings, 1500)
        self.assertTrue(driver.available)

    def test_complete_card_delivery_with_discount(self):

        app = RouteEarner()

        driver = app.register_driver(
            "John",
            "08022222222",
            "Honda Accord"
        )

        driver.go_online()

        request = app.create_request(
            "Rumuola",
            "GRA",
            5000,
            payment_method="card",
            discount_rate=0.20
        )

        app.assign_driver(request, driver)

        request.complete()

        self.assertEqual(request.status, "Delivered")
        self.assertEqual(request.customer_paid, 4000)
        self.assertEqual(request.service_fee, 500)
        self.assertEqual(driver.wallet_balance, 4500)
        self.assertEqual(driver.deliveries, 1)

    def test_driver_restricted_by_debt(self):

        app = RouteEarner()

        driver = app.register_driver(
            "Peter",
            "08033333333",
            "Toyota Camry"
        )

        driver.go_online()

        # Simulate a driver whose wallet has reached the debt limit
        driver.wallet_balance = -6000
        driver.check_cash_restriction()

        request = app.create_request(
            "Rumuola",
            "GRA",
            5000
        )

        app.assign_driver(request, driver)

        self.assertEqual(driver.wallet_balance, -6000)
        self.assertIsNotNone(driver.restriction_start_balance)
        self.assertIsNone(request.driver)
        self.assertEqual(request.status, "Pending")
        self.assertTrue(driver.online)
        self.assertTrue(driver.available)

    def test_driver_debt_recovery(self):

        app = RouteEarner()

        driver = app.register_driver(
            "Mary",
            "08044444444",
            "Toyota Corolla"
        )

        driver.go_online()

        # Put the driver under debt restriction
        driver.wallet_balance = -6000
        driver.check_cash_restriction()

        # A card payment should help recover the debt
        driver.process_payment(
            5000,
            payment_method="card"
        )

        self.assertEqual(driver.wallet_balance, -1500)
        self.assertIsNone(driver.restriction_start_balance)

    def test_driver_bonus_eligibility(self):

        app = RouteEarner()

        driver = app.register_driver(
            "Tega",
            "08055555555",
            "Toyota Camry"
        )

        # Set the driver just below the bonus threshold
        driver.deliveries = 19
        driver.update_wallet()

        self.assertEqual(driver.bonus, 0)
        self.assertEqual(driver.wallet_balance, 0)

        # Complete the 20th delivery
        driver.add_delivery()

        self.assertEqual(driver.deliveries, 20)
        self.assertEqual(driver.bonus, 5000)
        self.assertEqual(driver.wallet_balance, 5000)

        # Confirm the bonus is not credited twice
        driver.update_wallet()

        self.assertEqual(driver.wallet_balance, 5000)

    def test_driver_fuel_eligibility(self):

        app = RouteEarner()

        driver = app.register_driver(
            "John",
            "08066666666",
            "Honda Accord"
        )

        # Set the driver just below the fuel incentive threshold
        driver.deliveries = 29
        driver.update_wallet()

        self.assertEqual(driver.bonus, 5000)
        self.assertEqual(driver.fuel, 0)
        self.assertEqual(driver.wallet_balance, 5000)

        # Complete the 30th delivery
        driver.add_delivery()

        self.assertEqual(driver.deliveries, 30)
        self.assertEqual(driver.bonus, 5000)
        self.assertEqual(driver.fuel, 1000)
        self.assertEqual(driver.wallet_balance, 6000)

        # Confirm incentives are not credited twice
        driver.update_wallet()

        self.assertEqual(driver.wallet_balance, 6000)

    def test_driver_earnings_calculation(self):

        app = RouteEarner()

        driver = app.register_driver(
            "Peter",
            "08077777777",
            "Toyota Camry"
        )

        # Record 10 completed deliveries
        for _ in range(10):
            driver.add_delivery()

        self.assertEqual(driver.deliveries, 10)
        self.assertEqual(driver.earnings, 15000)
        self.assertEqual(driver.calculate_earnings(), 15000)

        # Earnings should remain separate from wallet balance
        self.assertEqual(driver.wallet_balance, 0)

    def test_offline_driver_delivery(self):

        app = RouteEarner()

        driver = app.register_driver(
            "Mary",
            "08088888888",
            "Toyota Corolla"
        )

        # Bring the driver online
        driver.go_online()

        request = app.create_request(
            "Rumuola",
            "GRA",
            5000
        )

        app.assign_driver(request, driver)

        # Driver goes offline after receiving the request
        driver.go_offline()

        # Complete the already-assigned delivery
        request.complete()

        self.assertEqual(request.status, "Delivered")
        self.assertEqual(driver.deliveries, 1)
        self.assertFalse(driver.online)
        self.assertFalse(driver.available)

    def test_request_completion_protection(self):

        app = RouteEarner()

        driver = app.register_driver(
            "Tega",
            "08099999999",
            "Toyota Camry"
        )

        driver.go_online()

        request = app.create_request(
            "Rumuola",
            "GRA",
            5000
        )

        # Try completing without assigning a driver
        request.complete()

        self.assertEqual(request.status, "Pending")
        self.assertEqual(driver.deliveries, 0)
        self.assertEqual(driver.wallet_balance, 0)

        # Assign the driver and complete the request
        app.assign_driver(request, driver)
        request.complete()

        self.assertEqual(request.status, "Delivered")
        self.assertEqual(driver.deliveries, 1)

        # Record the wallet balance after completion
        wallet_before = driver.wallet_balance

        # Try completing the same request again
        request.complete()

        self.assertEqual(request.status, "Delivered")
        self.assertEqual(driver.deliveries, 1)
        self.assertEqual(driver.wallet_balance, wallet_before)

    def test_invalid_payment_method(self):

        app = RouteEarner()

        driver = app.register_driver(
            "Peter",
            "08011112222",
            "Toyota Camry"
        )

        driver.go_online()

        request = app.create_request(
            "Rumuola",
            "GRA",
            5000,
            payment_method="transfer"
        )

        app.assign_driver(request, driver)

        request.complete()

        self.assertEqual(request.status, "Assigned")
        self.assertEqual(driver.deliveries, 0)
        self.assertEqual(driver.wallet_balance, 0)

    def test_duplicate_driver_registration(self):

        app = RouteEarner()

        app.register_driver(
            "Peter",
            "08011111111",
            "Toyota Camry"
        )

        with self.assertRaises(ValueError):
            app.register_driver(
                "John",
                "08011111111",
                "Honda Accord"
            )

        self.assertEqual(len(app.drivers), 1)

    def test_prevent_duplicate_request_assignment(self):

        app = RouteEarner()

        driver_one = app.register_driver(
            "Peter",
            "08011111111",
            "Toyota Camry"
        )

        driver_two = app.register_driver(
            "John",
            "08022222222",
            "Honda Accord"
        )

        driver_one.go_online()
        driver_two.go_online()

        request = app.create_request(
            "Rumuola",
            "GRA",
            5000
        )

        # Assign the first driver
        app.assign_driver(request, driver_one)

        # Attempt to assign the same request to another driver
        app.assign_driver(request, driver_two)

        self.assertEqual(request.driver, driver_one)
        self.assertEqual(request.status, "Assigned")

        self.assertFalse(driver_one.available)
        self.assertTrue(driver_two.available)

    def test_prevent_assignment_to_unavailable_driver(self):

        app = RouteEarner()

        driver = app.register_driver(
            "Mary",
            "08033333333",
            "Toyota Corolla"
        )

        # Driver is initially offline and unavailable
        request = app.create_request(
            "Rumuola",
            "GRA",
            5000
        )

        app.assign_driver(request, driver)

        self.assertIsNone(request.driver)
        self.assertEqual(request.status, "Pending")
        self.assertFalse(driver.available)

        # Bring the driver online
        driver.go_online()

        # Assign the request successfully
        app.assign_driver(request, driver)

        self.assertEqual(request.driver, driver)
        self.assertEqual(request.status, "Assigned")
        self.assertFalse(driver.available)

    def test_prevent_assignment_of_delivered_request(self):

        app = RouteEarner()

        driver_one = app.register_driver(
            "Peter",
            "08011111111",
            "Toyota Camry"
        )

        driver_two = app.register_driver(
            "John",
            "08022222222",
            "Honda Accord"
        )

        driver_one.go_online()
        driver_two.go_online()

        request = app.create_request(
            "Rumuola",
            "GRA",
            5000
        )

        # Assign and complete the delivery
        app.assign_driver(request, driver_one)
        request.complete()

        # Try assigning the delivered request to another driver
        app.assign_driver(request, driver_two)

        self.assertEqual(request.status, "Delivered")
        self.assertEqual(request.driver, driver_one)

        self.assertTrue(driver_two.available)
        self.assertEqual(driver_one.deliveries, 1)
        self.assertEqual(driver_two.deliveries, 0)

    def test_debt_recovery_below_threshold(self):

        app = RouteEarner()

        driver = app.register_driver(
            "Mary",
            "08044444444",
            "Toyota Corolla"
        )

        driver.wallet_balance = -6000
        driver.check_cash_restriction()

        # Card payment adds ₦3,600 after the service fee
        driver.process_payment(
            4000,
            payment_method="card"
        )

        self.assertEqual(driver.wallet_balance, -2400)
        self.assertEqual(driver.calculate_recovery(), 3600)

        # Restriction should remain because recovery is below ₦4,200
        self.assertEqual(driver.restriction_start_balance, -6000)

    def test_exact_debt_recovery_threshold(self):

        app = RouteEarner()

        driver = app.register_driver(
            "John",
            "08055555555",
            "Honda Accord"
        )

        # Start with a debt restriction
        driver.wallet_balance = -6000
        driver.check_cash_restriction()

        # Simulate exactly ₦4,200 in debt recovery
        driver.wallet_balance = -1800

        driver.update_recovery()

        self.assertEqual(driver.wallet_balance, -1800)
        self.assertIsNone(driver.restriction_start_balance)

    def test_cash_payment_debt_accumulation(self):

        app = RouteEarner()

        driver = app.register_driver(
            "Peter",
            "08066666666",
            "Toyota Camry"
        )

        driver.go_online()

        # Complete 12 cash deliveries
        for _ in range(12):

            request = app.create_request(
                "Rumuola",
                "GRA",
                5000,
                payment_method="cash"
            )

            app.assign_driver(request, driver)
            request.complete()

        self.assertEqual(driver.deliveries, 12)
        self.assertEqual(driver.wallet_balance, -6000)

        self.assertEqual(
            driver.restriction_start_balance,
            -6000
        )

        self.assertTrue(driver.online)

    def test_cash_debt_beyond_restriction_threshold(self):

        app = RouteEarner()

        driver = app.register_driver(
            "John",
            "08077777777",
            "Honda Accord"
        )

        driver.go_online()

        # Start just above the debt restriction threshold
        driver.wallet_balance = -5900

        request = app.create_request(
            "Rumuola",
            "GRA",
            5000,
            payment_method="cash"
        )

        app.assign_driver(request, driver)

        request.complete()

        self.assertEqual(request.status, "Delivered")
        self.assertEqual(driver.wallet_balance, -6400)

        self.assertEqual(
            driver.restriction_start_balance,
            -6400
        )

        self.assertEqual(driver.deliveries, 1)

    def test_automatic_debt_restriction_during_dispatch(self):

        app = RouteEarner()

        driver = app.register_driver(
            "Mary",
            "08088888888",
            "Toyota Corolla"
        )

        driver.go_online()

        # Set wallet just above the restriction threshold
        driver.wallet_balance = -5500

        first_request = app.create_request(
            "Rumuola",
            "GRA",
            5000,
            payment_method="cash"
        )

        app.assign_driver(first_request, driver)
        first_request.complete()

        # Confirm debt restriction was activated
        self.assertEqual(driver.wallet_balance, -6000)
        self.assertEqual(
            driver.restriction_start_balance,
            -6000
        )

        # Attempt to assign another delivery
        second_request = app.create_request(
            "GRA",
            "Choba",
            4000
        )

        app.assign_driver(second_request, driver)

        self.assertIsNone(second_request.driver)
        self.assertEqual(second_request.status, "Pending")
        self.assertEqual(driver.deliveries, 1)

    def test_driver_reactivation_after_debt_recovery(self):

        app = RouteEarner()

        driver = app.register_driver(
            "John",
            "08099999999",
            "Honda Accord"
        )

        driver.go_online()

        # Activate the debt restriction
        driver.wallet_balance = -6000
        driver.check_cash_restriction()

        self.assertIsNotNone(driver.restriction_start_balance)

        # Simulate a card payment that helps recover the debt
        driver.process_payment(
            5000,
            payment_method="card"
        )

        # Confirm that the restriction has been cleared
        self.assertEqual(driver.wallet_balance, -1500)
        self.assertIsNone(driver.restriction_start_balance)

        # Attempt to assign a new delivery
        request = app.create_request(
            "Rumuola",
            "GRA",
            5000
        )

        app.assign_driver(request, driver)

        self.assertEqual(request.driver, driver)
        self.assertEqual(request.status, "Assigned")
        self.assertFalse(driver.available)

    def test_card_request_creation_with_discount(self):

        app = RouteEarner()

        request = app.create_request(
            "Rumuola",
            "GRA",
            5000,
            payment_method="card",
            discount_rate=0.20
        )

        self.assertEqual(request.pickup, "Rumuola")
        self.assertEqual(request.destination, "GRA")
        self.assertEqual(request.fare, 5000)

        self.assertEqual(request.payment_method, "card")
        self.assertEqual(request.discount_rate, 0.20)

        self.assertEqual(request.status, "Pending")
        self.assertIsNone(request.driver)

        self.assertEqual(len(app.requests), 1)

    def test_default_request_settings(self):

        app = RouteEarner()

        request = app.create_request(
            "Rumuola",
            "GRA",
            5000
        )

        self.assertEqual(request.payment_method, "cash")
        self.assertEqual(request.discount_rate, 0)

        self.assertEqual(request.status, "Pending")
        self.assertIsNone(request.driver)

        self.assertEqual(request.fare, 5000)

    def test_multiple_driver_registrations(self):

        app = RouteEarner()

        driver_one = app.register_driver(
            "Peter",
            "08011111111",
            "Toyota Camry"
        )

        driver_two = app.register_driver(
            "John",
            "08022222222",
            "Honda Accord"
        )

        driver_three = app.register_driver(
            "Mary",
            "08033333333",
            "Toyota Corolla"
        )

        self.assertEqual(len(app.drivers), 3)

        self.assertEqual(app.drivers[0], driver_one)
        self.assertEqual(app.drivers[1], driver_two)
        self.assertEqual(app.drivers[2], driver_three)

        self.assertEqual(driver_one.name, "Peter")
        self.assertEqual(driver_two.name, "John")
        self.assertEqual(driver_three.name, "Mary")

    def test_reject_driver_without_phone(self):

        app = RouteEarner()

        with self.assertRaises(ValueError):
            app.register_driver(
                "Peter",
                "",
                "Toyota Camry"
            )

        self.assertEqual(len(app.drivers), 0)

    def test_reject_driver_without_name(self):

        app = RouteEarner()

        with self.assertRaises(ValueError):
            app.register_driver(
                "",
                "08044444444",
                "Toyota Camry"
            )

        self.assertEqual(len(app.drivers), 0)

    def test_reject_driver_without_vehicle(self):

        app = RouteEarner()

        with self.assertRaises(ValueError):
            app.register_driver(
                "Peter",
                "08055555555",
                ""
            )

        self.assertEqual(len(app.drivers), 0)

    def test_reject_driver_name_with_only_spaces(self):

        app = RouteEarner()

        with self.assertRaises(ValueError):
            app.register_driver(
                "   ",
                "08066666666",
                "Toyota Camry"
            )

        self.assertEqual(len(app.drivers), 0)

    def test_reject_phone_with_only_spaces(self):

        app = RouteEarner()

        with self.assertRaises(ValueError):
            app.register_driver(
                "Peter",
                "   ",
                "Toyota Camry"
            )

        self.assertEqual(len(app.drivers), 0)

    def test_reject_vehicle_with_only_spaces(self):

        app = RouteEarner()

        with self.assertRaises(ValueError):
            app.register_driver(
                "Peter",
                "08077777777",
                "   "
            )

        self.assertEqual(len(app.drivers), 0)

    def test_reject_short_phone_number(self):

        app = RouteEarner()

        with self.assertRaises(ValueError):
            app.register_driver(
                "Peter",
                "08012345",
                "Toyota Camry"
            )

        self.assertEqual(len(app.drivers), 0)
    def test_reject_letters_in_phone_number(self):

        app = RouteEarner()

        with self.assertRaises(ValueError):
            app.register_driver(
                "Peter",
                "abcdefghijk",
                "Toyota Camry"
            )

        self.assertEqual(len(app.drivers), 0)

    def test_reject_special_characters_in_phone(self):

        app = RouteEarner()

        with self.assertRaises(ValueError):
            app.register_driver(
                "Peter",
                "080123456@#",
                "Toyota Camry"
            )

        self.assertEqual(len(app.drivers), 0)

    def test_reject_spaces_inside_phone_number(self):

        app = RouteEarner()

        with self.assertRaises(ValueError):
            app.register_driver(
                "Peter",
                "080 1234567",
                "Toyota Camry"
            )

        self.assertEqual(len(app.drivers), 0)

    def test_reject_long_phone_number(self):

        app = RouteEarner()

        with self.assertRaises(ValueError):
            app.register_driver(
                "Peter",
                "080123456789",
                "Toyota Camry"
            )

        self.assertEqual(len(app.drivers), 0)

    def test_reject_phone_with_leading_space(self):

        app = RouteEarner()

        with self.assertRaises(ValueError):
            app.register_driver(
                "Peter",
                " 08012345678",
                "Toyota Camry"
            )

        self.assertEqual(len(app.drivers), 0)
    def test_reject_phone_with_trailing_space(self):

        app = RouteEarner()

        with self.assertRaises(ValueError):
            app.register_driver(
                "Peter",
                "08012345678 ",
                "Toyota Camry"
            )

        self.assertEqual(len(app.drivers), 0)

    def test_reject_duplicate_phone_number(self):

        app = RouteEarner()

        app.register_driver(
            "Peter",
            "08011111111",
            "Toyota Camry"
        )

        with self.assertRaises(ValueError):
            app.register_driver(
                "John",
                "08011111111",
                "Honda Accord"
            )

        self.assertEqual(len(app.drivers), 1)

    def test_register_driver_with_valid_details(self):

        app = RouteEarner()

        driver = app.register_driver(
            "Tega",
            "08098765432",
            "Toyota Corolla"
        )

        self.assertEqual(driver.name, "Tega")
        self.assertEqual(driver.phone, "08098765432")
        self.assertEqual(driver.vehicle, "Toyota Corolla")

        self.assertEqual(len(app.drivers), 1)

    def test_reject_phone_number_as_integer(self):

        app = RouteEarner()

        with self.assertRaises(ValueError):
            app.register_driver(
                "Peter",
                8012345678,
                "Toyota Camry"
            )

        self.assertEqual(len(app.drivers), 0)



if __name__ == "__main__":
    unittest.main()
