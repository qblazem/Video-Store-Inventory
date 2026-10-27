def sort_inventory(
    videos: list[dict],
    sort_by: str = "title",
    descending: bool = False
) -> list[dict]:
    """Return videos sorted by the selected field."""
    if sort_by not in ["title", "genre", "year", "availability"]:
        raise ValueError("Choose title, genre, year, or availability.")

    def get_sort_value(video):
        if sort_by == "availability":
            return video["available_quantity"] > 0

        if sort_by == "year":
            return int(video.get("year") or 0)

        return str(video.get(sort_by) or "").casefold()

    return sorted(videos, key=get_sort_value, reverse=descending)


def filter_inventory(
    videos: list[dict],
    genre: str | None = None,
    availability: str | None = None
) -> list[dict]:
    """Return videos matching the selected filters."""
    if genre is not None:
        genre = genre.strip().casefold() or None

    if availability is not None:
        availability = availability.strip().casefold() or None

    if availability not in [None, "available", "rented"]:
        raise ValueError("Choose Available or Rented.")

    results = []

    for video in videos:
        video_genre = str(video.get("genre") or "").strip().casefold()

        if genre is not None and video_genre != genre:
            continue

        if availability is not None:
            available = video["available_quantity"]

            if availability == "available" and available <= 0:
                continue

            if availability == "rented":
                if video["total_quantity"] <= 0 or available != 0:
                    continue

        results.append(video)

    return results
