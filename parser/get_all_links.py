import logging
from typing import List
from urllib.parse import urljoin

import aiohttp
import bs4


class LinkFetcher:
    """
    The LinkFetcher class is responsible for fetching links from the specified web page.
    """

    def __init__(self, url: str) -> None:
        """
        Initialize the LinkFetcher instance.

        Parameters:
        - url (str): The URL to fetch links from.
        """
        self.url = url

    async def fetch_links(self) -> List[str]:
        """
        Fetches links from the specified URL.

        Returns:
            List[str]: A list of URLs found on the page.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                links = []
                if response.status == 200:
                    html_text = await response.text()
                    soup = bs4.BeautifulSoup(html_text, "html.parser")
                    product_links = soup.find_all(
                        "a", class_="cmp-category__item-link"
                    )
                    for link in product_links:
                        href_value = link.get("href")
                        full_link = urljoin(self.url, href_value)
                        links.append(full_link)
                else:
                    logging.info(
                        f"Failed to retrieve page. Status code: {response.status}"
                    )
                return links
