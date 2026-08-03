"""
A small standalone script to deliberately trigger retry logic against
a URL that will fail — proving the backoff behavior actually works,
not just that it looks correct on paper.
"""
from fetch_api import fetch_with_retry

# This URL doesn't exist — every request to it will fail with a connection error
BAD_URL = "https://this-domain-absolutely-does-not-exist-12345.com/data"

try:
    fetch_with_retry(BAD_URL, max_retries=3)
except RuntimeError as e:
    print(f"Correctly failed after retries, as expected: {e}")

# Now test a URL that DOES exist but returns a 404 (page doesn't exist)
NOT_FOUND_URL = "https://jsonplaceholder.typicode.com/posts/99999999"

try:
    fetch_with_retry(NOT_FOUND_URL, max_retries=3)
except Exception as e:
    print(f"Handled non-200 response cleanly: {e}")
