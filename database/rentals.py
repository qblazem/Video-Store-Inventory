
from datetime import datetime, timezone

from database.database import supabase
from database.customers import get_customer
from database.videos import get_video, available_quantity


def create_rental(
    customer_id: int,
    video_id: int
) -> dict:
    """Create a rental if the customer and video exist"""

    customer = get_customer(customer_id)

    if customer is None:
        raise ValueError("Customer does not exist")

    video = get_video(video_id)

    if video is None:
        raise ValueError("Video does not exist")

    if available_quantity(video_id) <= 0:
        raise ValueError("No copies available for rental")

    data = {
        "customer_id": customer_id,
        "video_id": video_id
    }

    response = (
        supabase.table("Rentals")
        .insert(data)
        .execute()
    )

    return response.data[0]


def get_rental(rental_id: int) -> dict | None:
    """Get a rental by ID or none if not found"""

    response = (
        supabase.table("Rentals")
        .select("*")
        .eq("rental_id", rental_id)
        .execute()
    )

    return response.data[0] if response.data else None


def get_all_rentals() -> list[dict]:
    """Return all rental records"""

    response = (
        supabase.table("Rentals")
        .select("*")
        .order("rental_id")
        .execute()
    )

    return response.data


def get_customer_rentals(customer_id: int) -> list[dict]:
    """Return all rentals for a customer"""

    response = (
        supabase.table("Rentals")
        .select("*")
        .eq("customer_id", customer_id)
        .order("rented_at", desc=True)
        .execute()
    )

    return response.data


def get_active_rentals() -> list[dict]:
    """Return all currently active rentals"""

    response = (
        supabase.table("Rentals")
        .select("*")
        .eq("currently_rented", True)
        .order("rented_at", desc=True)
        .execute()
    )

    return response.data


def return_rental(rental_id: int) -> dict | None:
    """Return an active rental and record the return time"""

    response = (
        supabase.table("Rentals")
        .update({
            "currently_rented": False,
            "returned_at": datetime.now(timezone.utc).isoformat()
        })
        .eq("rental_id", rental_id)
        .eq("currently_rented", True)
        .execute()
    )

    return response.data[0] if response.data else None
