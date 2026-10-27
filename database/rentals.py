
def create_rental(
    customer_id: int,
    video_id: int
) -> dict:


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
