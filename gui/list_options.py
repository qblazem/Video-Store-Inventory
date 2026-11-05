"""Filtering and sorting helpers for the inventory and customer tables"""
from collections import Counter



AGE_ORDER = {'G': 0, 'PG': 1, 'PG-13': 2, 'R': 3, 'NC-17': 4}


def filter_sort_videos(videos, sort_by='Name', available_only=False,
                       years=(), ratings=(), genres=(), active_rentals=()):
    """Return videos matching active filters in the requested order"""
    rented = Counter(r['video_id'] for r in active_rentals if r.get('video_id') is not None)
    result = []
    for video in videos:
        year = video.get('year')
        try:
            year = int(year) if year is not None and str(year).strip() else None
        except (ValueError, TypeError):
            year = None
        if years and not any(low <= year <= high for low, high in years if year is not None):
            continue
        if ratings and str(video.get('rating') or '').upper() not in ratings:
            continue
        if genres and str(video.get('genre') or '').casefold() not in genres:
            continue
        if available_only and int(video.get('total_quantity') or 0) <= rented[video['video_id']]:
            continue
        result.append(video)

    def key(v):
        field = {'Name': 'title', 'Director': 'director', 'Genre': 'genre',
                 'Rating': 'rating'}.get(sort_by)
        if sort_by == 'Year':
            try:
                value = int(v.get('year'))
            except (ValueError, TypeError):
                value = -1
            return value, str(v.get('title') or '').casefold()
        if sort_by == 'Rental_Status':
            remaining = int(v.get('total_quantity') or 0) - rented[v['video_id']]
            return (remaining <= 0, str(v.get('title') or '').casefold())
        if sort_by == 'Rating':
            rating = str(v.get('rating') or '').upper()
            return AGE_ORDER.get(rating, 99), str(v.get('title') or '').casefold()
        return str(v.get(field or 'title') or '').casefold(), str(v.get('title') or '').casefold()

    return sorted(result, key=key)


def filter_sort_customers(customers, sort_by='First', renting_only=False,
                          email_providers=(), active_rentals=()):
    """Return customers matching active filters in the requested order"""
    active_customers = {r.get('customer_id') for r in active_rentals}
    common_domains = {
        'Gmail': {'gmail.com'}, 'Icloud': {'icloud.com', 'me.com', 'mac.com'},
        'Yahoo': {'yahoo.com', 'ymail.com'}, 'Outlook': {'outlook.com', 'hotmail.com', 'live.com'}
    }
    known = set().union(*common_domains.values())
    result = []
    for customer in customers:
        if renting_only and customer.get('customer_id') not in active_customers:
            continue
        if email_providers:
            email = str(customer.get('email') or '').strip().lower()
            domain = email.rsplit('@', 1)[-1] if '@' in email else ''
            matched = any(domain in common_domains[provider] for provider in email_providers
                          if provider in common_domains)
            if 'Other' in email_providers and domain and domain not in known:
                matched = True
            if not matched:
                continue
        result.append(customer)
    field = {'First': 'first_name', 'Last': 'last_name', 'Address': 'address',
             'Phone': 'phone', 'Email': 'email'}.get(sort_by, 'first_name')
    return sorted(result, key=lambda c: (str(c.get(field) or '').casefold(),
                                          str(c.get('first_name') or '').casefold()))
