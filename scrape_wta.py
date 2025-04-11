import requests
from requests.exceptions import RequestException
from requests.models import Response

from bs4 import BeautifulSoup
from tqdm import tqdm
import json
import time
import typing as t
import logging
import random
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constant for the hike listing URL
HIKE_LISTING_URL = "https://www.wta.org/go-outside/hikes/?b_start:int={}"

def safe_get(url: str, retries=3, backoff=2) -> t.Union[Response,None]:
    """ Make a GET request using python requests package. If the request
    fails (example: returns a 503), back off, then retry.

    Args:
        url (str): The URL to request.

    Returns:
        Response | None: Return the python request or None
    """
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except RequestException as e:
            logger.warning(f"Attempt {attempt+1} failed for {url}: {e}")
            time.sleep(backoff * (attempt + 1))
    logger.error(f"All retries failed for {url}")
    return None

def scrape_data(url: str) -> t.Dict[str,str]:
    """Gather data from the html content of the WTA hike page.

    Args:
        url (str):  The URL to scrape.

    Returns:
        Dict[str,str]: parsed information
    """
    req: Response | None = safe_get(url)
    if req is None:
        return {
            "title": "N/A",
            "url": url,
            "distance": "N/A",
            "elevation_gain": "N/A",
            "high_point": "N/A",
            "calculated_difficulty": "N/A",
            "rating": "N/A",
            "summary": "request failed"
        }
    soup = BeautifulSoup(req.content, "html.parser")

    def get_text(selector):
        el = soup.select_one(selector)
        return el.get_text(strip=True) if el else None

    title = get_text("h1.documentFirstHeading")

    # Extract length
    length_tag = soup.select_one("div.hike-stats__stat:has(dt:-soup-contains('Length')) dd")

    distance = length_tag.text.strip() if length_tag else "N/A"

    # Extract elevation gain
    elevation_tag = soup.select_one("div.hike-stats__stat:has(dt:-soup-contains('Elevation Gain')) dd")
    elevation = elevation_tag.text.strip() if elevation_tag else "N/A"

    # Extract highest point
    highest_point_tag = soup.select_one("div.hike-stats__stat:has(dt:-soup-contains('Highest Point')) dd")
    high_point = highest_point_tag.text.strip() if highest_point_tag else "N/A"

    # Extract highest point
    calculated_difficulty = soup.select_one("div.hike-stats__stat:has(dt:-soup-contains('Calculated Difficulty')) dd")
    difficulty = calculated_difficulty.text.strip() if calculated_difficulty else "N/A"

    # Extract average rating
    rating_div = soup.select_one("div.AverageRating div.current-rating")
    rating = rating_div.text.strip() if rating_div else "N/A"

    summary_div = soup.find(id='hike-body-text')
    if summary_div:
        paragraphs = summary_div.find_all('p')
        summary_text = '\n\n'.join(p.get_text(strip=True) for p in paragraphs)
    else:
        summary_text = "No summary provided"

    return {
        "title": title,
        "url": url,
        "distance": distance,
        "elevation_gain": elevation,
        "high_point": high_point,
        "calculated_difficulty": difficulty,
        "rating": rating,
        "summary": summary_text
    }

def get_page_links(page: int) -> t.Union[t.List[str], t.List]:
    """Scrapes all the hike URLs from the WTA listing pages.

    This function will extract all the links from a provided URL.

    Args:
        start (int): The starting index for pagination.

    Returns:
        List[str]: A list of hike URLs extracted from the page.
    """
    try:
        req: Response | None = safe_get(HIKE_LISTING_URL.format(page))
        if req is None:
            return []
        soup = BeautifulSoup(req.content, "html.parser")
        links = soup.select("h3.listitem-title a")
        return [link.get("href") for link in links if link.get("href") and link.get("href").startswith("https://www.wta.org/go-hiking/hikes/")]
    except RequestException as e:
        logger.error(f"Error fetching page {page}: {e}")
        return []

def gather_hike_urls() -> t.List[str]:
    """Scrapes all the hike URLs from the WTA listing pages.

    Washington Trail Association provides 138 pages of hike
    listings. There are ~30 hike links per page. This method
    indexes through all 138 pages and consolidates the hike links
    into a list for future scraping.

    Returns:
        List[str]: A list of unique hike URLs.
    """
    hike_page_links = set()
    for start in tqdm(range(0, 6000, 30)):
        page_links: t.List[str] = get_page_links(start)
        hike_page_links.update(page_links)
        time.sleep(random.uniform(0.2, 0.5))
    return list(hike_page_links)

def main():
    """This function will gather the hiking URLs, extract the necessary data,
    and then write the data to a file.
    """
    hike_data: t.List[t.Dict[str,str]] = []

    hike_urls: t.List[str] = gather_hike_urls()

    for url in tqdm(hike_urls):
        try:
            hike = scrape_data(url)
            if hike:
                hike_data.append(hike)
            time.sleep(0.2)
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    output_file = f"wta_hikes_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    with open(output_file, "w") as f:
        json.dump(hike_data, f, indent=2)


if __name__ == "__main__":
    """If the script is called, run the main function.
    """
    main()