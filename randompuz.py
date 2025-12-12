#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "requests-cache",
#   "beautifulsoup4",
#   "platformdirs"
# ]
# ///
from datetime import timedelta
import os
import random
import re
import sys

from bs4 import BeautifulSoup
from platformdirs import user_data_dir
import requests_cache

USER_DATA_PATH = os.path.join(user_data_dir(), "puzzle-pals")
CACHE_FILE = os.path.join(USER_DATA_PATH, "requests_cache.db")
BASE_URL = 'https://jigsawpuzzles.io'
LATEST_URL = BASE_URL + '/browse/latest'
MAX_ERRORS = 5
TIMEOUT = 5

def get_latest_image_number(session):
    response = session.get(LATEST_URL, timeout=TIMEOUT)
    soup = BeautifulSoup(response.text, features='html.parser')
    first_image_link_tag = soup.select_one('a[href^="/browse/image"]')
    mat = re.search(r'\d+', first_image_link_tag['href'])
    latest_image_number = int(mat[0])
    return latest_image_number

def get_random_image_url(low, high):
    random_image_number = random.randint(low, high)
    return f'{BASE_URL}/browse/image/{random_image_number}'

def get_params(session):
    lowest = 0
    highest = 0

    if len(sys.argv) > 1:
        lowest = sys.argv[1]
        if lowest:
            if lowest.isnumeric() or lowest[0] == '-' and lowest[1:].isnumeric():
                lowest = int(lowest)
            else:
                sys.exit("Lowest image number must be numeric.")
    if not lowest:
        lowest = 1

    if len(sys.argv) > 2:
        highest = sys.argv[2]
        if highest:
            if highest.isnumeric():
                highest = int(highest)
            else:
                sys.exit("Highest image number must be numeric.")

    if not highest:
        highest = get_latest_image_number(session)

    if lowest < 0:
        lowest = highest + lowest

    if lowest > highest:
        sys.exit(f"Lowest image number {lowest} must be less than or equal to highest image number {highest}.")
    return (lowest, highest)

session = requests_cache.CachedSession(CACHE_FILE, expire_after=timedelta(days=1))
lowest_image_number, highest_image_number = get_params(session)

errors = 0
urls_tried = []
random_image_url = None
size_of_range = highest_image_number - lowest_image_number + 1
max_errors = min(MAX_ERRORS, size_of_range)
while not random_image_url and errors < max_errors and len(urls_tried) < size_of_range:
    url = get_random_image_url(lowest_image_number, highest_image_number)
    if url not in urls_tried:
        response = session.get(url, timeout=TIMEOUT)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, features='html.parser')
            main_image = soup.select_one('img.main-image')
            if main_image:
                random_image_url = url
            else:
                print(f"No image on page; discarding: {url}")
                urls_tried.append(url)
                errors += 1
        else:
            print(f"Image not found; discarding: {url}")
            urls_tried.append(url)
            errors += 1
    else:
        print(f"Not requesting URL again: {url}")
if not random_image_url:
    sys.exit(f"Gave up after {errors} retries. Site down or no valid images in range: {lowest_image_number}-{highest_image_number}")

print(f"\nRandom puzzle image: {random_image_url}\n")
