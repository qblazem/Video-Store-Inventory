import unittest
from unittest.mock import patch

from database import rentals


class TestRentals(unittest.TestCase):

    def setUp(self):
        """Give each test its own fake database and rental."""
        self.patcher = patch("database.rentals.supabase", create=True)
        self.db = self.patcher.start()
        self.addCleanup(self.patcher.stop)

        self.rental = {
            "rental_id": 1,
            "customer_id": 2,
            "video_id": 3,
            "rented_at": "2026-11-01T10:00:00+00:00",
            "currently_rented": True
        }

        self.table = self.db.table.return_value
        self.query = self.table.select.return_value
        self.filtered = self.query.eq.return_value

    def test_get_existing_rental(self):
        """Find a rental by its ID."""
        self.filtered.execute.return_value.data = [self.rental]

        result = rentals.get_rental(1)

        self.assertEqual(result, self.rental)
        self.db.table.assert_called_once_with("Rentals")
        self.query.eq.assert_called_once_with("rental_id", 1)
        self.filtered.execute.assert_called_once()

    def test_get_missing_rental(self):
        """Return None when the rental does not exist."""
        self.filtered.execute.return_value.data = []

        result = rentals.get_rental(999)

        self.assertIsNone(result)
        self.db.table.assert_called_once_with("Rentals")
        self.query.eq.assert_called_once_with("rental_id", 999)
        self.filtered.execute.assert_called_once()

    def test_get_rental_database_error(self):
        """Let the caller know when a rental lookup fails."""
        self.filtered.execute.side_effect = RuntimeError(
            "Database unavailable"
        )

        with self.assertRaisesRegex(RuntimeError, "Database unavailable"):
            rentals.get_rental(1)

        self.db.table.assert_called_once_with("Rentals")
        self.query.eq.assert_called_once_with("rental_id", 1)
        self.filtered.execute.assert_called_once()

    def test_get_all_rentals(self):
        """Include both active and returned rentals."""
        returned = self.rental.copy()
        returned["rental_id"] = 2
        returned["currently_rented"] = False

        records = [self.rental, returned]
        self.query.execute.return_value.data = records

        result = rentals.get_all_rentals()

        self.assertEqual(result, records)
        self.db.table.assert_called_once_with("Rentals")
        self.query.execute.assert_called_once()
        self.query.eq.assert_not_called()

    def test_get_all_rentals_when_empty(self):
        """Return an empty list when there are no rentals."""
        self.query.execute.return_value.data = []

        result = rentals.get_all_rentals()

        self.assertEqual(result, [])
        self.db.table.assert_called_once_with("Rentals")
        self.query.execute.assert_called_once()

    def test_get_all_rentals_database_error(self):
        """Do not treat a database error as an empty rental list."""
        self.query.execute.side_effect = RuntimeError(
            "Database unavailable"
        )

        with self.assertRaisesRegex(RuntimeError, "Database unavailable"):
            rentals.get_all_rentals()

        self.db.table.assert_called_once_with("Rentals")
        self.query.execute.assert_called_once()

    def test_get_customer_rentals(self):
        """Return a customer's active and past rentals."""
        returned = self.rental.copy()
        returned["rental_id"] = 2
        returned["currently_rented"] = False

        records = [self.rental, returned]
        self.filtered.execute.return_value.data = records

        result = rentals.get_customer_rentals(2)

        self.assertEqual(result, records)
        self.db.table.assert_called_once_with("Rentals")
        self.query.eq.assert_called_once_with("customer_id", 2)
        self.filtered.execute.assert_called_once()

    def test_get_customer_rentals_when_empty(self):
        """Return an empty list for a customer with no rentals."""
        self.filtered.execute.return_value.data = []

        result = rentals.get_customer_rentals(99)

        self.assertEqual(result, [])
        self.db.table.assert_called_once_with("Rentals")
        self.query.eq.assert_called_once_with("customer_id", 99)
        self.filtered.execute.assert_called_once()

    def test_get_active_rentals(self):
        """Request only rentals marked as currently rented."""
        self.filtered.execute.return_value.data = [self.rental]

        result = rentals.get_active_rentals()

        self.assertEqual(result, [self.rental])
        self.db.table.assert_called_once_with("Rentals")
        self.query.eq.assert_called_once_with("currently_rented", True)
        self.filtered.execute.assert_called_once()

    def test_get_active_rentals_when_empty(self):
        """Return an empty list when no rentals are active."""
        self.filtered.execute.return_value.data = []

        result = rentals.get_active_rentals()

        self.assertEqual(result, [])
        self.db.table.assert_called_once_with("Rentals")
        self.query.eq.assert_called_once_with("currently_rented", True)
        self.filtered.execute.assert_called_once()


if __name__ == "__main__":
    unittest.main()
