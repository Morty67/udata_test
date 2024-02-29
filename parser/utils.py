import asyncio

import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def initialize_soup(html_text: str) -> bs4.BeautifulSoup:
    """
    Initialize BeautifulSoup object from HTML text.

    Args:
        html_text (str): The HTML text to parse.

    Returns:
        bs4.BeautifulSoup: The initialized BeautifulSoup object.
    """
    return bs4.BeautifulSoup(html_text, "html.parser")


async def parse_product_name(soup: bs4.BeautifulSoup) -> str:
    """
    Parse the product name from the BeautifulSoup object.

    Args:
        soup (bs4.BeautifulSoup): The BeautifulSoup object representing the HTML.

    Returns:
        str: The parsed product name.
    """
    product_name_element = soup.find(
        "span", class_="cmp-product-details-main__heading-title"
    )
    if product_name_element:
        return product_name_element.text.strip()
    else:
        return "No name available"


async def parse_description(soup: bs4.BeautifulSoup) -> str:
    """
    Parse the product description from the BeautifulSoup object.

    Args:
        soup (bs4.BeautifulSoup): The BeautifulSoup object representing the HTML.

    Returns:
        str: The parsed product description.
    """
    description_element = soup.find("div", class_="cmp-text")
    if description_element:
        description_text = description_element.text.strip()
        return description_text
    else:
        return "No description available."


async def initialize_driver():
    """
    Initialize the Selenium WebDriver.

    Returns:
        WebDriver: The initialized WebDriver object.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


async def translate_nutrient(nutrient: str, translation_dict: dict) -> str:
    """
    Translate nutrient names using a translation dictionary.

    Args:
        nutrient (str): The nutrient name to translate.
        translation_dict (dict): The translation dictionary.

    Returns:
        str: The translated nutrient name, or the original if not found in the dictionary.
    """
    if nutrient in translation_dict:
        return translation_dict[nutrient]
    return nutrient


async def scrape_nutrition_info(driver: webdriver.Chrome, url: str) -> dict:
    """
    Scrape nutrition information using Selenium WebDriver.

    Args:
        driver (WebDriver): The initialized WebDriver object.
        url (str): The URL of the product page.

    Returns:
        dict: A dictionary containing the scraped nutrition information.
    """
    driver.get(url)
    await asyncio.sleep(0.2)

    button = driver.find_element(
        By.ID, "accordion-29309a7a60-item-9ea8a10642-button"
    )
    button.click()
    await asyncio.sleep(0.2)

    nutrition_items = driver.find_elements(
        By.CLASS_NAME, "cmp-nutrition-summary__heading-primary-item"
    )
    nutrition_dict = {}

    translation_dict = {
        "Калорійність": "calories",
        "Жири": "fats",
        "Вуглеводи": "carbs",
        "Білки": "proteins",
        "НЖК:": "unsaturated fats",
        "Цукор:": "sugar",
        "Сіль:": "salt",
        "Порція:": "portion",
    }

    for item in nutrition_items:
        name = (
            item.find_element(By.CLASS_NAME, "sr-only-pd")
            .get_attribute("textContent")
            .strip()
        )
        parts = name.split()
        nutrient = parts[1]
        value = parts[0] + " " + " ".join(parts[2:])
        nutrient = await translate_nutrient(nutrient, translation_dict)
        nutrition_dict[nutrient] = value

    nutrition_details = driver.find_elements(
        By.CLASS_NAME, "cmp-nutrition-summary__details-column-view-mobile"
    )
    for detail in nutrition_details:
        nutrition_info = detail.find_elements(By.CLASS_NAME, "label-item")
        for info in nutrition_info:
            metric = info.find_element(By.CLASS_NAME, "metric").text
            value = info.find_element(By.CLASS_NAME, "value").text
            metric = await translate_nutrient(metric, translation_dict)
            nutrition_dict[metric] = "".join(value.split()[:4])

    return nutrition_dict


async def scrape_nutrition_info_with_selenium(url: str) -> dict:
    """
    Scrape nutrition information using Selenium WebDriver.

    Args:
        url (str): The URL of the product page.

    Returns:
        dict: A dictionary containing the scraped nutrition information.
    """
    driver = await initialize_driver()
    try:
        return await scrape_nutrition_info(driver, url)
    finally:
        driver.quit()
