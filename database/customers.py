
def create_customer(
    first_name: str,
    last_name: str | None = None,
    address: str | None = None,
    phone: str | None = None,
    email: str | None = None
) -> dict:
    pass


def get_customer(customer_id: int) -> dict | None:
    pass


def get_all_customers() -> list[dict]:
    pass


def search_customers(search_term: str) -> list[dict]:
    pass


def update_customer(
    customer_id: int,
    updates: dict
) -> dict | None:
    pass


def delete_customer(customer_id: int) -> bool:
    pass