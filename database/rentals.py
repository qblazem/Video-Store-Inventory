
from database.database import supabase
from database.videos import available_quantity


def create_rental(
    customer_id: int,
    video_id: int
) -> dict:
    # check if the video exists
    #.single might potentially lead to problems
    video = supabase.table("Videos").select("*").eq("video_id", video_id).single().execute()

    if not video.data:
        raise ValueError("Video does not exist")

    # check available inventory
    if available_quantity(video_id) <= 0:
        raise ValueError("No copies available for rental")

    data = {
        "customer_id": customer_id,
        "video_id": video_id,
        "currently_rented": True
    }

    response = supabase.table("Rentals").insert(data).execute()
    return response.data[0]


def get_rental(rental_id: int) -> dict | None:
    response = (
        supabase.table("Rentals")
        .select("*")
        .eq("rental_id", rental_id)
        .execute()
    )

    return response.data[0] if response.data else None


def get_all_rentals() -> list[dict]:
    response = supabase.table("Rentals").select("*").execute()
    return response.data


def get_customer_rentals(customer_id: int) -> list[dict]:
    response = (
        supabase.table("Rentals")
        .select("*")
        .eq("customer_id", customer_id)
        .execute()
    )

    return response.data


def get_active_rentals() -> list[dict]:
    response = (
        supabase.table("Rentals")
        .select("*")
        .eq("currently_rented", True)
        .execute()
    )

    return response.data


def return_rental(rental_id: int) -> dict | None:
    response = (
        supabase.table("Rentals")
        .update({"currently_rented": False})
        .eq("rental_id", rental_id)
        .eq("currently_rented", True)
        .execute()
    )

    return response.data[0] if response.data else None


