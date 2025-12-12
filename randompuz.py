#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "requests",
#   "beautifulsoup4",
# ]
# ///
import random
import re
import sys

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://jigsawpuzzles.io'
LATEST_URL = BASE_URL + '/browse/latest'
MAX_ERRORS = 5
TIMEOUT = 5

def get_latest_image_number():
    response = requests.get(LATEST_URL, timeout=TIMEOUT)
    soup = BeautifulSoup(response.text, features='html.parser')
    first_image_link_tag = soup.select_one('a[href^="/browse/image"]')
    mat = re.search(r'\d+', first_image_link_tag['href'])
    latest_image_number = int(mat[0])
    return latest_image_number

def get_random_image_url(low, high):
    random_image_number = random.randint(low, high)
    return f'{BASE_URL}/browse/image/{random_image_number}'

lowest_image_number = 0
highest_image_number = 0

if len(sys.argv) > 1:
    lowest_image_number = sys.argv[1]
    if lowest_image_number:
        if lowest_image_number.isnumeric() or lowest_image_number[0] == '-' and lowest_image_number[1:].isnumeric():
            lowest_image_number = int(lowest_image_number)
        else:
            sys.exit("Lowest image number must be numeric.")
if not lowest_image_number:
    lowest_image_number = 1

if len(sys.argv) > 2:
    highest_image_number = sys.argv[2]
    if highest_image_number:
        if highest_image_number.isnumeric():
            highest_image_number = int(highest_image_number)
        else:
            sys.exit("Highest image number must be numeric.")

if not highest_image_number:
    highest_image_number = get_latest_image_number()

if lowest_image_number < 0:
    lowest_image_number = highest_image_number + lowest_image_number

if lowest_image_number > highest_image_number:
   sys.exit(f"Lowest image number {lowest_image_number} must be less than or equal to highest image number {highest_image_number}.")

errors = 0
urls_tried = []
random_image_url = None
size_of_range = highest_image_number - lowest_image_number + 1
max_errors = min(MAX_ERRORS, size_of_range)
while not random_image_url and errors < max_errors and len(urls_tried) < size_of_range:
    url = get_random_image_url(lowest_image_number, highest_image_number)
    if url not in urls_tried:
        response = requests.get(url, timeout=TIMEOUT)
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
