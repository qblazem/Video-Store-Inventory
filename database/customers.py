
from database.database import supabase


def create_customer(
    first_name: str,
    last_name: str | None = None,
    address: str | None = None,
    phone: str | None = None,
    email: str | None = None
) -> dict:
    """Create a customer and return the new record"""

    if not first_name or not first_name.strip():
        raise ValueError("Customer first name cannot be empty")

    customer = {
        "first_name": first_name.strip(),
        "last_name": last_name,
        "address": address,
        "phone": phone.strip() if phone else None,
        "email": email
    }

    response = (
        supabase.table("Customers")
        .insert(customer)
        .execute()
    )

    return response.data[0]


def get_customer(customer_id: int) -> dict | None:
    """Retrieve a customer by ID"""

    response = (
        supabase.table("Customers")
        .select("*")
        .eq("customer_id", customer_id)
        .execute()
    )

    return response.data[0] if response.data else None


def get_all_customers() -> list[dict]:
    """Retrieve all customers."""

    response = (
        supabase.table("Customers")
        .select("*")
        .order("customer_id")
        .execute()
    )

    return response.data


def search_customers(search_term: str) -> list[dict]:
    """Search customers by first or last name"""

    if not search_term.strip():
        return []

    pattern = f"%{search_term.strip()}%"

    response = (
        supabase.table("Customers")
        .select("*")
        .or_(
            f"first_name.ilike.{pattern},last_name.ilike.{pattern}"
        )
        .execute()
    )

    return response.data


def update_customer(
    customer_id: int,
    updates: dict
) -> dict | None:
    """Update a customer and return the updated record"""

    allowed_fields = {
        "first_name", "last_name", "address", "phone", "email"
    }

    if not updates or not set(updates).issubset(allowed_fields):
        raise ValueError("Invalid or empty customer updates")

    updates = updates.copy()

    if "first_name" in updates:
        first_name = updates["first_name"]

        if not isinstance(first_name, str) or not first_name.strip():
            raise ValueError("Customer first name cannot be empty")

        updates["first_name"] = first_name.strip()

    if "phone" in updates:
        phone = updates["phone"]
        updates["phone"] = phone.strip() if phone else None

    response = (
        supabase.table("Customers")
        .update(updates)
        .eq("customer_id", customer_id)
        .execute()
    )

    return response.data[0] if response.data else None


def delete_customer(customer_id: int) -> bool:
    """Delete a customer and return True if deleted"""

    response = (
        supabase.table("Customers")
        .delete()
        .eq("customer_id", customer_id)
        .execute()
    )

    return bool(response.data)
