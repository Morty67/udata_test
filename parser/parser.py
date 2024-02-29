import asyncio
import logging
import time
from typing import List

import aiohttp
import bs4

from data_saver import DataSaver
from get_all_links import LinkFetcher
from utils import (
    parse_description,
    parse_product_name,
    scrape_nutrition_info_with_selenium,
)

URL = "https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/000000000 Safari/537.36",
}
logging.basicConfig(level=logging.INFO)


class AsyncMcDonaldsScraper:
    """
    A class to scrape product information from the McDonald's menu page asynchronously.

    Attributes:
        url (str): The URL of the McDonald's menu page.
        links (List[str]): List of product URLs to scrape.
        data (List[dict]): List to store scraped product information.
    """

    def __init__(self, url: str) -> None:
        """
        Initialize the AsyncMcDonaldsScraper instance.

        Parameters:
        - url (str): The URL of the McDonald's menu page.
        """
        self.url = url
        self.links: List[str] = []
        self.data: List[dict] = []

    async def fetch_product_details(
        self,
        session: aiohttp.ClientSession,
        semaphore: asyncio.Semaphore,
        product_url: str,
    ) -> None:
        """
        Fetch product details asynchronously.

        Parameters:
            session (aiohttp.ClientSession): An aiohttp ClientSession object.
            semaphore (asyncio.Semaphore): Semaphore to limit concurrent requests.
            product_url (str): URL of the product to scrape.
        """
        async with semaphore:
            async with session.get(product_url, headers=HEADERS) as response:
                html_text = await response.text()
                soup = bs4.BeautifulSoup(html_text, "html.parser")

                product_name = await parse_product_name(soup)
                product_description = await parse_description(soup)

                product_info = {
                    "name": product_name,
                    "description": product_description,
                }

                nutrition_info = await scrape_nutrition_info_with_selenium(
                    product_url
                )
                product_info.update(nutrition_info)

                self.data.append(product_info)
                logging.info(f"Fetched details for product: {product_name}")

    async def scrape_product_info(self):
        """
        Scrape product information asynchronously.
        """
        link_fetcher = LinkFetcher(self.url)
        self.links = await link_fetcher.fetch_links()

        async with aiohttp.ClientSession() as session:
            tasks = []
            semaphore = asyncio.Semaphore(
                15
            )  # Limit on the number of simultaneous requests
            for url in self.links:
                tasks.append(
                    self.fetch_product_details(session, semaphore, url)
                )
                await asyncio.sleep(0.1)  # Delay between requests
            await asyncio.gather(*tasks)


if __name__ == "__main__":
    start_time = time.time()

    async_scraper = AsyncMcDonaldsScraper(URL)
    asyncio.run(async_scraper.scrape_product_info())
    data_saver = DataSaver()
    data_saver.save_to_json(async_scraper.data)

    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"Total execution time: {elapsed_time} seconds")
