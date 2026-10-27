
from database.database import supabase


def create_video(
    title: str,
    year: str | None = None,
    director: str | None = None,
    rating: float | None = None,
    genre: str | None = None,
    total_quantity: int = 0
        #0 is a placeholder, needs to pull quantities from database probably
) -> dict:
    """Create a video and return the new record"""

    if not title.strip():
        raise ValueError("Video title cannot be empty")

    if total_quantity < 0:
        raise ValueError("Total quantity cannot be negative")

    video = {
        "title": title,
        "year": year,
        "director": director,
        "rating": rating,
        "genre": genre,
        "total_quantity": total_quantity
    }

    response = supabase.table("Videos").insert(video).execute()

    return response.data[0]


def get_video(video_id: int) -> dict | None:
    """Get a video by ID, or none if not found"""

    response = (
        supabase.table("Videos")
        .select("*")
        .eq("video_id", video_id)
        .execute()
    )

    return response.data[0] if response.data else None


def get_all_videos() -> list[dict]:
    """Return all videos (up to the API row limit)"""

    response = (
        supabase.table("Videos")
        .select("*")
        .order("video_id")
        .execute()
    )

    return response.data


def search_video(search_term: str) -> list[dict]:
    """Search videos by title, director, or genre"""

    if not search_term.strip():
        return []

    pattern = f"%{search_term.strip()}%"

    response = (
        supabase.table("Videos")
        .select("*")
        .or_(
            f"title.ilike.{pattern},"
            f"director.ilike.{pattern},"
            f"genre.ilike.{pattern}"
        )
        .execute()
    )

    return response.data


def update_video(video_id: int, updates: dict) -> dict | None:
    """Update a video and return the updated record"""

    allowed_fields = {
        "title", "year", "director",
        "rating", "genre", "total_quantity"
    }

    if not updates or not set(updates).issubset(allowed_fields):
        raise ValueError("Invalid or empty video updates")

    if "title" in updates:
        if not isinstance(updates["title"], str) or not updates["title"].strip():
            raise ValueError("Video title cannot be empty")

    if "total_quantity" in updates:
        if updates["total_quantity"] is None or updates["total_quantity"] < 0:
            raise ValueError("Total quantity cannot be negative")

    response = (
        supabase.table("Videos")
        .update(updates)
        .eq("video_id", video_id)
        .execute()
    )

    return response.data[0] if response.data else None


def delete_video(video_id: int) -> bool:
    """Delete a video, return true if deleted"""

    response = (
        supabase.table("Videos")
        .delete()
        .eq("video_id", video_id)
        .execute()
    )

    return len(response.data) > 0


def total_quantity(video_id: int) -> int | None:
    """Return the total number of copies, or none if not found"""

    video = get_video(video_id)

    if video is None:
        return None

    return video["total_quantity"]


# Calculation
def available_quantity(video_id: int) -> int:
    """Calculate available copies after accounting for active rentals"""

    total = total_quantity(video_id)

    if total is None:
        raise ValueError("Video not found")

    response = (
        supabase.table("Rentals")
        .select("rental_id", count="exact")
        .eq("video_id", video_id)
        .eq("currently_rented", True)
        .execute()
    )

    rented = response.count or 0

    return max(0, total - rented)
