## McDonald's Menu Scraper
This project is a scraper for the McDonald's menu available at McDonald's Ukraine website. The script is written in Python and is designed to collect information about all items on the menu, including their name, description, nutritional values (calories, fats, carbs, proteins, unsaturated fats, sugar, salt), and portion size. The collected data is saved locally in a JSON file.
## Installing / Getting started:
```shell
To get started, you need to clone the repository from GitHub: https://github.com/Morty67/udata_test/tree/developer
Python 3.12 must be installed

python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)

pip install -r requirements.txt
```
## Fields to Collect:
*  Name
*  Description
*  Calories
*  Fats.
*  Carbohydrates.
*  Proteins.
*  Unsaturated fats.
*  Sugar
*  Salt
*  Portion

## How to run
*  To run the scraper, execute the following command in your terminal:

```shell
python parser/parser.py
```

## Endpoints:
*  At the end of the scraper you can access the collected data through the following endpoints:
```shell
python -m uvicorn src.main:app --reload
```
*  Go to http://127.0.0.1:8000/docs
*  GET /all_products/: Returns all information about all products on the McDonald's menu.
*  GET /products/{product_name}: Returns information about a specific product on the menu.
*  GET /products/{product_name}/{product_field}: Returns information about a specific field of a particular product on the menu.