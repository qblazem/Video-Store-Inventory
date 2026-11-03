
from database.database import supabase


def _validate_video_fields(fields: dict) -> dict:
    """Validate and format video fields before saving"""

    fields = fields.copy()

    if "title" in fields:
        title = fields["title"]

        if not isinstance(title, str) or not title.strip():
            raise ValueError("Video title cannot be empty")

        fields["title"] = title.strip()

    if "year" in fields:
        year = fields["year"]

        if year is None or year == "":
            fields["year"] = None
        else:
            try:
                year = int(str(year).strip())
            except ValueError:
                raise ValueError("Year must be a valid integer")

            if year < 1888 or year > 2100:
                raise ValueError("Year must be between 1888 and 2100")

            fields["year"] = year

    if "rating" in fields:
        rating = fields["rating"]

        if rating is None or rating == "":
            fields["rating"] = None
        else:
            try:
                rating = float(rating)
            except (ValueError, TypeError):
                raise ValueError("Rating must be a number")

            if not 0 <= rating <= 10:
                raise ValueError("Rating must be between 0 and 10")

            fields["rating"] = rating

    if "total_quantity" in fields:
        quantity = fields["total_quantity"]

        try:
            quantity = int(str(quantity).strip())
        except (ValueError, TypeError):
            raise ValueError("Total quantity must be a valid integer")

        if quantity < 0:
            raise ValueError("Total quantity cannot be negative")

        fields["total_quantity"] = quantity

    return fields


def _active_rental_count(video_id: int) -> int:
    """Count the active rentals for a video"""

    response = (
        supabase.table("Rentals")
        .select("rental_id", count="exact", head=True)
        .eq("video_id", video_id)
        .eq("currently_rented", True)
        .execute()
    )

    return response.count or 0


def create_video(
    title: str,
    year: int | str | None = None,
    director: str | None = None,
    rating: float | None = None,
    genre: str | None = None,
    total_quantity: int = 0
) -> dict:
    """Create a video and return the new record"""

    video = _validate_video_fields({
        "title": title,
        "year": year,
        "director": director,
        "rating": rating,
        "genre": genre,
        "total_quantity": total_quantity
    })

    response = supabase.table("Videos").insert(video).execute()

    return response.data[0]


def get_video(video_id: int) -> dict | None:
    """Get a video by ID or none if not found"""

    response = (
        supabase.table("Videos")
        .select("*")
        .eq("video_id", video_id)
        .execute()
    )

    return response.data[0] if response.data else None


def get_all_videos() -> list[dict]:
    """Return all videos up to the API row limit"""

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

    updates = _validate_video_fields(updates)

    if "total_quantity" in updates:
        rented = _active_rental_count(video_id)

        if updates["total_quantity"] < rented:
            raise ValueError(
                "Total quantity cannot be less than active rentals"
            )

    response = (
        supabase.table("Videos")
        .update(updates)
        .eq("video_id", video_id)
        .execute()
    )

    return response.data[0] if response.data else None


def delete_video(video_id: int) -> bool:
    """Delete a video and return true if deleted"""

    response = (
        supabase.table("Videos")
        .delete()
        .eq("video_id", video_id)
        .execute()
    )

    return bool(response.data)


def total_quantity(video_id: int) -> int | None:
    """Return total copies or none if not found"""

    video = get_video(video_id)

    if video is None:
        return None

    return video["total_quantity"]


def available_quantity(video_id: int) -> int:
    """Calculate available copies after active rentals"""

    total = total_quantity(video_id)

    if total is None:
        raise ValueError("Video not found")

    rented = _active_rental_count(video_id)

    return max(0, total - rented)
