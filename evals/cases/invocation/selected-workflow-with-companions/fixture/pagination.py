def page_count(total_items, page_size):
    """Return how many pages are needed to show total_items, page_size per page."""
    if page_size <= 0:
        raise ValueError("page_size must be positive")
    return total_items // page_size
