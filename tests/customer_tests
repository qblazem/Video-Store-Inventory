import unittest
from unittest.mock import patch

from database import customers


class TestCustomers(unittest.TestCase):

    def setUp(self):
        """Give each test its own fake database and customer."""
        self.patcher = patch("database.customers.supabase", create=True)
        self.db = self.patcher.start()
        self.addCleanup(self.patcher.stop)

        self.customer = {
            "customer_id": 1,
            "first_name": "Sam",
            "last_name": "Test",
            "address": "123 Test Street",
            "phone": "515-555-0100",
            "email": "sam@example.com"
        }

        self.table = self.db.table.return_value
        self.query = self.table.select.return_value

    def test_create_customer(self):
        """Save the supplied details and return the new customer."""
        details = self.customer.copy()
        del details["customer_id"]

        insert = self.table.insert.return_value
        insert.execute.return_value.data = [self.customer]

        result = customers.create_customer(**details)

        self.assertEqual(result, self.customer)
        self.db.table.assert_called_once_with("Customers")
        self.table.insert.assert_called_once_with(details)
        insert.execute.assert_called_once()

    def test_create_customer_rejects_blank_name(self):
        """Reject a blank first name without accessing the database."""
        with self.assertRaises(ValueError):
            customers.create_customer("   ")

        self.db.table.assert_not_called()

    def test_get_existing_customer(self):
        """Find a customer by their ID."""
        lookup = self.query.eq.return_value
        lookup.execute.return_value.data = [self.customer]

        result = customers.get_customer(1)

        self.assertEqual(result, self.customer)
        self.db.table.assert_called_once_with("Customers")
        self.query.eq.assert_called_once_with("customer_id", 1)
        lookup.execute.assert_called_once()

    def test_get_missing_customer(self):
        """Return None when the requested customer is missing."""
        lookup = self.query.eq.return_value
        lookup.execute.return_value.data = []

        result = customers.get_customer(999)

        self.assertIsNone(result)
        self.db.table.assert_called_once_with("Customers")
        self.query.eq.assert_called_once_with("customer_id", 999)
        lookup.execute.assert_called_once()

    def test_get_all_customers(self):
        """Return all customer records provided by the database."""
        self.query.execute.return_value.data = [self.customer]

        result = customers.get_all_customers()

        self.assertEqual(result, [self.customer])
        self.db.table.assert_called_once_with("Customers")
        self.query.execute.assert_called_once()

    def test_get_all_customers_when_empty(self):
        """Return an empty list when no customers exist."""
        self.query.execute.return_value.data = []

        result = customers.get_all_customers()

        self.assertEqual(result, [])
        self.db.table.assert_called_once_with("Customers")
        self.query.execute.assert_called_once()

    def test_search_customers_with_match(self):
        """Search for a partial first-name match."""
        search = self.query.ilike.return_value
        search.execute.return_value.data = [self.customer]

        result = customers.search_customers("Sam")

        self.assertEqual(result, [self.customer])
        self.db.table.assert_called_once_with("Customers")
        self.query.ilike.assert_called_once_with("first_name", "%Sam%")
        search.execute.assert_called_once()

    def test_search_customers_without_match(self):
        """Return an empty list when the search finds nothing."""
        search = self.query.ilike.return_value
        search.execute.return_value.data = []

        result = customers.search_customers("Nobody")

        self.assertEqual(result, [])
        self.db.table.assert_called_once_with("Customers")
        self.query.ilike.assert_called_once_with("first_name", "%Nobody%")
        search.execute.assert_called_once()

    def test_update_customer(self):
        """Update the selected customer's phone number."""
        changes = {"phone": "515-555-0101"}
        updated = self.customer.copy()
        updated.update(changes)

        update = self.table.update.return_value
        save = update.eq.return_value
        save.execute.return_value.data = [updated]

        result = customers.update_customer(1, changes)

        self.assertEqual(result, updated)
        self.db.table.assert_called_once_with("Customers")
        self.table.update.assert_called_once_with(changes)
        update.eq.assert_called_once_with("customer_id", 1)
        save.execute.assert_called_once()

    def test_customer_lookup_database_error(self):
        """Let the caller know when a database request fails."""
        lookup = self.query.eq.return_value
        lookup.execute.side_effect = RuntimeError("Database unavailable")

        with self.assertRaisesRegex(RuntimeError, "Database unavailable"):
            customers.get_customer(1)

        self.db.table.assert_called_once_with("Customers")
        self.query.eq.assert_called_once_with("customer_id", 1)


if __name__ == "__main__":
    unittest.main()
