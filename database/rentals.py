from database import supabase

def create_rental(
    customer_id: int,
    video_id: int
) -> dict:
    
    """Create a rental and return its saved record.
    Requires positive customer and video IDs.
    The database must check availability and update quantities.
    Raises ValueError for invalid IDs. Database errors pass to the GUI."""

if customer_id <= 0 or video_id <= 0:
    raise ValueError("Customer and Videos IDs must be positive.")
    
    result = supabase.rpc(
        "create_rental",
        {"p_customer_id": customer_id, "p_video_id": video_id}
    ).execute()

    return result.data


def get_rental(rental_id: int) -> dict | None:
    pass


def get_all_rentals() -> list[dict]:
    pass


def get_customer_rentals(customer_id: int) -> list[dict]:
    pass


def get_active_rentals() -> list[dict]:
    pass


def return_rental(rental_id: int) -> dict | None:
    pass
