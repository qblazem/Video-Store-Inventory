
import re

from database.database import supabase


def _validate_customer_fields(fields: dict) -> dict:
    """Check and clean customer details before saving"""

    fields = fields.copy()
    labels = {
        "first_name": "First name",
        "last_name": "Last name",
        "address": "Address",
        "phone": "Phone",
        "email": "Email"
    }

    for key, label in labels.items():
        if key not in fields:
            continue
        value = fields[key]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{label} is required")
        fields[key] = value.strip()

    if "phone" in fields:
        phone = fields["phone"]
        digits = re.sub(r"\D", "", phone)
        if len(digits) != 10 or not re.fullmatch(r"[0-9() .-]+", phone):
            raise ValueError("Enter a valid 10-digit phone number")
        fields["phone"] = f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"

    if "email" in fields:
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", fields["email"]):
            raise ValueError("Enter a valid email address")

    return fields


def create_customer(
    first_name: str,
    last_name: str | None = None,
    address: str | None = None,
    phone: str | None = None,
    email: str | None = None
) -> dict:
    """Create a customer and return the new record"""

    customer = _validate_customer_fields({
        "first_name": first_name,
        "last_name": last_name,
        "address": address,
        "phone": phone,
        "email": email
    })

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
    """Retrieve all customers"""

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

    updates = _validate_customer_fields(updates)

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

