from database.database import supabase


def create_customer(
    first_name: str,
    last_name: str | None = None,
    address: str | None = None,
    phone: str | None = None,
    email: str | None = None
) -> dict:

    customer = {
        "first_name": first_name,
        "last_name": last_name,
        "address": address,
        "phone": int(phone) if phone else None,
        "email": email
    }

    response = supabase.table("Customers").insert(customer).execute()

    return response.data[0]


def get_customer(customer_id: int) -> dict | None:
    response = (
        supabase.table("Customers")
        .select("*")
        .eq("customer_id", customer_id)
        .execute()
    )

    return response.data[0] if response.data else None


def get_all_customers() -> list[dict]:

    response = (
        supabase.table("Customers")
        .select("*")
        .order("customer_id")
        .execute()
    )

    return response.data


def search_customers(search_term: str) -> list[dict]:
    if not search_term.strip():
        return []

    pattern = f"%{search_term.strip()}%"

    first = (
        supabase.table("Customers")
        .select("*")
        .ilike("first_name", pattern)
        .execute()
    )

    last = (
        supabase.table("Customers")
        .select("*")
        .ilike("last_name", pattern)
        .execute()
    )

    # combine results without duplicate customers
    customers = {
        customer["customer_id"]: customer
        for customer in first.data + last.data
    }

    return list(customers.values())


def update_customer(
    customer_id: int,
    updates: dict
) -> dict | None:
    """update a customer and return the updated record"""

    allowed_fields = {
        "first_name", "last_name", "address", "phone", "email"
    }

    if not updates or not set(updates).issubset(allowed_fields):
        raise ValueError("Invalid or empty customer updates")

    updates = updates.copy()

    if "phone" in updates:
        updates["phone"] = (
            int(updates["phone"]) if updates["phone"] else None
        )

    response = (
        supabase.table("Customers")
        .update(updates)
        .eq("customer_id", customer_id)
        .execute()
    )

    return response.data[0] if response.data else None


def delete_customer(customer_id: int) -> bool:
    """Delete a customer, return True if deleted"""

    response = (
        supabase.table("Customers")
        .delete()
        .eq("customer_id", customer_id)
        .execute()
    )

    return len(response.data) > 0