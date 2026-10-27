def get_inventory(
    videos: list[dict],
    genre: str | None = None,
    availability: str | None = None,
    sort_by: str = "title",
    descending: bool = False
) -> list[dict]:
    
    """Return video records filtered and sorted for the GUI.
    Accepts a video list, optional genre and availability filters,
    a sorting field, and a descending flag.
    Returns an empty list if nothing matches.
    Raises ValueError for invalid options or quantities. """
    
    fields = ["title", "genre", "year", "rating", "director", "availability"]

    if sort_by not in fields:
        raise ValueError("Invalid sorting field.")

    genre = genre.strip().casefold() if genre else ""
    availability = availability.strip().casefold() if availability else ""

    if availability not in ["", "available", "rented"]:
        raise ValueError("Choose Available or Rented.")

    results = []

    for video in videos:
        if genre and str(video.get("genre") or "").casefold() != genre:
            continue

        if availability:
            if get_availability(video).casefold() != availability:
                continue

        results.append(video)

    def sort_value(video):
        
        """Return the field value used to sort one video."""
        
        if sort_by == "availability":
            return get_availability(video)

        if sort_by in ["year", "rating"]:
            return float(video[sort_by])

        return str(video.get(sort_by) or "").casefold()

    if sort_by in ["year", "rating"]:
        filled = [v for v in results if v.get(sort_by) not in [None, ""]]
        missing = [v for v in results if v.get(sort_by) in [None, ""]]
        return sorted(filled, key=sort_value, reverse=descending) + missing

    return sorted(results, key=sort_value, reverse=descending)


def get_availability(video: dict) -> str:
    
    """Return Available, Rented, or No copies for a video. 
    Requires integer total_quantity and available_quantity fields.
    Raises ValueError for missing or inconsistent quantities. """
    
    total = video.get("total_quantity")
    available = video.get("available_quantity")

    if type(total) is not int or type(available) is not int:
        raise ValueError("Video quantities must be integers.")

    if not 0 <= available <= total:
        raise ValueError("Available quantity must be between zero and total.")

    if total == 0:
        return "No copies"

    return "Available" if available > 0 else "Rented"
