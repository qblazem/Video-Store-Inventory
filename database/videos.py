
def create_video(
    title: str,
    year: str | None = None,
    director: str | None = None,
    rating: float | None = None,
    genre: str | None = None,
    total_quantity: int = 0
) -> dict:
    pass


def get_video(video_id: int) -> dict | None:
    pass


def get_all_videos() -> list[dict]:
    pass


def search_video(search_term: str) -> list[dict]:
    pass


def update_video(video_id: int, updates: dict) -> dict | None:
    pass


def delete_video(video_id: int) -> bool:
    pass


def total_quantity(video_id: int) -> int | None:
    pass


# Calculation
def available_quantity(video_id: int) -> int:
    pass
