"""
This file fetches data from a public API, handling two real-world problems:
  1. Pagination — the API won't give us everything in one request
  2. Failures — the API (or the network) sometimes fails temporarily,
     and we should retry politely instead of giving up immediately
"""

import requests
import time
from logging import getLogger, basicConfig, INFO

# Basic logging setup so we can see what's happening as it runs
basicConfig(level=INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = getLogger(__name__)

# The base URL of the API we're fetching from
BASE_URL = "https://jsonplaceholder.typicode.com/posts"


def fetch_with_retry(url: str, params: dict = None, max_retries: int = 5) -> requests.Response:
    """
    Fetches a single URL, retrying with EXPONENTIAL BACKOFF if it fails.

    'Exponential backoff' just means: wait longer after each failure.
    Attempt 1 fails -> wait 1 second
    Attempt 2 fails -> wait 2 seconds
    Attempt 3 fails -> wait 4 seconds
    ...and so on. This is the "polite" way to retry — hammering a
    struggling server with instant retries usually makes things worse.
    """
    for attempt in range(max_retries):
        try:
            # Actually make the HTTP request. timeout=10 means:
            # "give up waiting after 10 seconds" — without this, a hung
            # connection could freeze your script forever.
            response = requests.get(url, params=params, timeout=10)

            # response.status_code is the API's way of saying "here's what happened"
            # 200 means success. Anything else means something went wrong.
            if response.status_code == 200:
                return response  # success! hand the response back immediately

            # If we got rate-limited (429) or a server error (5xx),
            # this is worth retrying — the problem might be temporary.
            if response.status_code == 429 or response.status_code >= 500:
                wait_time = 2 ** attempt  # 1, 2, 4, 8, 16 seconds...
                logger.warning(
                    f"Got status {response.status_code} on attempt {attempt + 1}. "
                    f"Waiting {wait_time}s before retrying..."
                )
                time.sleep(wait_time)
                continue  # go back to the top of the loop and try again

            # Any OTHER error (like 404 Not Found) won't fix itself by
            # retrying — that's a real problem, not a temporary one.
            # So we raise an error immediately instead of wasting time retrying.
            response.raise_for_status()

        except requests.exceptions.ConnectionError:
            # This catches network-level failures (like no internet at all)
            wait_time = 2 ** attempt
            logger.warning(f"Connection error on attempt {attempt + 1}. Waiting {wait_time}s...")
            time.sleep(wait_time)

    # If we've used up ALL our retries and still failed, give up loudly.
    # This is important — silently giving up would hide a real problem.
    raise RuntimeError(f"Failed to fetch {url} after {max_retries} attempts")


def fetch_all_posts(page_size: int = 10) -> list[dict]:
    """
    Fetches ALL posts from the API, page by page, using fetch_with_retry()
    for every single page — so pagination and retry logic work together.
    """
    all_posts = []
    page = 1

    while True:
        # _limit and _page are query parameters this specific API understands
        # for pagination — different APIs use different parameter names,
        # always check the API's documentation for its actual pagination style.
        params = {"_limit": page_size, "_page": page}

        logger.info(f"Fetching page {page}...")
        response = fetch_with_retry(BASE_URL, params=params)

        # .json() turns the API's raw text response into a Python list/dict
        page_data = response.json()

        # If the API returns an empty list, there's no more data — stop.
        if not page_data:
            logger.info("No more data. Pagination complete.")
            break

        all_posts.extend(page_data)  # add this page's posts to our growing list
        logger.info(f"Page {page} returned {len(page_data)} posts. Total so far: {len(all_posts)}")

        page += 1  # move to the next page for the next loop

    return all_posts


if __name__ == "__main__":
    posts = fetch_all_posts(page_size=10)
    logger.info(f"DONE. Fetched {len(posts)} total posts.")
